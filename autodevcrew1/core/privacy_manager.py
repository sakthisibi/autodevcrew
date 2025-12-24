import os
import json
from pathlib import Path
from typing import Dict, Any, Optional, List
import hashlib
from enum import Enum

class PrivacyLevel(Enum):
    STRICT = "strict"        # No external calls, all local
    MODERATE = "moderate"    # Local by default, optional external
    OPEN = "open"           # Allow external APIs

class DataRetentionPolicy(Enum):
    LOCAL_ONLY = "local_only"          # Keep all data locally
    ENCRYPTED_CLOUD = "encrypted_cloud" # Encrypt before cloud storage
    AUTO_PURGE = "auto_purge"          # Purge after task completion

class PrivacyManager:
    def __init__(self, privacy_level: PrivacyLevel = PrivacyLevel.STRICT):
        self.privacy_level = privacy_level
        self.data_retention_policy = DataRetentionPolicy.LOCAL_ONLY
        self.encryption_key = self._generate_encryption_key()
        self.blocked_domains = ["api.openai.com", "api.anthropic.com", "api.cohere.ai"]
        self.local_cache_dir = Path("~/.autodevcrew/cache").expanduser()
        self.local_cache_dir.mkdir(parents=True, exist_ok=True)
        
        # Data anonymization salt
        self.anonymization_salt = hashlib.sha256(os.urandom(32)).hexdigest()
    
    def _generate_encryption_key(self) -> bytes:
        """Generate encryption key for sensitive data"""
        key_material = os.urandom(32)
        return hashlib.sha256(key_material).digest()
    
    def ensure_local_execution(self, agent_name: str, operation: str) -> bool:
        """
        Enforce local-only execution based on privacy level
        Returns True if operation is allowed, False if blocked
        """
        if self.privacy_level == PrivacyLevel.STRICT:
            # Block all external network calls
            self._block_external_network()
            return True
        
        elif self.privacy_level == PrivacyLevel.MODERATE:
            # Allow only whitelisted domains
            allowed_domains = ["localhost", "127.0.0.1", "ollama", "huggingface.co"]
            # Check if operation needs external calls
            if self._requires_external(operation):
                print(f"⚠️ External operation '{operation}' requires privacy review")
                return False
            return True
        
        return True  # OPEN mode allows everything
    
    def _requires_external(self, operation: str) -> bool:
        # Simple heuristic for now
        return "download" in operation or "api" in operation or "http" in operation
    
    def _block_external_network(self):
        """Block external network calls"""
        import socket
        
        original_socket = socket.socket
        
        class BlockedSocket(original_socket):
            def connect(self, address):
                host, port = address[0], address[1]
                # Allow local connections
                if host in ["localhost", "127.0.0.1", "::1"]:
                    return super().connect(address)
                    
                raise ConnectionError(
                    f"Privacy violation: External connection to {host}:{port} blocked. "
                    f"System is in strict offline mode."
                )
        
        socket.socket = BlockedSocket
    
    def anonymize_data(self, data: Any) -> Any:
        """Anonymize sensitive data"""
        if isinstance(data, str):
            # Hash with salt for consistent anonymization
            return hashlib.sha256(f"{data}{self.anonymization_salt}".encode()).hexdigest()[:16]
        elif isinstance(data, dict):
            return {self.anonymize_data(k): self.anonymize_data(v) for k, v in data.items()}
        elif isinstance(data, list):
            return [self.anonymize_data(item) for item in data]
        return data
    
    def encrypt_sensitive_data(self, data: str) -> str:
        """Encrypt sensitive data before storage"""
        from cryptography.fernet import Fernet
        import base64
        
        # Generate Fernet key from our encryption key (needs to be 32 url-safe base64-encoded bytes)
        # hashlib gives 32 bytes, we allow Fernet to generate its own valid key for this session
        # Real impl would manage keys better
        fernet_key = base64.urlsafe_b64encode(self.encryption_key)
        cipher = Fernet(fernet_key)
        
        encrypted = cipher.encrypt(data.encode())
        
        # Store both encrypted data and key (key should be in secure storage)
        return json.dumps({
            "encrypted": encrypted.decode(),
            "key": fernet_key.decode()
        })
    
    def store_local_only(self, data: Dict[str, Any], task_id: str) -> str:
        """Store data locally with privacy controls"""
        
        # Anonymize sensitive fields
        anonymized = self.anonymize_data(data)
        
        # Encrypt if needed
        if self.data_retention_policy == DataRetentionPolicy.ENCRYPTED_CLOUD:
            encrypted = self.encrypt_sensitive_data(json.dumps(anonymized))
            storage_data = {"encrypted": True, "data": encrypted}
        else:
            storage_data = {"encrypted": False, "data": anonymized}
        
        # Save to local cache
        cache_file = self.local_cache_dir / f"task_{task_id}.json"
        with open(cache_file, 'w') as f:
            json.dump(storage_data, f, indent=2)
        
        return str(cache_file)
    
    def cleanup_sensitive_data(self, task_id: str):
        """Clean up sensitive data based on retention policy"""
        if self.data_retention_policy == DataRetentionPolicy.AUTO_PURGE:
            cache_file = self.local_cache_dir / f"task_{task_id}.json"
            if cache_file.exists():
                # Secure delete (overwrite before removal)
                with open(cache_file, 'wb') as f:
                    f.write(os.urandom(cache_file.stat().st_size))
                cache_file.unlink()
    
    def generate_privacy_report(self) -> Dict[str, Any]:
        """Generate privacy compliance report"""
        return {
            "privacy_level": self.privacy_level.value,
            "data_retention_policy": self.data_retention_policy.value,
            "local_cache_size": sum(f.stat().st_size for f in self.local_cache_dir.glob('*')),
            "blocked_domains_count": len(self.blocked_domains),
            "encryption_enabled": self.data_retention_policy == DataRetentionPolicy.ENCRYPTED_CLOUD
        }

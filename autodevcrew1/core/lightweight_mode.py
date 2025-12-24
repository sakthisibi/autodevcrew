try:
    import torch
    TORCH_AVAILABLE = True
except ImportError:
    TORCH_AVAILABLE = False
    torch = None

from pathlib import Path
import json
from typing import Dict, Any, Optional
from dataclasses import dataclass
from enum import Enum

class QuantizationLevel(Enum):
    FP16 = "fp16"        # Half precision
    INT8 = "int8"        # 8-bit quantization
    INT4 = "int4"        # 4-bit quantization
    GPTQ = "gptq"        # GPTQ quantization

@dataclass
class HardwareProfile:
    ram_gb: float
    vram_gb: float
    cpu_cores: int
    has_gpu: bool
    gpu_model: Optional[str] = None

class LightweightMode:
    def __init__(self, hardware_profile: Optional[HardwareProfile] = None):
        self.hardware_profile = hardware_profile or self.detect_hardware()
        self.quantization_level = self.determine_optimal_quantization()
        self.simplified_agents = True
        self.basic_workflow_only = True
        self.enable_model_offloading = True
        self.cpu_offload_layers = 4
        
        # Load quantized models
        self.quantized_models_dir = Path("quantized_models")
        self.available_models = self.scan_available_models()
    
    def detect_hardware(self) -> HardwareProfile:
        """Auto-detect hardware capabilities"""
        import psutil
        import platform
        
        ram_gb = psutil.virtual_memory().total / (1024**3)
        cpu_cores = psutil.cpu_count(logical=False)
        
        # Try to detect GPU
        has_gpu = False
        gpu_model = None
        vram_gb = 0
        
        try:
            import torch
            if torch.cuda.is_available():
                has_gpu = True
                gpu_model = torch.cuda.get_device_name(0)
                vram_gb = torch.cuda.get_device_properties(0).total_memory / (1024**3)
        except:
            pass
        
        return HardwareProfile(
            ram_gb=ram_gb,
            vram_gb=vram_gb,
            cpu_cores=cpu_cores,
            has_gpu=has_gpu,
            gpu_model=gpu_model
        )
    
    def determine_optimal_quantization(self) -> QuantizationLevel:
        """Determine best quantization based on hardware"""
        if self.hardware_profile.vram_gb >= 8:
            return QuantizationLevel.FP16
        elif self.hardware_profile.vram_gb >= 4:
            return QuantizationLevel.INT8
        elif self.hardware_profile.vram_gb >= 2:
            return QuantizationLevel.INT4
        else:
            return QuantizationLevel.GPTQ  # Most memory efficient
    
    def scan_available_models(self) -> Dict[str, Path]:
        """Scan for available quantized models"""
        models = {}
        
        if not self.quantized_models_dir.exists():
            self.quantized_models_dir.mkdir(parents=True, exist_ok=True)
            self.download_default_models()
        
        for model_dir in self.quantized_models_dir.iterdir():
            if model_dir.is_dir():
                config_file = model_dir / "config.json"
                if config_file.exists():
                    with open(config_file) as f:
                        config = json.load(f)
                        models[config["model_name"]] = model_dir
        
        return models
    
    def download_default_models(self):
        """Download default quantized models for offline use"""
        default_models = {
            "llama2-7b-4bit": "https://huggingface.co/TheBloke/Llama-2-7B-GGUF/resolve/main/llama-2-7b.Q4_K_M.gguf",
            "mistral-7b-4bit": "https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.1-GGUF/resolve/main/mistral-7b-instruct-v0.1.Q4_K_M.gguf",
            "codellama-7b-4bit": "https://huggingface.co/TheBloke/CodeLlama-7B-GGUF/resolve/main/codellama-7b.Q4_K_M.gguf"
        }
        
        print("Downloading default quantized models for offline use...")
        
        for model_name, url in default_models.items():
            model_dir = self.quantized_models_dir / model_name
            model_dir.mkdir(exist_ok=True)
            
            # Download GGUF file
            import requests
            try:
                # Use a timeout to avoid hanging indefinitely if network is bad
                response = requests.get(url, stream=True, timeout=30)
                if response.status_code == 200:
                    model_file = model_dir / "model.gguf"
                    
                    with open(model_file, 'wb') as f:
                        for chunk in response.iter_content(chunk_size=8192):
                            f.write(chunk)
                    
                    # Create config
                    config = {
                        "model_name": model_name,
                        "quantization": "Q4_K_M",
                        "format": "GGUF",
                        "size_gb": model_file.stat().st_size / (1024**3),
                        "compatibility": "CPU/GPU",
                        "layers": 32
                    }
                    
                    with open(model_dir / "config.json", 'w') as f:
                        json.dump(config, f, indent=2)
                else:
                    print(f"Failed to download {model_name}: Status {response.status_code}")
            except Exception as e:
                print(f"Error downloading {model_name}: {e}")
    
    def load_quantized_model(self, model_name: str):
        """Load quantized model with optimal settings"""
        if model_name not in self.available_models:
            raise ValueError(f"Model {model_name} not available in quantized form")
        
        model_dir = self.available_models[model_name]
        model_file = model_dir / "model.gguf"
        
        # Use llama.cpp for GGUF models
        from llama_cpp import Llama
        
        llm = Llama(
            model_path=str(model_file),
            n_ctx=2048,  # Context window
            n_threads=self.hardware_profile.cpu_cores,
            n_gpu_layers=self.cpu_offload_layers if self.enable_model_offloading else 0,
            verbose=False
        )
        
        return llm
    
    def create_lightweight_agent(self, agent_type: str):
        """Create simplified agent for lightweight mode"""
        
        base_config = {
            "max_tokens": 512,
            "temperature": 0.7,
            "stream": False,
            "use_cache": True,
            "memory_limit": 100  # Only keep last 100 messages
        }
        
        if agent_type == "engineer":
            return {
                **base_config,
                "model": "codellama-7b-4bit",
                "strategy": "direct",  # Simple direct generation
                "code_templates": True,  # Use templates instead of full generation
                "quality_check": False  # Skip deep quality analysis
            }
        elif agent_type == "tester":
            return {
                **base_config,
                "model": "llama2-7b-4bit",
                "test_framework": "unittest",  # Use simple unittest
                "coverage_target": 70,  # Lower coverage target
                "max_test_cases": 5  # Limit test cases
            }
        elif agent_type == "devops":
            return {
                **base_config,
                "model": "mistral-7b-4bit",
                "simulate_only": True,  # Only simulate, don't actually deploy
                "environments": ["development"],  # Only dev environment
                "skip_security_scan": True
            }
        
        return base_config
    
    def optimize_memory_usage(self):
        """Apply memory optimization techniques"""
        
        optimizations = []
        
        # Clear CUDA cache if GPU available
        try:
            import torch
            if torch.cuda.is_available():
                torch.cuda.empty_cache()
                optimizations.append("Cleared CUDA cache")
        except:
            pass
        
        # Limit Python's memory usage
        try:
            # resource module is Unix only generally
            import resource
            memory_limit_gb = max(1, int(self.hardware_profile.ram_gb * 0.7))
            memory_limit_bytes = memory_limit_gb * 1024**3
            
            resource.setrlimit(resource.RLIMIT_AS, (memory_limit_bytes, memory_limit_bytes))
            optimizations.append(f"Set memory limit to {memory_limit_gb}GB")
        except ImportError:
            optimizations.append("Memory limit setting skipped (Windows/Unsupported OS)")
        except Exception as e:
            optimizations.append(f"Failed to set memory limit: {e}")
        
        # Enable memory-efficient attention
        try:
            import torch
            if hasattr(torch.nn.functional, 'scaled_dot_product_attention') and torch.cuda.is_available():
                torch.backends.cuda.enable_flash_sdp(True)
                torch.backends.cuda.enable_mem_efficient_sdp(True)
                optimizations.append("Enabled memory-efficient attention")
        except:
            pass
        
        return optimizations
    
    def get_performance_report(self) -> Dict[str, Any]:
        """Generate performance optimization report"""
        return {
            "hardware_profile": {
                "ram_gb": self.hardware_profile.ram_gb,
                "vram_gb": self.hardware_profile.vram_gb,
                "cpu_cores": self.hardware_profile.cpu_cores,
                "has_gpu": self.hardware_profile.has_gpu
            },
            "quantization_level": self.quantization_level.value,
            "available_models": list(self.available_models.keys()),
            "simplified_agents": self.simplified_agents,
            "basic_workflow": self.basic_workflow_only,
            "model_offloading": self.enable_model_offloading,
            "estimated_memory_usage_gb": self.estimate_memory_usage()
        }
    
    def estimate_memory_usage(self) -> float:
        """Estimate total memory usage in GB"""
        base_usage = 0.5  # Base system
        
        # Model memory
        if self.quantization_level == QuantizationLevel.FP16:
            model_memory = 14  # GB for 7B model in FP16
        elif self.quantization_level == QuantizationLevel.INT8:
            model_memory = 7   # GB for 7B model in INT8
        elif self.quantization_level == QuantizationLevel.INT4:
            model_memory = 3.5 # GB for 7B model in INT4
        else:  # GPTQ
            model_memory = 2   # GB for 7B model in GPTQ
        
        # Agent overhead
        agent_overhead = 0.5 if self.simplified_agents else 2.0
        
        return base_usage + model_memory + agent_overhead

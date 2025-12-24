import os
import json
import yaml
import shutil
from pathlib import Path
from typing import Dict, Any, Optional
import subprocess
import requests
from dataclasses import dataclass
import tempfile

@dataclass
class DeploymentConfig:
    platform: str  # huggingface, colab, local
    space_name: str
    space_visibility: str = "public"  # public, private
    hardware_tier: str = "cpu-basic"  # cpu-basic, cpu-upgraded, free-gpu, etc.
    environment_vars: Dict[str, str] = None
    requirements_file: str = "requirements.txt"
    python_version: str = "3.9"

class CloudDeployer:
    def __init__(self, huggingface_token: Optional[str] = None):
        self.huggingface_token = huggingface_token or os.getenv("HF_TOKEN")
        self.colab_ready = False
        self.temp_dir = Path(tempfile.mkdtemp(prefix="autodevcrew_deploy_"))
        
    def deploy_to_huggingface(self, config: DeploymentConfig) -> Dict[str, Any]:
        """Deploy AutoDevCrew to HuggingFace Spaces"""
        
        print(f"🚀 Deploying to HuggingFace Space: {config.space_name}")
        
        # Create space directory structure
        space_dir = self.temp_dir / "huggingface_space"
        space_dir.mkdir(exist_ok=True)
        
        # Copy necessary files
        self._prepare_huggingface_files(space_dir, config)
        
        # Create app.py for HuggingFace
        self._create_huggingface_app(space_dir, config)
        
        # Create README
        self._create_huggingface_readme(space_dir, config)
        
        # Create requirements.txt
        self._create_requirements_file(space_dir, config)
        
        # Create Dockerfile if needed
        if config.hardware_tier != "cpu-basic":
            self._create_huggingface_dockerfile(space_dir, config)
        
        # Push to HuggingFace
        if self.huggingface_token:
            return self._push_to_huggingface(space_dir, config)
        else:
            print("⚠️ No HuggingFace token provided. Created local deployment package.")
            return {
                "status": "package_ready",
                "space_dir": str(space_dir),
                "next_steps": [
                    "1. Create a new Space at https://huggingface.co/spaces",
                    "2. Upload contents of the space_dir",
                    f"3. Set space visibility to {config.space_visibility}"
                ]
            }
    
    def _prepare_huggingface_files(self, space_dir: Path, config: DeploymentConfig):
        """Prepare files for HuggingFace deployment"""
        
        # Core files to include
        core_files = [
            "main.py",
            "requirements.txt",
            "config/development.yaml",
            "ui/streamlit_app.py",
            "agents/",
            "core/",
            "db/",
            "workflows/"
        ]
        
        # Copy files
        for file_path in core_files:
            src = Path(file_path)
            # Handle source relative to current working dir if not absolute
            if not src.is_absolute():
                src = Path.cwd() / src
                
            dst = space_dir / file_path
            
            if src.is_dir():
                shutil.copytree(src, dst, dirs_exist_ok=True)
            elif src.exists():
                # Ensure parent dir exists
                dst.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(src, dst)
            else:
                print(f"Warning: Source file/directory {file_path} not found for deployment.")

    def _create_huggingface_app(self, space_dir: Path, config: DeploymentConfig):
        """Create the app.py entry point for HuggingFace Spaces"""
        app_content = """import streamlit as st
import os
import sys

# Add current directory to path
sys.path.append(os.path.dirname(__file__))

# Import the actual app
from ui.streamlit_app import main

if __name__ == "__main__":
    # Ensure database is initialized
    from db.storage import init_db
    init_db()
    
    # Run the app
    # Note: Streamlit on HF Spaces usually runs via `streamlit run app.py`
    # But if importing, we need to make sure code handling is correct.
    # Often simpler to just execute the file.
    pass 
"""
        # Since we are using Streamlit, typically HF spaces configured as Streamlit SDK 
        # just run `app.py`. If our app is in ui/streamlit_app.py, we might just copy it or symlink it.
        # But let's write a redirection or similar.
        
        # Actually, let's just create a simple app.py that executes the ui/streamlit_app.py content
        with open(space_dir / "app.py", "w") as f:
            f.write("import os\n")
            f.write("import sys\n")
            f.write("import streamlit.web.cli as stcli\n\n")
            f.write("if __name__ == '__main__':\n")
            f.write("    sys.argv = ['streamlit', 'run', 'ui/streamlit_app.py']\n")
            f.write("    sys.exit(stcli.main())\n")

    def _create_huggingface_readme(self, space_dir: Path, config: DeploymentConfig):
        """Create README.md with YAML metadata for Spaces"""
        content = f"""---
title: {config.space_name}
emoji: 🤖
colorFrom: blue
colorTo: indigo
sdk: streamlit
sdk_version: 1.28.2
app_file: app.py
pinned: false
---

# AutoDevCrew

Automated Software Development Life Cycle with AI Agents.
"""
        with open(space_dir / "README.md", "w") as f:
            f.write(content)

    def _create_requirements_file(self, space_dir: Path, config: DeploymentConfig):
        """Create specific requirements.txt for deployment"""
        # We can copy the existing one or add to it
        req_path = space_dir / "requirements.txt"
        if not req_path.exists():
            with open(req_path, "w") as f:
                f.write("streamlit\n")
                f.write("langchain\n")
                f.write("openai\n")
                f.write("pydantic\n")

    def _create_huggingface_dockerfile(self, space_dir: Path, config: DeploymentConfig):
        """Create Dockerfile if custom environment needed"""
        dockerfile = f"""FROM python:{config.python_version}

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY . /code

CMD ["streamlit", "run", "app.py", "--server.port=7860", "--server.address=0.0.0.0"]
"""
        with open(space_dir / "Dockerfile", "w") as f:
            f.write(dockerfile)

    def _push_to_huggingface(self, space_dir: Path, config: DeploymentConfig) -> Dict[str, Any]:
        """Push to HuggingFace Hub"""
        try:
            from huggingface_hub import HfApi
            api = HfApi(token=self.huggingface_token)
            
            # Create repo if not exists
            repo_id = f"{api.whoami()['name']}/{config.space_name}"
            api.create_repo(repo_id=repo_id, repo_type="space", space_sdk="streamlit", exist_ok=True)
            
            # Upload folder
            api.upload_folder(
                folder_path=str(space_dir),
                repo_id=repo_id,
                repo_type="space"
            )
            
            return {
                "status": "success",
                "space_url": f"https://huggingface.co/spaces/{repo_id}",
                "repo_id": repo_id
            }
        except Exception as e:
            return {
                "status": "error",
                "error": str(e)
            }

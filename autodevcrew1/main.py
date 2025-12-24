import asyncio
import argparse
import sys
import os
import logging
import json
import yaml
from pathlib import Path
from typing import Optional, Dict, Any, List
import uvicorn
import signal

# Force UTF-8 encoding for Windows console
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

# Core imports
from core.privacy_manager import PrivacyManager, PrivacyLevel
from core.lightweight_mode import LightweightMode, HardwareProfile
from core.cloud_deployer import CloudDeployer, DeploymentConfig
from integrations.github_integration import GitHubIntegration
from db.storage import save_task, save_code, save_test_log, save_deployment_log, save_final_report, get_task_summary

# Agent imports
from agents.engineer_agent import generate_code
from agents.tester_agent import validate_code, generate_tests
from agents.devops_agent import build_and_deploy
from agents.summarizer_agent import summarize_task

# Advanced Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
    handlers=[
        logging.FileHandler("autodevcrew.log"),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger("AutoDevCrew")

class Message:
    """Communication unit between agents"""
    def __init__(self, sender: str, receiver: str, content: Any, msg_type: str = "data"):
        self.sender = sender
        self.receiver = receiver
        self.content = content
        self.msg_type = msg_type
        self.timestamp = Path().stat().st_mtime # Simple timestamp

class Orchestrator:
    """
    Coordination Layer: Enables message-based collaboration.
    Maintains the task execution chain: User -> Engineer -> Tester -> DevOps -> Summarizer -> User
    """
    def __init__(self, agents: Dict[str, Any]):
        self.agents = agents
        self.history: List[Message] = []

    def _add_to_history(self, sender, receiver, content):
        msg = Message(sender, receiver, content)
        self.history.append(msg)
        logger.info(f"Collaboration: {sender} -> {receiver} | Content Size: {len(str(content))}")

    async def execute(self, task_description: str, context: Dict[str, Any]) -> Dict[str, Any]:
        logger.info(f"🚀 Mission Started: {task_description[:50]}...")
        
        # 1. User -> Engineer
        self._add_to_history("User", "Engineer", task_description)
        code = await self.agents["engineer"].generate(task_description)
        
        # 2. Engineer -> Tester
        self._add_to_history("Engineer", "Tester", code)
        valid, report = await self.agents["tester"].validate(code)
        
        # 3. Tester -> DevOps
        self._add_to_history("Tester", "DevOps", report)
        deploy_status = "Waiting..."
        deploy_success = False
        
        if valid:
            deploy_success, deploy_status = await self.agents["devops"].deploy(code)
        else:
            deploy_status = "Blocked: Code Validation Failed"
        
        # 4. DevOps -> Summarizer
        self._add_to_history("DevOps", "Summarizer", deploy_status)
        summary = await self.agents["summarizer"].summarize(task_description, code, report, deploy_status)
        
        # 5. Summarizer -> User
        self._add_to_history("Summarizer", "User", summary)
        
        result = {
            "success": valid and deploy_success,
            "task": task_description,
            "generated_code": code,
            "test_report": report,
            "deployment_status": deploy_status,
            "summary": summary,
            "execution_time": 1.0,
            "history": [m.__dict__ for m in self.history]
        }
        
        return result

# Agent Wrappers
class BaseAgent:
    def __init__(self, name, config):
        self.name = name
        self.config = config
    def get_metrics(self): return {"status": "active", "load": "low"}

class EngineerAgent(BaseAgent):
    async def generate(self, prompt): return generate_code(prompt)

class TesterAgent(BaseAgent):
    async def validate(self, code): return validate_code(code)

class DevOpsAgent(BaseAgent):
    async def deploy(self, code): return build_and_deploy(code)

class SummarizerAgent(BaseAgent):
    async def summarize(self, task, code, report, deploy): return summarize_task(task, code, report, deploy)

class AutoDevCrew:
    def __init__(self, config_path: str = "config/development.yaml"):
        self.config = self._load_config(config_path)
        self.privacy_manager = PrivacyManager(
            privacy_level=PrivacyLevel(self.config.get("privacy_level", "strict"))
        )
        self.setup_agents()
        self.orchestrator = Orchestrator(self.agents)
        self.github = GitHubIntegration()
        
    def _load_config(self, path):
        if Path(path).exists():
            with open(path, 'r') as f:
                return yaml.safe_load(f)
        return {}

    def setup_agents(self):
        self.agents = {
            "engineer": EngineerAgent("Engineer", self.config),
            "tester": TesterAgent("Tester", self.config),
            "devops": DevOpsAgent("DevOps", self.config),
            "summarizer": SummarizerAgent("Summarizer", self.config)
        }

    async def process_task(self, task_description: str, **kwargs):
        # Memory Layer check/save (Persistence)
        task_id = save_task(task_description)
        
        try:
            result = await self.orchestrator.execute(task_description, kwargs)
            
            # Save artifacts to Memory Layer
            save_code(task_id, result["generated_code"])
            save_test_log(task_id, result["test_report"])
            save_deployment_log(task_id, result["deployment_status"])
            save_final_report(task_id, result["summary"])
            
            return result
        except Exception as e:
            logger.error(f"Execution Error: {e}")
            raise

    async def run_interactive_pro(self):
        print("\n" + "="*60)
        print("🤖 AutoDevCrew Pro - Industrial SDLC Automation")
        print("==========================" + "="*34)
        
        while True:
            print("\n📋 Main Menu:")
            print("1. 🚀 Single Task")
            print("2. 🗃️  Task History")
            print("3. 📊 System Diagnostics")
            print("4. ☁️  Cloud Deployment")
            print("5. 🔄 GitHub Integration")
            print("6. ⚙️  Privacy Status")
            print("7. 🚪 Exit")
            
            choice = input("\nChoice: ")
            
            if choice == "1":
                task = input("Enter task description: ")
                result = await self.process_task(task)
                print("\n" + "="*60)
                print(result['summary']['summary_report'])
                print("="*60)
                
            elif choice == "2":
                print("\n--- Recent Tasks ---")
                from db.storage import get_task_summary
                summary = get_task_summary()
                if summary:
                    for task_id, desc in summary.items():
                        print(f"ID {task_id}: {desc[:50]}...")
                else:
                    print("No tasks found in memory.")
                
            elif choice == "3":
                stats = self.get_system_stats()
                print(f"\nCPU Usage: {stats['cpu']}%")
                print(f"Memory Usage: {stats['memory']}%")
                print(f"Active Agents: {stats['agents']}")
                
            elif choice == "4":
                print("Initiating cloud deployment...")
                deployer = CloudDeployer()
                # Mock configuration
                print("Staging artifacts for HuggingFace...")
                
            elif choice == "5":
                print("Generating GitHub Actions workflow...")
                # Use integration
                self.github.generate_workflow(".github/workflows/autodevcrew.yml")
                print("Saved to .github/workflows/autodevcrew.yml")
                
            elif choice == "6":
                report = self.privacy_manager.generate_privacy_report()
                print(json.dumps(report, indent=2))
                
            elif choice == "7":
                print("Farewell, Engineer.")
                break

    def get_system_stats(self):
        import psutil
        return {
            "cpu": psutil.cpu_percent(),
            "memory": psutil.virtual_memory().percent,
            "agents": len(self.agents)
        }

async def main():
    parser = argparse.ArgumentParser(description="AutoDevCrew Pro - Industrial SDLC Automation")
    parser.add_argument("--mode", choices=["cli", "ui", "api", "deploy"], default="cli")
    parser.add_argument("--task", type=str, help="Single task to process")
    parser.add_argument("--project", type=str, help="Project name")
    parser.add_argument("--privacy", choices=["strict", "moderate", "open"], default="strict")
    parser.add_argument("--lightweight", action="store_true", help="Enable hardware optimization")
    args = parser.parse_args()

    app = AutoDevCrew()
    
    # Apply Privacy Level
    app.privacy_manager.privacy_level = PrivacyLevel(args.privacy)
    
    # Handle Hardware Optimization if requested
    if args.lightweight:
        optimizer = LightweightMode()
        profile = optimizer.detect_hardware()
        logger.info(f"Lightweight mode enabled: {profile}")

    if args.task:
        res = await app.process_task(args.task, project=args.project)
        print("\n" + "="*60)
        print(res['summary']['summary_report'])
        print("="*60)
        return

    if args.mode == "cli":
        await app.run_interactive_pro()
    elif args.mode == "ui":
        import subprocess
        logger.info("Launching Streamlit UI...")
        subprocess.run([sys.executable, "-m", "streamlit", "run", "ui/streamlit_app.py"])
    elif args.mode == "api":
        print("API mode ready on port 8000 (Simulated)")
    elif args.mode == "deploy":
        deployer = CloudDeployer()
        await deployer.deploy(DeploymentConfig(target="huggingface"))

if __name__ == "__main__":
    asyncio.run(main())

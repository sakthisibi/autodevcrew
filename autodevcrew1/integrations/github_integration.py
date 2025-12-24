import os
import yaml
import json
import base64
from pathlib import Path
from typing import Dict, Any, Optional, List
import requests
from datetime import datetime
import hmac
import hashlib

class GitHubIntegration:
    def __init__(self, github_token: Optional[str] = None, repo: Optional[str] = None):
        self.github_token = github_token or os.getenv("GITHUB_TOKEN")
        self.repo = repo or os.getenv("GITHUB_REPOSITORY")
        self.api_base = "https://api.github.com"
        self.headers = {
            "Authorization": f"token {self.github_token}",
            "Accept": "application/vnd.github.v3+json"
        }
    
    def create_actions_workflow(self, task_id: str, workflow_config: Dict[str, Any]) -> str:
        """Generate GitHub Actions workflow YAML"""
        
        workflow_name = f"autodevcrew-{task_id}"
        
        workflow = {
            "name": workflow_name,
            "on": {
                "workflow_dispatch": {
                    "inputs": {
                        "task_description": {
                            "description": "AutoDevCrew task description",
                            "required": True,
                            "type": "string"
                        },
                        "environment": {
                            "description": "Deployment environment",
                            "required": False,
                            "default": "development",
                            "type": "choice",
                            "options": ["development", "staging", "production"]
                        }
                    }
                },
                "push": {
                    "branches": ["main", "master"],
                    "paths": ["src/**", "requirements.txt"]
                },
                "pull_request": {
                    "branches": ["main", "master"]
                }
            },
            "jobs": {
                "autodevcrew-pipeline": {
                    "runs-on": "ubuntu-latest",
                    "strategy": {
                        "matrix": {
                            "python-version": ["3.9", "3.10", "3.11"]
                        }
                    },
                    "steps": [
                        {
                            "name": "Checkout repository",
                            "uses": "actions/checkout@v3"
                        },
                        {
                            "name": "Set up Python",
                            "uses": "actions/setup-python@v4",
                            "with": {
                                "python-version": "${{ matrix.python-version }}"
                            }
                        },
                        {
                            "name": "Install dependencies",
                            "run": "pip install -r requirements.txt"
                        },
                        {
                            "name": "Run AutoDevCrew",
                            "env": {
                                "GITHUB_TOKEN": "${{ secrets.GITHUB_TOKEN }}",
                                "TASK_DESCRIPTION": "${{ github.event.inputs.task_description }}",
                                "ENVIRONMENT": "${{ github.event.inputs.environment }}"
                            },
                            "run": """
                            python -c "
                            from main import AutoDevCrew
                            import asyncio
                            import os
                            
                            async def run():
                                autodevcrew = AutoDevCrew()
                                result = await autodevcrew.process_task(
                                    os.getenv('TASK_DESCRIPTION'),
                                    project_name='github-actions',
                                    priority='high'
                                )
                                return result
                            
                            result = asyncio.run(run())
                            print('Task completed:', result['success'])
                            "
                            """
                        },
                        {
                            "name": "Upload artifacts",
                            "uses": "actions/upload-artifact@v3",
                            "with": {
                                "name": "autodevcrew-output",
                                "path": "db/\ngenerated_code/\nreports/"
                            }
                        },
                        {
                            "name": "Create PR with generated code",
                            "if": "success()",
                            "run": """
                                git config --global user.name 'github-actions[bot]'
                                git config --global user.email 'github-actions[bot]@users.noreply.github.com'
                                git checkout -b feature/autodevcrew-${{ github.run_id }}
                                git add .
                                git commit -m "AutoDevCrew: Generated code for task"
                                git push origin feature/autodevcrew-${{ github.run_id }}
                                gh pr create --title "AutoDevCrew: Generated Implementation" --body "This PR contains code generated by AutoDevCrew"
                            """,
                            "env": {
                                "GITHUB_TOKEN": "${{ secrets.GITHUB_TOKEN }}"
                            }
                        }
                    ]
                },
                "deploy": {
                    "runs-on": "ubuntu-latest",
                    "needs": ["autodevcrew-pipeline"],
                    "if": "github.event.inputs.environment == 'production'",
                    "steps": [
                        {
                            "name": "Deploy to production",
                            "run": "echo 'Deploying generated code to production...'"
                        }
                    ]
                }
            }
        }
        
        # Add custom steps from config
        if workflow_config.get("additional_steps"):
            workflow["jobs"]["autodevcrew-pipeline"]["steps"].extend(
                workflow_config["additional_steps"]
            )
        
        return yaml.dump(workflow, default_flow_style=False)
    
    def trigger_real_ci_cd(self, task_description: str, branch: str = "main") -> Dict[str, Any]:
        """Trigger actual CI/CD pipeline through GitHub Actions"""
        
        if not self.github_token or not self.repo:
            return {"error": "GitHub token and repository not configured"}
        
        # Create workflow dispatch event
        url = f"{self.api_base}/repos/{self.repo}/actions/workflows/autodevcrew.yml/dispatches"
        
        payload = {
            "ref": branch,
            "inputs": {
                "task_description": task_description,
                "environment": "development"
            }
        }
        
        response = requests.post(url, headers=self.headers, json=payload)
        
        if response.status_code == 204:
            return {
                "success": True,
                "message": f"Triggered CI/CD pipeline for: {task_description[:50]}...",
                "repository": self.repo,
                "branch": branch
            }
        else:
            return {
                "success": False,
                "error": response.text,
                "status_code": response.status_code
            }
    
    def create_webhook(self, webhook_url: str, events: List[str] = None) -> Dict[str, Any]:
        """Create GitHub webhook for AutoDevCrew events"""
        
        events = events or ["push", "pull_request", "issues"]
        
        url = f"{self.api_base}/repos/{self.repo}/hooks"
        
        payload = {
            "name": "web",
            "active": True,
            "events": events,
            "config": {
                "url": webhook_url,
                "content_type": "json",
                "secret": os.urandom(32).hex()
            }
        }
        
        response = requests.post(url, headers=self.headers, json=payload)
        
        if response.status_code == 201:
            hook_data = response.json()
            return {
                "success": True,
                "webhook_id": hook_data["id"],
                "webhook_url": hook_data["config"]["url"],
                "secret": hook_data["config"]["secret"]
            }
        else:
            return {
                "success": False,
                "error": response.text
            }
    
    def process_webhook_event(self, payload: Dict[str, Any], signature: str, secret: str) -> Dict[str, Any]:
        """Process incoming GitHub webhook events"""
        
        # Verify signature
        expected_signature = hmac.new(
            secret.encode(),
            json.dumps(payload).encode(),
            hashlib.sha256
        ).hexdigest()
        
        if not hmac.compare_digest(f"sha256={expected_signature}", signature):
            return {"error": "Invalid signature"}
        
        event_type = payload.get("action", "unknown")
        
        if event_type == "opened" and "issue" in payload:
            # New issue opened - treat as task request
            issue = payload["issue"]
            return {
                "type": "new_issue",
                "task_description": issue["title"] + "\n" + issue["body"],
                "issue_number": issue["number"],
                "user": issue["user"]["login"]
            }
        
        elif event_type == "opened" and "pull_request" in payload:
            # New PR opened - could trigger code review
            pr = payload["pull_request"]
            return {
                "type": "new_pull_request",
                "title": pr["title"],
                "branch": pr["head"]["ref"],
                "user": pr["user"]["login"]
            }
        
        return {"type": event_type, "processed": True}
    
    def create_issue_from_task(self, task_result: Dict[str, Any]) -> Dict[str, Any]:
        """Create GitHub issue from AutoDevCrew task result"""
        
        url = f"{self.api_base}/repos/{self.repo}/issues"
        
        issue_body = f"""
## AutoDevCrew Task Result

**Task**: {task_result['task']}

### Results
- **Status**: {'✅ Success' if task_result['success'] else '❌ Failed'}
- **Execution Time**: {task_result['execution_time']:.2f}s
- **Code Quality**: {task_result.get('code_quality', 'N/A')}

### Generated Code
```python
{task_result.get('generated_code', '')[:1000]}...
```

### Test Results
- **Coverage**: {task_result.get('test_coverage', 'N/A')}%
- **Passed**: {task_result.get('tests_passed', 0)}
- **Failed**: {task_result.get('tests_failed', 0)}

### Next Steps
1. Review generated code
2. Run additional tests if needed
3. Merge if satisfactory
        """
        
        payload = {
            "title": f"AutoDevCrew: {task_result['task'][:50]}...",
            "body": issue_body,
            "labels": ["autodevcrew", "generated"]
        }
        
        response = requests.post(url, headers=self.headers, json=payload)
        
        if response.status_code == 201:
            issue_data = response.json()
            return {
                "success": True,
                "issue_url": issue_data["html_url"],
                "issue_number": issue_data["number"]
            }
        else:
            return {
                "success": False,
                "error": response.text
            }
    
    def generate_security_scan_workflow(self) -> str:
        """Generate security scanning workflow"""
        
        workflow = {
            "name": "Security Scan with AutoDevCrew",
            "on": ["push", "pull_request"],
            "jobs": {
                "security-scan": {
                    "runs-on": "ubuntu-latest",
                    "steps": [
                        {
                            "name": "Checkout code",
                            "uses": "actions/checkout@v3"
                        },
                        {
                            "name": "Run AutoDevCrew Security Scan",
                            "run": """
                                python -c "
                                from agents.tester_agent import TesterAgent
                                import os
                                
                                tester = TesterAgent()
                                
                                # Scan all Python files
                                import glob
                                security_issues = []
                                
                                for py_file in glob.glob('**/*.py', recursive=True):
                                    with open(py_file, 'r') as f:
                                        code = f.read()
                                    
                                    results = tester.run_security_tests(code)
                                    if results['failed'] > 0:
                                        security_issues.append({
                                            'file': py_file,
                                            'issues': results['detailed_report']
                                        })
                                
                                if security_issues:
                                    print('Security issues found:')
                                    for issue in security_issues:
                                        print(f'  - {issue[\"file\"]}: {len(issue[\"issues\"])} issues')
                                    exit(1)
                                else:
                                    print('✅ No security issues found')
                                "
                            """
                        }
                    ]
                }
            }
        }
        
        return yaml.dump(workflow, default_flow_style=False)
    def generate_workflow(self, output_path: str):
        """Generate a default AutoDevCrew workflow and save it to a file"""
        workflow_yaml = self.create_actions_workflow("main", {})
        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, 'w') as f:
            f.write(workflow_yaml)
        return str(path)

import subprocess
import tempfile
import os
import sys

def build_and_deploy(code):
    """DevOps Agent: CI/CD & Deployment Role"""
    # Create a temp file to run code/tests
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', prefix='exec_', delete=False) as f:
        f.write(code)
        temp_path = f.name
    
    output_log = []
    
    try:
        # 1. Run Tests
        output_log.append("--- Testing Phase ---")
        test_result = subprocess.run([sys.executable, '-m', 'pytest', temp_path], 
                                    capture_output=True, text=True)
        
        if test_result.returncode not in [0, 5]: 
            output_log.append(f"❌ Tests Failed:\n{test_result.stderr or test_result.stdout}")
            return False, "\n".join(output_log)
        
        output_log.append("✅ Tests Passed (or none found).")
        
        # 2. Capture Execution Output (if there's a __main__ block)
        output_log.append("\n--- Execution Phase ---")
        exec_result = subprocess.run([sys.executable, temp_path], 
                                    capture_output=True, text=True)
        
        if exec_result.stdout:
            output_log.append(f"STDOUT:\n{exec_result.stdout}")
        if exec_result.stderr:
            output_log.append(f"STDERR:\n{exec_result.stderr}")
            
        if not exec_result.stdout and not exec_result.stderr:
            output_log.append("ℹ️ Code executed with no direct output.")

        # Simulate deployment
        output_log.append("\n✅ Deployed to Virtual Environment!")
        return True, "\n".join(output_log)
        
    except Exception as e:
        return False, f"Deployment error: {str(e)}"
    finally:
        if os.path.exists(temp_path):
            os.unlink(temp_path)

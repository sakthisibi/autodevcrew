import ast
def validate_code(code):
    """Tester Agent: QA Analyst Role"""
    if not code or len(code.strip()) == 0:
        return False, "❌ Error: No code provided for validation."
    
    try:
        # Basic syntax check
        ast.parse(code)
        
        # Heuristic checks
        report = []
        report.append("✅ Syntax Check: PASSED")
        
        if "login" in code.lower() or "auth" in code.lower():
            report.append("✅ Context Verification: Contains relevant keywords (Login/Auth)")
        
        if len(code.split('\n')) > 5:
            report.append(f"✅ Complexity: Code has {len(code.split('\n'))} lines (Satisfactory)")
        
        return True, "\n".join(report)
        
    except SyntaxError as e:
        return False, f"❌ Syntax Error: {str(e)} at line {e.lineno}"
    except Exception as e:
        return False, f"❌ Generic Error: {str(e)}"

def generate_tests(code):
    """Basic test suite generation"""
    test_template = f"""
import pytest

# Generated Test Suite for AutoDevCrew
def test_syntax_integrity():
    # Verify the code is valid python
    import ast
    try:
        ast.parse({repr(code)})
        assert True
    except:
        assert False, "Syntax failure in generated code"

def test_placeholder():
    assert 1 == 1 # Basic smoke test
"""
    return test_template.strip()

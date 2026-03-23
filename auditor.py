import ast
from typing import List, Tuple

class AdversarialAuditor:
    def __init__(self):
        self.findings = []
    
    def scan_for_injection_vulnerabilities(self, source_code: str) -> List[str]:
        """Reviewer acts as Security Hacker to find 'Injection Vulnerabilities' in generated code"""
        vulnerabilities = []
        try:
            tree = ast.parse(source_code)
            for node in ast.walk(tree):
                if isinstance(node, ast.Call):
                    if isinstance(node.func, ast.Name):
                        if node.func.id in ['eval', 'exec']:
                            vulnerabilities.append(f"Found dynamic execution function: {node.func.id}")
                    elif isinstance(node.func, ast.Attribute):
                        if node.func.attr == 'execute' and isinstance(node.func.value, ast.Name) and "cursor" in node.func.value.id:
                            vulnerabilities.append("Found potential SQL execution without parameterization check.")
        except Exception as e:
            vulnerabilities.append(f"Failed to parse source code: {e}")
            
        # Simplistic checks for demonstration
        if "os.system" in source_code or "subprocess.Popen" in source_code:
             vulnerabilities.append("Found OS command injection vector candidates")
             
        self.findings.extend(vulnerabilities)
        return vulnerabilities

    def manual_mse_audit(self, predictions: List[float], actuals: List[float]) -> float:
        """Math Audit: Recalculate the Mean Squared Error (MSE) for a 3-point sample"""
        if len(predictions) != 3 or len(actuals) != 3:
            raise ValueError("Audit requires exactly a 3-point sample.")
        
        sum_squared_error = sum((p - a) ** 2 for p, a in zip(predictions, actuals))
        mse = sum_squared_error / 3.0
        
        # Fail Condition
        if mse == 0.0:
            raise ValueError("Synthetically Manipulated Data Detected: MSE is 0 (impossible for live data).")
            
        return mse

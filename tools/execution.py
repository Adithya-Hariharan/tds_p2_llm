import sys
import subprocess

def python_repl(code: str) -> str:
    """
    Executes Python code in a subprocess.
    Auto-injects imports for pandas, requests, and numpy to ensure robustness.
    """
    print("[Tool] Executing Python...")
    
    # Pre-load common libraries to prevent model errors
    prepend_imports = "import pandas as pd\nimport numpy as np\nimport requests\nimport json\nimport re\n"
    full_code = prepend_imports + code
    
    try:
        # Run the code safely in a subprocess
        result = subprocess.run(
            [sys.executable, "-c", full_code],
            capture_output=True, text=True, timeout=45
        )
        
        # Return stdout if successful, else stderr
        if result.returncode == 0:
            return f"STDOUT:\n{result.stdout}"
        else:
            return f"STDERR:\n{result.stderr}"
            
    except Exception as e:
        return f"Execution Error: {e}"
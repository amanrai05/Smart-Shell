import subprocess
import platform
import shlex

def execute_in_wsl(command: str) -> str:
    """Execute shell command safely in WSL or native Linux."""
    try:
        system = platform.system().lower()
        if "windows" in system:
            
            result = subprocess.run(command,shell=True, capture_output=True, text=True)
        else:
            
            result = subprocess.run(command,shell=True ,capture_output=True, text=True)

        if result.returncode == 0:
            return result.stdout.strip()
        else:
            return f"Error:\n{result.stderr.strip()}"
    except Exception as e:
        return f"Exception: {str(e)}"
from app.agents.installer_agent import InstallerAgent
from app.nlp_parser import get_bash_command
from app.safety_checker import is_safe_command
from app.executor import execute_in_wsl

installer = InstallerAgent()

def cli_interface(user_input):
    print("\n🧠 Interpreting your request...")

    
    if "install" in user_input.lower():
        words = user_input.lower().split()
        try:
            idx = words.index("install")
            package = words[idx + 1]
            print(f"\n⚙ Installing: {package}")
            installer.install_package(package)
            return
        except IndexError:
            print("❌ No package name found.")
            return

   
    bash_command = get_bash_command(user_input)
    print(f"\n⚙ Executing: {bash_command}")

    
    if not is_safe_command(bash_command):
        print("🚨 Unsafe command detected! Not executing.")
        return

    output = execute_in_wsl(bash_command)

    if output.strip():
        print(f"\n📤 Output:\n{output}")
    else:
        print("\n✅ Command executed successfully. (No output)")
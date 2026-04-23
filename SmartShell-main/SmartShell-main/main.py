import os
import sys
import subprocess
from app.cli import cli_interface
from app.agents.downloader_agent import DownloaderAgent
from app.executor import execute_in_wsl

def get_command_explanation(command):
    """Fetch the explanation of a Linux command using man."""
    try:
        result = subprocess.run(['wsl', 'man', command], capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            return result.stdout[:500]
        else:
            return f"Error retrieving manual page for {command}."
    except subprocess.TimeoutExpired:
        return f"Error: man {command} took too long to fetch."
    except Exception as e:
        return f"Error fetching manual page for {command}: {str(e)}"

def handle_prompt(user_input):
    if "what does" in user_input.lower():
        command = user_input.split(' ')[-2]
        return get_command_explanation(command)
    return None

def main():
    downloader = DownloaderAgent(download_dir="./downloads")

    print("\n🚀 Welcome to AI-Powered Linux Shell Assistant!")

    while True:
        print("\n Choose an option:")
        print("1. Manual input (Linux command or install package)")
        print("2. Voice input (download URL)")
        print("3. Resume a download")
        print("4. Exit")

        choice = input(" Enter your choice (1-4): ").strip()

        if choice == "1":
            user_input = input("\nEnter your Linux task (e.g., update packages, install git, list files): ").strip()

            if not user_input:
                print("❌ Input is empty.")
                continue

            
            cli_interface(user_input)

        elif choice == "2":
            downloader.handle(use_voice=True)

        elif choice == "3":
            url = input(" Enter the URL to resume download: ").strip()
            if url:
                print(downloader.download_with_resume(url))
            else:
                print("❌ No URL provided.")

        elif choice == "4":
            print("👋 Exiting the AI Shell Assistant. Goodbye!")
            break

        else:
            print("❌ Invalid choice. Please enter a number between 1 and 4.")

if __name__ == "__main__":
    main()
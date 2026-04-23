import re
import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3"

def get_bash_command(user_input):
    prompt = f"""
You are a Linux Bash expert.
Convert the following natural language request into a SAFE bash command.
Commands may be chained using '&&' if required.
ONLY return the bash command. Do not include explanations or backticks.

Request: {user_input}

Bash Command:"""

    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False
    }

    response = requests.post(OLLAMA_URL, json=payload)
    if response.status_code == 200:
        bash_command = response.json()['response'].strip()
        # ✅ This removes leading/trailing ` or ``` safely
        bash_command = re.sub(r'^`{1,3}|`{1,3}$', '', bash_command).strip()
        return bash_command
    else:
        raise Exception(f"Ollama Error: {response.text}")
def is_safe_command(command):
    
    dangerous_keywords = [
        "rm -rf", "mkfs", ":(){ :|:& };:", "dd if=", "shutdown", "reboot",
        "killall", "poweroff", "halt"
    ]
    
    for keyword in dangerous_keywords:
        if keyword in command:
            return False
    return True

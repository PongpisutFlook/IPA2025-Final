import subprocess

def showrun(ip):
    command = [
        'ansible-playbook',
        'showrun_playbook.yaml',
        '--extra-vars', f"target_ip={ip}"
    ]

    result = subprocess.run(command, capture_output=True, text=True)
    output = result.stdout

    if 'failed=0' in output and 'unreachable=0' in output:
        return 'ok'
    else:
        return f"Error: Ansible"

def motd(ip, message):
    try:
        message = message.replace("!", "\\!")
        command = [
            "ansible-playbook", 
            "motd_playbook.yaml",
            "-i", f"{ip},",
            "--extra-vars", f"motd_message=\"{message}\" ansible_user=admin ansible_password=cisco"
        ]
        result = subprocess.run(command, capture_output=True, text=True, timeout=60)

        if result.returncode == 0:
            return 'Ok: success'
        else:
            return f'Error: No success (code={result.returncode})'

    except Exception as e:
        return f"Error running Ansible: {e}"

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

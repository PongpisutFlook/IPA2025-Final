from netmiko import ConnectHandler
from pprint import pprint
import textfsm
import io
import re

username = "admin"
password = "cisco"

def gigabit_status(device_ip):
    ans = ""
    device_params = {
        "device_type": "cisco_ios",
        "ip": device_ip,
        "username": username,
        "password": password,
    }

    with ConnectHandler(**device_params) as ssh:
        up = 0
        down = 0
        admin_down = 0

        result = ssh.send_command("show ip interface brief", use_textfsm=True)
        status_list = []

        for status in result:
            intf = status.get("intf") or status.get("interface")
            if not intf:
                continue

            line_status = status.get("status", "").lower()

            if "gigabitethernet" in intf.lower():
                if line_status == "up":
                    up += 1
                elif line_status == "down":
                    down += 1
                elif line_status == "administratively down":
                    admin_down += 1

                status_list.append(f"{intf} {line_status}")

        ans = (
            ", ".join(status_list)
            + f" -> {up} up, {down} down, {admin_down} administratively down"
        )

        pprint(ans)
        return ans

def read_motd(ip):
    try:
        device = {
            "device_type": "cisco_ios",
            "host": ip,
            "username": "admin",
            "password": "cisco",
        }

        with ConnectHandler(**device) as conn:
            output = conn.send_command("show banner motd")

        motd_message = output.strip().replace("\\!", "!")

        if not motd_message:
            return f"Error: No MOTD Configured"
        
        return motd_message

    except Exception as e:
        return f"Error reading MOTD from {ip}: {e}"

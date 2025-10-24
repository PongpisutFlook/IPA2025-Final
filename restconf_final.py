import json
import requests
requests.packages.urllib3.disable_warnings()

# RESTCONF base URL (IP จะถูกส่งเข้ามาแทน)
base_api_path = "/restconf/data/ietf-interfaces:interfaces"

headers = {
    "Accept": "application/yang-data+json",
    "Content-Type": "application/yang-data+json"
}

basicauth = ("admin", "cisco")


def create(ip, student_id):
    interface_name = f"Loopback{student_id}"
    interface_ip = f"172.1.{student_id[-2:]}.1"
    url = f"https://{ip}{base_api_path}/interface={interface_name}"

    resp = requests.get(url, auth=basicauth, headers=headers, verify=False)

    if resp.status_code == 200:
        return f"Cannot create: Interface loopback {student_id}"

    yangConfig = {
        "ietf-interfaces:interface": {
            "name": interface_name,
            "type": "iana-if-type:softwareLoopback",
            "enabled": True,
            "ietf-ip:ipv4": {
                "address": [
                    {"ip": interface_ip, "netmask": "255.255.255.0"}
                ]
            },
            "ietf-ip:ipv6": {}
        }
    }

    resp = requests.put(url, data=json.dumps(yangConfig), auth=basicauth, headers=headers, verify=False)

    if 200 <= resp.status_code <= 299:
        return f"Interface loopback {student_id} is created successfully using Restconf"
    else:
        return f"Cannot create: Interface loopback {student_id}"


def delete(ip, student_id):
    interface_name = f"Loopback{student_id}"
    url = f"https://{ip}{base_api_path}/interface={interface_name}"

    resp = requests.get(url, auth=basicauth, headers=headers, verify=False)

    if resp.status_code == 404:
        return f"Cannot delete: Interface loopback {student_id}"

    resp = requests.delete(url, auth=basicauth, headers=headers, verify=False)

    if 200 <= resp.status_code <= 299:
        return f"Interface loopback {student_id} is deleted successfully using Restconf"
    else:
        return f"Cannot delete: Interface loopback {student_id}"


def enable(ip, student_id):
    interface_name = f"Loopback{student_id}"
    url = f"https://{ip}{base_api_path}/interface={interface_name}"

    resp = requests.get(url, auth=basicauth, headers=headers, verify=False)

    if resp.status_code == 404:
        return f"Cannot enable: Interface loopback {student_id}"

    yangConfig = {
        "ietf-interfaces:interface": {
            "enabled": True
        }
    }

    resp = requests.patch(url, data=json.dumps(yangConfig), auth=basicauth, headers=headers, verify=False)

    if 200 <= resp.status_code <= 299:
        return f"Interface loopback {student_id} is enabled successfully using Restconf"
    else:
        return f"Cannot enable: Interface loopback {student_id}"


def disable(ip, student_id):
    interface_name = f"Loopback{student_id}"
    url = f"https://{ip}{base_api_path}/interface={interface_name}"

    resp = requests.get(url, auth=basicauth, headers=headers, verify=False)

    if resp.status_code == 404:
        return f"Cannot shutdown: Interface loopback {student_id}"

    yangConfig = {
        "ietf-interfaces:interface": {
            "enabled": False
        }
    }

    resp = requests.patch(url, data=json.dumps(yangConfig), auth=basicauth, headers=headers, verify=False)

    if 200 <= resp.status_code <= 299:
        return f"Interface loopback {student_id} is shutdowned successfully using Restconf"
    else:
        return f"Cannot shutdown: Interface loopback {student_id} (checked by Restconf)"


def status(ip, student_id):
    interface_name = f"Loopback{student_id}"
    url = f"https://{ip}{base_api_path}/interface={interface_name}"

    resp = requests.get(url, auth=basicauth, headers=headers, verify=False)

    if resp.status_code == 404:
        return f"No Interface loopback {student_id}"

    if 200 <= resp.status_code <= 299:
        response_json = resp.json()
        enabled_status = response_json["ietf-interfaces:interface"].get("enabled", None)

        if enabled_status is True:
            return f"Interface loopback {student_id} is enabled (checked by Restconf)"
        else:
            return f"Interface loopback {student_id} is disabled (checked by Restconf)"

    return f"Cannot determine status of loopback {student_id}"

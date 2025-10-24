import json
import requests
requests.packages.urllib3.disable_warnings()

# Router IP Address is 10.0.15.181-184
api_url = "https://10.0.15.62/restconf/data/ietf-interfaces:interfaces"

# the RESTCONF HTTP headers, including the Accept and Content-Type
# Two YANG data formats (JSON and XML) work with RESTCONF
headers = {
    "Accept": "application/yang-data+json",
    "Content-Type": "application/yang-data+json"
}

basicauth = ("admin", "cisco")

# Information me
student_id = "66070124"
interface_name = f"Loopback{student_id}"
ip_address = f"172.1.24.1"

url = f"{api_url}/interface={interface_name}"


def create():
    resp = requests.get(url, auth=basicauth, headers=headers, verify=False)

    if resp.status_code == 200:
        print(f"Cannot create: Interface {interface_name} already exists")
        return f"Cannot create: Interface loopback {student_id}"

    yangConfig = {
        "ietf-interfaces:interface": {
            "name": interface_name,
            "type": "iana-if-type:softwareLoopback",
            "enabled": True,
            "ietf-ip:ipv4": {
                "address": [
                    {"ip": ip_address, "netmask": "255.255.255.0"}
                ]
            },
            "ietf-ip:ipv6": {}
        }
    }

    resp = requests.put(
        url,
        data=json.dumps(yangConfig),
        auth=basicauth,
        headers=headers,
        verify=False
    )

    if 200 <= resp.status_code <= 299:
        print("STATUS OK:", resp.status_code)
        return f"Interface loopback {student_id} is created successfully"
    else:
        print("Error. Status Code:", resp.status_code)
        print(resp.text)
        return f"Error creating {interface_name}"


def delete():
    resp = requests.get(url, auth=basicauth, headers=headers, verify=False)

    if resp.status_code == 404:
        print(f"Cannot delete: Interface loopback {student_id} does not exist")
        return f"Cannot delete: Interface loopback {student_id}"

    elif resp.status_code != 200:
        print(f"Error checking interface: {resp.status_code}")
        return f"Error checking interface: {resp.status_code}"

    resp = requests.delete(
        url,
        auth=basicauth,
        headers=headers,
        verify=False
    )

    if 200 <= resp.status_code <= 299:
        print("STATUS OK:", resp.status_code)
        return f"Interface loopback {student_id} is deleted successfully"
    else:
        print("Error. Status Code:", resp.status_code)
        return f"Error deleting {interface_name}"


def enable():
    resp = requests.get(url, auth=basicauth, headers=headers, verify=False)

    if resp.status_code == 404:
        print(f"Cannot enable: Interface {interface_name} does not exist")
        return f"Cannot enable: Interface loopback {student_id}"
    elif resp.status_code != 200:
        print(f"Error checking interface: {resp.status_code}")
        return f"Error checking interface: {resp.status_code}"

    yangConfig = {
        "ietf-interfaces:interface": {
            "enabled": True
        }
    }

    resp = requests.patch(
        url,
        data=json.dumps(yangConfig),
        auth=basicauth,
        headers=headers,
        verify=False
    )

    if 200 <= resp.status_code <= 299:
        print("STATUS OK:", resp.status_code)
        return f"Interface loopback {student_id} is enabled successfully"
    else:
        print("Error. Status Code:", resp.status_code)
        print(resp.text)
        return f"Error enabling {interface_name}"

def disable():
    resp_check = requests.get(url, auth=basicauth, headers=headers, verify=False)
    if resp_check.status_code == 404:
        print(f"Cannot disable: Interface {interface_name} not found")
        return f"Cannot disable: Interface loopback {student_id}"

    yangConfig = {
        "ietf-interfaces:interface": {
            "enabled": False
        }
    }

    resp = requests.patch(
        url,
        data=json.dumps(yangConfig),
        auth=basicauth,
        headers=headers,
        verify=False
    )

    if 200 <= resp.status_code <= 299:
        print("STATUS OK:", resp.status_code)
        return f"Interface loopback {student_id} is disabled successfully"
    else:
        print("Error. Status Code:", resp.status_code)
        print(resp.text)
        return f"Error disabling interface {interface_name}"

def status():
    resp = requests.get(url, auth=basicauth, headers=headers, verify=False)

    if 200 <= resp.status_code <= 299:
        print("STATUS OK:", resp.status_code)
        response_json = resp.json()
        print(json.dumps(response_json, indent=2))

        interface_data = response_json["ietf-interfaces:interface"]

        if isinstance(interface_data, list):
            interface_info = interface_data[0]
        else:
            interface_info = interface_data

        enabled_status = interface_info.get("enabled", None)

        if enabled_status is True:
            return f"Interface loopback {student_id} is enabled"
        elif enabled_status is False:
            return f"Interface loopback {student_id} is disabled"
        else:
            return f"Cannot determine status of loopback {student_id}"

    elif resp.status_code == 404:
        print("STATUS NOT FOUND:", resp.status_code)
        return f"No Interface loopback {student_id}"

    else:
        print("Error. Status Code:", resp.status_code)
        print(resp.text)
        return f"Error checking status of loopback {student_id}"
from ncclient import manager
import xmltodict

def connect(ip):
    return manager.connect(
        host=ip,
        port=830,
        username="admin",
        password="cisco",
        hostkey_verify=False
    )

def create(ip, student_id):
    interface_name = f"Loopback{student_id}"
    interface_ip = f"172.1.{student_id[-2:]}.1"
    netconf_config = f"""
    <config>
      <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
        <interface>
          <name>{interface_name}</name>
          <description>Created by NETCONF</description>
          <type xmlns:ianaift="urn:ietf:params:xml:ns:yang:iana-if-type">ianaift:softwareLoopback</type>
          <enabled>true</enabled>
          <ipv4 xmlns="urn:ietf:params:xml:ns:yang:ietf-ip">
            <address>
              <ip>{interface_ip}</ip>
              <netmask>255.255.255.0</netmask>
            </address>
          </ipv4>
        </interface>
      </interfaces>
    </config>
    """

    try:
        with connect(ip) as m:
            reply = m.edit_config(target="running", config=netconf_config)
            if "<ok/>" in reply.xml:
                return f"Interface loopback {student_id} is created successfully using Netconf"
            else:
                return f"Cannot create: Interface loopback {student_id}"
    except Exception as e:
        return f"Cannot create: Interface loopback {student_id} ({e})"


def delete(ip, student_id):
    interface_name = f"Loopback{student_id}"
    netconf_config = f"""
    <config>
      <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
        <interface operation="delete">
          <name>{interface_name}</name>
        </interface>
      </interfaces>
    </config>
    """

    try:
        with connect(ip) as m:
            reply = m.edit_config(target="running", config=netconf_config)
            if "<ok/>" in reply.xml:
                return f"Interface loopback {student_id} is deleted successfully using Netconf"
            else:
                return f"Cannot delete: Interface loopback {student_id}"
    except Exception as e:
        return f"Cannot delete: Interface loopback {student_id} ({e})"


def enable(ip, student_id):
    interface_name = f"Loopback{student_id}"
    netconf_config = f"""
    <config>
      <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
        <interface>
          <name>{interface_name}</name>
          <enabled>true</enabled>
        </interface>
      </interfaces>
    </config>
    """

    try:
        with connect(ip) as m:
            reply = m.edit_config(target="running", config=netconf_config)
            if "<ok/>" in reply.xml:
                return f"Interface loopback {student_id} is enabled successfully using Netconf"
            else:
                return f"Cannot enable: Interface loopback {student_id}"
    except Exception as e:
        return f"Cannot enable: Interface loopback {student_id} ({e})"


def disable(ip, student_id):
    interface_name = f"Loopback{student_id}"
    netconf_config = f"""
    <config>
      <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
        <interface>
          <name>{interface_name}</name>
          <enabled>false</enabled>
        </interface>
      </interfaces>
    </config>
    """

    try:
        with connect(ip) as m:
            reply = m.edit_config(target="running", config=netconf_config)
            if "<ok/>" in reply.xml:
                return f"Interface loopback {student_id} is shutdowned successfully using Netconf"
            else:
                return f"Cannot shutdown: Interface loopback {student_id} (checked by Netconf)"
    except Exception as e:
        return f"Cannot shutdown: Interface loopback {student_id} (checked by Netconf)"


def status(ip, student_id):
    interface_name = f"Loopback{student_id}"
    netconf_filter = f"""
    <filter>
      <interfaces-state xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
        <interface>
          <name>{interface_name}</name>
        </interface>
      </interfaces-state>
    </filter>
    """

    try:
        with connect(ip) as m:
            reply = m.get(filter=netconf_filter)
            data_dict = xmltodict.parse(reply.xml)

            data_section = data_dict.get("rpc-reply", {}).get("data", {})
            if not data_section or "interfaces-state" not in data_section:
                return f"No Interface loopback {student_id}"

            iface_data = data_section["interfaces-state"].get("interface", None)
            if not iface_data:
                return f"No Interface loopback {student_id}"

            admin_status = iface_data.get("admin-status", "")
            oper_status = iface_data.get("oper-status", "")

            if admin_status == "up" and oper_status == "up":
                return f"Interface loopback {student_id} is enabled (checked by Netconf)"
            elif admin_status == "down" and oper_status == "down":
                return f"Interface loopback {student_id} is disabled (checked by Netconf)"

    except Exception as e:
        return f"Cannot determine status of loopback {student_id} ({e})"
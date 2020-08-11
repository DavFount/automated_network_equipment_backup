import json
import platform
import subprocess

from pathlib import Path

from netmiko import ConnectHandler
from netmiko.ssh_exception import NetMikoTimeoutException, AuthenticationException
from paramiko.ssh_exception import SSHException

with open("config.json") as config_file:
    config = json.load(config_file)


def ping(host):
    """
    Returns True if host (str) responds to a ping request.
    Remember that a host may not respond to a ping (ICMP) request even if the host name is valid.
    """
    param = "-n" if platform.system().lower() == "windows" else "-c"
    command = ["ping", param, "1", host]

    return (
        subprocess.call(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        == 0
    )


def create_config_backup(hostname, username, password, ip, device_type, backup_count):
    """
    Generates a backup of the running configuration for a given network device. Automatically overwrites existing backups.
    """
    path = Path(config['path_to_backup']) / f'{hostname}-{backup_count}.txt'
    hp_procurve = {
        "device_type": device_type,
        "host": ip,
        "username": username,
        "password": password,
    }
    try:
        net_connect = ConnectHandler(**hp_procurve)
        output = net_connect.send_command("show run")
        path.write_text(output)
    except (AuthenticationException):
        path.write_text(f"Authentication Failure: {hostname}")
    except (NetMikoTimeoutException):
        path.write_text(f"Timeout to device: {hostname}")
    except (SSHException):
        path.write_text(f"SSH not enabled: {hostname}")

# Create Path object for the backup counter file
backup_count_path = Path(config['backup_counter_file_path']) / config['backup_counter_file']

# Set the backup count to the number in the file if the file doesn't exist set to 1
backup_num = int(backup_count_path.read_text()) if backup_count_path.exists() else 1

# Loop through the Devices Array in Config
count = 0
for device in config["devices"]:
    # print(f"\rCurrent Device: {device['hostname']}'\nIP: {device['ip']}\nType: {device['type']}\nBackup Num: {backup_num}\n\n", end="", flush=True)
    percentage = (count / len(config["devices"]))*100
    print("\rBacking Up Configs for %s"%device['hostname'], end="", flush=True)

    if not ping(device['ip']):
        continue
    create_config_backup(device['hostname'], device['username'], device['password'], device['ip'], device['type'], backup_num)
    count += 1

# Determin the next backup count
next_backup = backup_num + 1 if backup_num < config["backup_count"] else 1
# Write the new backup count
backup_count_path.write_text(str(next_backup))

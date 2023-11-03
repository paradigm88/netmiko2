from netmiko import ConnectHandler
import time
import sys
import os
from datetime import datetime

if len(sys.argv) != 5:
    print("Usage: python script.py <devices_file> <commands_file> <username> <password>")
    sys.exit(1)

devices_file = sys.argv[1]
commands_file = sys.argv[2]
username = sys.argv[3]
password = sys.argv[4]


# Define a function to connect to a device and run commands
def run_commands(device, commands, username, password, filename):
    try:
        # Establish an SSH connection to the device
        connection = ConnectHandler(**device)
        with open(filename, 'w') as f:
            # Loop over the commands
            for command in commands:
                # Get the prompt
                prompt = connection.find_prompt()   # Print the prompt, the command, and the output
                output = connection.send_command(command)   # Send the command to the device
                f.write(prompt)
                f.write(command)
                f.write("\n")
                f.write(output)
                f.write("\n")
                print(f"\t{prompt}{command}")
            #Close the connection
            connection.disconnect()
            os.chmod(filename, 0o755)

    except Exception as e:
        print(f"Failed to run commands on {device['ip']}: {e}")

# Read the devices file
try:
    with open(devices_file, 'r') as f:
        devices = f.read().splitlines()
except Exception as e:
    print(f"Failed to read devices file: {e}")
    devices = []

# Read the commands file
try:
    with open(commands_file, 'r') as f:
        commands = f.read().splitlines()
except Exception as e:
    print(f"Failed to read commands file: {e}")
    commands = []

date_folder = datetime.now().strftime("%Y%m%d")
backup_dir = "/nit/website/network_backups"
if not os.path.exists(backup_dir):
    os.makedirs(backup_dir, mode=0o755)
folder_path = os.path.join(backup_dir, date_folder)
if not os.path.exists(folder_path):
    os.makedirs(folder_path, mode=0o755)

# Loop over the devices
for device_info in devices:
    # Split the device info into parts
    device_name, device_type, ip, version, controller = device_info.split()

    # Define the device
    device = {
        'device_type': device_type,
        'ip': ip,
        'username': username,
        'password': password,
    }

    # Run the commands on the device
    filename = os.path.join(folder_path, f"{device_name}.txt")
    print(f"Connecting to {device_name} ...")
    run_commands(device, commands, username, password, filename)

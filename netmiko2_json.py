from netmiko import ConnectHandler
import json
import time
import sys
import os
from datetime import datetime

def run_commands(device, commands, username, password, filename):
    # create ssh connection
    connection = ConnectHandler(device_type=device['device_type'], ip=device['ip'], username=username, password=password)
    print(f"\n{'#' * 10} Device name : {device['device_name']} {'#' * 10}")
    
    output_data = {'device_name': device['device_name'], 'commands': []}
    
    # run commands and save the output in JSON format
    for command in commands:
        print(f"{'#' * 10} {device['device_name']}#{command} {'#' * 10} ")
        command_output = {'command': command, 'output': ''}
        
        command_output['output'] = connection.send_command(command)
        output_data['commands'].append(command_output)
    
    connection.disconnect()
    
    # Save the output as JSON
    with open(filename, 'w') as json_file:
        json.dump(output_data, json_file, indent=4)
    
    os.chmod(filename, 0o755)

if len(sys.argv) != 5:
    print("Usage: python script.py <devices_file> <commands_file> <username> <password>")
    sys.exit()
	
devices_file, commands_file, username, password = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]

with open(devices_file, 'r') as f:
    devices = [{'device_name': device.strip().split()[0], 'device_type': device.strip().split()[1], 'ip': device.strip().split()[2]} for device in f.readlines()]

with open(commands_file, 'r') as f:
    commands = [command.strip() for command in f.readlines()]

date_folder = datetime.now().strftime("%Y%m%d")
backup_dir = "/var/network_backups"
if not os.path.exists(backup_dir):
    os.makedirs(backup_dir, mode=0o755)
folder_path = os.path.join(backup_dir, date_folder)
if not os.path.exists(folder_path):
    os.makedirs(folder_path, mode=0o755)

for device in devices:
    filename = os.path.join(folder_path, f"{device['device_name']}.txt")
    run_commands(device, commands, username, password, filename)

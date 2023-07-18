#/bin/sh

cd /home/domain/user/work/collect_configs/

bin/python -u netmiko2.py devices_file_ios commands_file_ios user pass
bin/python -u netmiko2.py devices_file_nxos commands_file_nxos user pass
bin/python -u netmiko2.py devices_file_asa commands_file_asa user pass

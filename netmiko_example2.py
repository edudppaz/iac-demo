from netmiko import ConnectHandler
import json

devices = [
    {
        "device_type": "cisco_ios",
        "host": "192.168.86.29",
        "username": "cisco",
        "password": 'cisco'
    }
]
command = "show ip int brief"
for d in devices:
    with ConnectHandler(**d) as net_connect:
        output = net_connect.send_command(command, use_genie=True)
print(json.dumps(output, indent=4))

for k,v in output.items():
    for a,v in v.items():
        print(a)
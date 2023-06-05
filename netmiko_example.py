from netmiko import ConnectHandler

devices = [
    {
        "device_type": "cisco_ios",
        "host": "192.168.86.29",
        "username": "cisco",
        "password": 'cisco',
    }
]
command = "show ip int brief"
for d in devices:
    with ConnectHandler(**d) as net_connect:
        output = net_connect.send_command(command)
print(output)
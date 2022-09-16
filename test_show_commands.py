from modules.RTR import RTR
from getpass import getpass
import json

user = 'sa'
ip = '172.30.100.31'
password = getpass(prompt='Password: ', stream=None)
rtr = RTR(ip, user, password)

data = rtr.get_all_commands()
with open('test_routes.txt', 'w') as f:
    json.dump(data, f, indent=4)

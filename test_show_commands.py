from modules.RTR import RTR
from getpass import getpass
import json

user = 'sa'
ip = '172.30.100.31'
password = getpass(prompt='Password: ', stream=None)
rtr = RTR(ip, user, password)

data = rtr.get_routes()
data_vrf = rtr.get_routes(vrf='4G')
data_arp = rtr.get_arp()
data.append(data_vrf)
data.append(data_arp)
with open('test_routes.txt', 'w') as f:
    json.dump(data, f, indent=4)
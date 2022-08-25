import netmiko


class RTR:
    TEMPLATES = {
        'brief': 'modules/cisco_xr_show_interface_brief.textfsm',
        'route': 'modules/cisco_xr_show_ip_route.textfsm',
        'arp': 'modules/cisco_xr_show_arp.textfsm'
    }

    def __init__(self, ip, user, password):
        rtr_dict = {
            'device_type': 'cisco_xr',
            'host': ip,
            'username': user,
            'password': password,
            'secret': password
        }
        self.ssh = netmiko.ConnectHandler(**rtr_dict)

    def get_routes(self, vrf: str = '') -> list:
        command = 'show route '
        if vrf:
            command += f'vrf {vrf}'
        cli_list = self.ssh.send_command(command, use_textfsm=True, textfsm_template=RTR.TEMPLATES['route'])
        return cli_list

    def get_int_brief(self) -> list:
        command = 'show ipv4 interface brief'
        cli_list = self.ssh.send_command(command, use_textfsm=True, textfsm_template=RTR.TEMPLATES['brief'])
        return cli_list

    def get_arp(self) -> list:
        command = 'show arp vrf all'
        cli_list = self.ssh.send_command(command, use_textfsm=True, textfsm_template=RTR.TEMPLATES['arp'])
        return cli_list

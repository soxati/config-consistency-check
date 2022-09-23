import netmiko


class RTR:
    TEMPLATES = {
        'arp': 'modules/cisco_xr_show_arp.textfsm',
        'evpn': 'modules/cisco_xr_show_evpn_evi.textfsm',
        'brief': 'modules/cisco_xr_show_interface_brief.textfsm',
        'desc': 'modules/cisco_xr_show_interface_description.textfsm',
        'route': 'modules/cisco_xr_show_ip_route.textfsm',
        'bd': 'modules/cisco_xr_show_l2vpn_bridge.textfsm',
        'vrf_policy': 'modules/cisco_xr_show_run_vrf_policy.textfsm',
        'vrf': 'modules/cisco_xr_show_vrf.textfsm',
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
        self.hostname = self.ssh.find_prompt()[:-1]

    def get_arp(self) -> list:
        command = 'show arp vrf all'
        cli_list = self.ssh.send_command(command, use_textfsm=True, textfsm_template=RTR.TEMPLATES['arp'])
        return cli_list

    def get_evpn(self) -> list:
        command = 'show evpn evi'
        cli_list = self.ssh.send_command(command, use_textfsm=True, textfsm_template=RTR.TEMPLATES['evpn'])
        return cli_list

    def get_int_brief(self) -> list:
        command = 'show ipv4 interface brief | i "(Loopback|TenGigE|FortyGigE|GigabitEthernet|HundredGigE' \
                  '|BVI|Bundle-Ether)[0-9.]+ "'
        cli_list = self.ssh.send_command(command, use_textfsm=True, textfsm_template=RTR.TEMPLATES['brief'])
        return cli_list

    def get_int_desc(self) -> list:
        command = 'show int desc | i "(Fo|Te|Gi|Hu|BE|Lo|BV)[0-9.]+ "'
        cli_list = self.ssh.send_command(command, use_textfsm=True, textfsm_template=RTR.TEMPLATES['desc'])
        return cli_list

    def get_routes(self, vrf: str = '') -> list:
        command = 'show route '
        if vrf:
            command += f'vrf {vrf}'
        cli_list = self.ssh.send_command(command, use_textfsm=True, textfsm_template=RTR.TEMPLATES['route'])
        return cli_list

    def get_l2vpn_bd(self) -> list:
        command = 'show l2vpn bridge-domain detail | i "bridge-domain:|evi:|AC:" '
        cli_list = self.ssh.send_command(command, use_textfsm=True, textfsm_template=RTR.TEMPLATES['bd'])
        return cli_list

    def get_vrf_policy(self) -> list:
        command = 'show run formal vrf | i "policy"'
        cli_list = self.ssh.send_command(command, use_textfsm=True, textfsm_template=RTR.TEMPLATES['vrf_policy'])
        return cli_list

    def get_vrf(self) -> list:
        command = 'show vrf all'
        cli_list = self.ssh.send_command(command, use_textfsm=True, textfsm_template=RTR.TEMPLATES['vrf'])
        return cli_list

    def get_all_commands(self) -> dict:
        data = {'arp': self.get_arp(), 'evpn': self.get_evpn(), 'brief': self.get_int_brief(),
                'desc': self.get_int_desc(), 'route': self.get_routes(), 'bd': self.get_l2vpn_bd(),
                'vrf_policy': self.get_vrf_policy(), 'vrf': self.get_vrf()}
        return data

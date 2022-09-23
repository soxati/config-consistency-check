import json
import subprocess
import re
import platform
import sys

from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from getpass import getpass
from modules.RTR import RTR
from pathlib import Path

USERNAME = 'sa'
PASSWORD = getpass(prompt='Password: ', stream=None)
DEVICES = [x.strip() for x in Path('device_list.txt').open('r').read().splitlines()]

CONFIG_PATH = Path('configs/')
CONFIG_PATH.mkdir(exist_ok=True)
DATE = datetime.now().strftime('%Y%m%d_%H%M')
LOG_PATH = CONFIG_PATH / f'log_{DATE}.txt'
LOG_FILE = LOG_PATH.open('a')
SYSTEM = platform.system()


class UnknownOS(Exception):
    pass


class NoPing(Exception):
    pass


if SYSTEM not in ['Windows', 'Linux']:
    raise UnknownOS(SYSTEM)


def ping_host(ip, result=True):
    command = ['ping']
    ping_count = '3'
    if SYSTEM == 'Windows':
        command.extend(['-n', ping_count, '-w', '1', ip])
        reply_re = ", \w+ = [1-9]+, "
    elif SYSTEM == 'Linux':
        command.extend(['-c', ping_count, '-W', '1', ip])
        reply_re = ', [1-9]+ received,'
    ping_launcher = subprocess.Popen(command, stdout=subprocess.PIPE)
    out, err = ping_launcher.communicate()
    reply = out.decode(sys.stdin.encoding)
    if result:
        print(reply)
    if re.search(reply_re, reply):
        if SYSTEM == 'Windows' and 'unreachable' not in reply:
            return True
        elif SYSTEM == 'Linux':
            return True
    return False


def get_info(ip, user, password):
    print(f'Pinging {ip}...')
    if ping_host(ip):
        rtr = RTR(ip, user, password)
        print(f'Connected to {ip}')
        data = rtr.get_all_commands()
        print(f'Finished with {ip}', LOG_FILE)
        return rtr.hostname, data
    else:
        print(f'No ping reply from {ip}', LOG_FILE)
        raise NoPing


def main():
    with ThreadPoolExecutor(max_workers=20) as executor:
        threads = {executor.submit(get_info, ip, USERNAME, PASSWORD): ip for ip in DEVICES}

        for task in as_completed(threads):
            try:
                hostname, data = task.result()
                with (CONFIG_PATH / f'{hostname}_{DATE}.json').open('w') as f:
                    json.dump(data, f, indent=4)
            except NoPing:
                print(f'No ping from {threads[task]}')
            except Exception as e:
                print(f'Got an error {e} from {threads[task]}', LOG_FILE)

# Python3
# Menu experiment
# Goal is to have a YAML with regex patterns and scripts
# Currently has local variables retrieved from regex group names
# pip3 install pyyaml

import re
import os
import subprocess
import yaml

# use LibYAML or normal
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

# >- is not multiline, > is multiline, | is multiline with \n in them
rules = """
rules:
    pwd:
        match: ^pwd$
        desc: Print Working Directory
        Windows_NT: cd
        Linux: pwd
    info:
        match: ^info$
        desc: Info on the system
        Windows_NT: |
            cd
            whoami
            dir .
        Linux: |
            pwd
            whoami
            id
            ls -al
    id:
        match: ^id$
        desc: Id of user
        Windows_NT: whoami  # for windows
        Linux: id
    ls:
        match: ^ls$
        desc: Dir
        Windows_NT: dir
        Linux: ls -al
    ping:
        match: ^ping$
        desc: Ping
        Windows_NT: ping -n 1 127.0.0.1
        Linux: ping -c 1 127.0.0.1
    pingip:
        match: ^ping (?P<ip>[.0-9]*)$
        desc: Ping address
        Windows_NT: ping -n 1 {ip}
        Linux: ping -c 1 {ip}
"""
data = yaml.load(rules, Loader=Loader)
print(yaml.dump(data))

# env
#for k, v in os.environ.items():
#    print(f'{k}={v}')

shell = True
os_value = os.environ.get('OS')  # =Windows_NT
if os_value is None:
    os_value = 'Linux'
    shell = False
print("Using os_value", os_value, ", shell", shell)

while True:
    inp = input("> ")
    for r in data:
        for c in data[r]:
            for prop in data[r][c]:
                if prop == 'match':
                    m = re.match(data[r][c][prop], inp)
                    if m:
                        # print("G", m.groupdict())  # variable map
                        print("Description:", data[r][c]['desc'])

                        os_value_ = data[r][c][os_value].format_map(m.groupdict())
                        if '\n' in os_value_:
                            cmds = os_value_.split('\n')
                            for cmdr in cmds:
                                cmd = cmdr.strip().split(' ')
                                if len(cmd) == 1 and cmd[0] == '':  # improve
                                    continue
                                ex = subprocess.run(cmd, shell=shell)
                        else:
                            cmd = os_value_.split(' ')
                            ex = subprocess.run(cmd, shell=shell)

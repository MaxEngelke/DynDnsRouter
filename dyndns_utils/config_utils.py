import os
import subprocess
import ipaddress
import socket

def add_config_option_to_dict(configDict, line):
    res = line.split('=')
    if(len(res) >= 2):
        configDict[res[0]] = res[1].rstrip()


def read_config_file(file):
    if(os.path.isfile(file)):
        try:
            configDict = {}
            with open(file, 'r') as cf:
                line = cf.readline()
                if line.startswith('#') == False:
                    add_config_option_to_dict(configDict, line)

                while line:
                    line = cf.readline()
                    if line.startswith('#') == False:
                        add_config_option_to_dict(configDict, line)

            return configDict

        except Exception as e:
            print(e)
            return None
    else:
        return None

def get_ip_address_as_string():
    res = subprocess.Popen(["ip","addr"], stdout=subprocess.PIPE)
    res_com = res.communicate()
    res_com_lines = res_com[0].splitlines()
    ip = ''
    for line in res_com_lines:
        line_dec = line.decode()
        if line_dec.find('inet6') != -1 and line_dec.find('global') != -1:
            ip = line_dec.split()[1]
            pos_slash = ip.find('/')
            if pos_slash != 0:
                ip = ip[0:pos_slash]
            break
    return ip

def get_ip_version(ip):
    res = ipaddress.ip_address(ip)
    
    if res.version == 4:
        return socket.AF_INET
    elif res.version == 6:
        return socket.AF_INET6
    else:
        return None

def write_config_file(file, configDict):
    with open(file, 'w') as cf:
        for key, value in configDict.items():
            cf.write(key + '=' + value + '\n')
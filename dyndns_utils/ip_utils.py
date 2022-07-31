import subprocess
import ipaddress
import socket
import requests
import logging

def get_ip_address_as_string(ip_version: str = 'ipv6') -> str:
    if ip_version == 'ipv6':
        return get_ipv6_address_as_string()
    elif ip_version == 'ipv4':
        return get_ipv4_address_as_string()
    else:
       logging.error('The current_ip_version should be either ipv6 or ipv4')
       return None


def get_ipv6_address_as_string() -> str:
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


def get_ipv4_address_as_string() -> str:
    endpoint = 'https://ipinfo.io/json'
    response = requests.get(endpoint, verify = True)

    if response.status_code != 200:
        return None

    data = response.json()

    return data['ip']


def get_ip_version(ip: str) -> socket.AddressFamily:
    res = ipaddress.ip_address(ip) 
    
    if res.version == 4:
        return socket.AF_INET
    elif res.version == 6:
        return socket.AF_INET6
    else:
        return None



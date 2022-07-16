#!/usr/bin/env python3
import socket
import os
import logging

from dyndns_utils import crypto_utils
from dyndns_utils import config_utils

root_dir = os.path.dirname(__file__)
config_file = os.path.join(root_dir, 'client.cfg')
log_file = os.path.join(root_dir, 'DynDnsClientUpdate.log')

logging.basicConfig(filename=log_file, level=logging.DEBUG, format='%(asctime)s %(message)s')

def encode_message(config_dict, msg):
    pk = crypto_utils.read_public_key(config_dict['public_key'])
    return crypto_utils.get_encrypted_message(pk, msg)


def create_config_send_message(config_dict):
    msg = 'client=' + config_dict['client'] + ';'
    msg += 'current_ip=' + config_dict['current_ip'] + ';'
    msg += 'tunnel_ports_tcp=' + config_dict['tunnel_ports_tcp'] + ';'
    msg += 'tunnel_ports_udp=' + config_dict['tunnel_ports_udp'] + ';'
    msg += '#VALID'
    logging.info('Message send: ' + msg)
    return encode_message(config_dict, msg)

         
def send_data_to_server(config_dict):
    ip = config_dict['server_ip']
    c = (ip, int(config_dict['server_port']))
    s = socket.socket(config_utils.get_ip_version(ip), socket.SOCK_DGRAM, 0)
    s.sendto(create_config_send_message(config_dict), c)
    s.close()

def write_default_configfile():
    config_dict = {}
    config_dict['server_ip'] = ''
    config_dict['server_port'] = ''
    config_dict['client'] = ''
    config_dict['tunnel_ports_tcp'] = ''
    config_dict['tunnel_ports_udp'] = ''
    config_dict['current_ip'] = ''
    config_dict['public_key'] = ''
    config_utils.write_config_file(config_file, config_dict)

if(__name__ == "__main__"):
    config_dict = config_utils.read_config_file(config_file)
    if(config_dict):
        ip = config_utils.get_ip_address_as_string()
        if ip != config_dict['current_ip']:
            config_dict['current_ip'] = ip
            try:
                send_data_to_server(config_dict)
                config_utils.write_config_file(config_file, config_dict)
            except Exception as e:
                logging.error('Error: ' + str(e))
    else:
        logging.error('Error: No Configfile provided!')
        print('No configfile for the client provided. I will provide one for you!')

        

#!/usr/bin/env python3
import socket
import os
import logging

from dyndns_utils import crypto_utils
from dyndns_utils import config_utils
from dyndns_utils import client_utils

root_dir = os.path.dirname(__file__)
config_file = os.path.join(root_dir, 'server.cfg')
clients_dir = os.path.join(root_dir, 'clients')
log_file = os.path.join(root_dir, 'DynDnsServer.log')

logging.basicConfig(filename=log_file, level=logging.INFO, format='%(asctime)s %(message)s')


def decode_message(config_dict, msg):
    pk = crypto_utils.read_private_key(config_dict['private_key'], None)
    return crypto_utils.get_decrypted_message(msg, pk)


def process_message(msg, sender, config_dict):
    try:
        msg_decrypt = decode_message(config_dict, msg)
        client_utils.process_client_from_message(msg_decrypt, clients_dir)
        logging.info(f'Client ${sender} processed and saved...')
    except:
        logging.error('Message invalid...')


def run_server(config_dict):
    sock = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
    addr_info = ('::', int(config_dict['server_port']), 0, 0)
    sock.bind(addr_info)
    logging.info('Server listening...')
    while(True):
        msg, sender = sock.recvfrom(1024)
        process_message(msg, sender, config_dict)


if (__name__ == '__main__'):
    logging.info('Server starting...')  
    config_dict = config_utils.read_config_file(config_file)
    client_utils.init_clients(clients_dir)
    logging.info('Config loaded...')
    run_server(config_dict)
import os
import logging

from dyndns_utils import socat_utils
from dyndns_utils import config_utils

def init_clients(clients_dir):
    if os.path.isdir(clients_dir):
        files = os.listdir(clients_dir)
        for file in files:
            if file.endswith('.cl'):
                client_file_name = os.path.join(clients_dir, file)
                process_client_from_file(client_file_name)
    else:
        os.mkdir(clients_dir)


def get_port_pid_dict(pids_ports):
    
    if len(pids_ports) == 0:
        return None

    port_pid_dict = {}

    for p in pids_ports:

        port_pid = p.split(':')

        if len(port_pid) >= 2:
            port_pid_dict[port_pid[0]] = port_pid[1]

    return port_pid_dict
        

def get_client_dict_from_message(message):
  
    if not message:
        logging.error('Message is empty')
        return None

    if not message.endswith('#VALID'):
        logging.error('Message is invalid')
        return None

    msg_parts = message.split(';')

    client_dict = {}

    for part in msg_parts:
        key_val = part.split('=')

        if len(key_val) > 1:
            client_dict[key_val[0]] = key_val[1]

    return client_dict


def update_client_dict(update_client_dict, new_client_dict):
    for key, value in new_client_dict.items():
        update_client_dict[key] = value


def process_protocols(client_dict, protocols = ['tcp','udp']):

    for protocol in protocols:
        key = 'socat_pids_' + protocol
        if key in client_dict:
            current_protocol_pids = get_port_pid_dict(client_dict[key].split(','))
        else:
            current_protocol_pids = {}

        key = 'current_ip'
        if key in client_dict:
            process_ports(client_dict, current_protocol_pids, protocol)


def process_ports(client_dict, port_pid_dict, protocol):

    if (client_dict['tunnel_ports_' + protocol].find(',') != -1):
            new_port_list = client_dict['tunnel_ports_' + protocol].split(',')
    else:
        new_port_list = [ client_dict['tunnel_ports_' + protocol] ]

    for port_close in port_pid_dict.values():
        logging.info(f'Closing socate process ${port_close}')
        socat_utils.terminate_process(int(port_close))  

    active_ports = ''

    for ports in new_port_list:
        open_port = False
        src_dest_ports = ports.split('-')
        if(len(src_dest_ports) == 2):
            if port_pid_dict and ports in port_pid_dict:
                if socat_utils.is_socat_process_running(int(port_pid_dict[ports])) == False:
                    open_port = True

            else:
                open_port = True

            if open_port:
                pid, err = socat_utils.start_socat_process_ip_to_ipv6_tunnel(protocol, src_dest_ports[0],
                                                                        client_dict['current_ip'], src_dest_ports[1])

                if err is None:
                    active_ports += ports + ':' + str(pid) + ','
                    client_name = client_dict['client']
                    logging.info(f"Openend ports ${active_ports} for client ${client_name}")
                else:
                    logging.error(f"Error opening port on client ${client_dict}! ERR: ${err}")
            
    client_dict['socat_pids_' + protocol] = active_ports[:-1]
           

def process_client_from_message(message, clients_dir):

    client_dict_message = get_client_dict_from_message(message)

    client_name =  client_dict_message['client']
    client_file_name = os.path.join(clients_dir,  client_name + '.cl')

    if os.path.isfile(client_file_name):
        client_dict_file = config_utils.read_config_file(client_file_name)
        update_client_dict(client_dict_file, client_dict_message)
        client_dict = client_dict_file
    else:
        client_dict = client_dict_message

    process_protocols(client_dict)

    config_utils.write_config_file(client_file_name, client_dict)


def process_client_from_file(client_file_name):
    if os.path.isfile(client_file_name):
        client_dict = config_utils.read_config_file(client_file_name)
        process_protocols(client_dict)

    config_utils.write_config_file(client_file_name, client_dict)


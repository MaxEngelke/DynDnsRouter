import unittest
import os

from dyndns_utils import socat_utils
from dyndns_utils import config_utils
from dyndns_utils import client_utils

class TestClientUtils(unittest.TestCase):

    @classmethod
    def get_clients_dir(cls) -> str:
        root_dir = os.path.dirname(__file__)
        return os.path.join(root_dir, 'clients')

    @classmethod
    def setUpClass(cls):

        socat_utils.kill_all_socat_processes()

        clients_dir = cls.get_clients_dir()
        if os.path.isdir(clients_dir) == False:
            os.mkdir(clients_dir)

        test_client_file = os.path.join(clients_dir, 'test_client_1.cl')
        if os.path.isfile(test_client_file) == False:
            with open(test_client_file, 'w') as cf:
                cf.write('client=test_client_2\n')
                cf.write('current_ip=2a02:908:1b3:4fe0::d878\n')
                cf.write('tunnel_ports_tcp=80-80,12451-12656,100-200\n')
                cf.write('tunnel_ports_udp=40-20\n')
                cf.write('socat_pids_tcp=12451-12656:73085\n')
                cf.write('socat_pids_udp=\n')


    @classmethod
    def tearDownClass(cls):
        clients_dir = cls.get_clients_dir()
        if os.path.isdir(clients_dir):

            files = os.listdir(clients_dir)
            for file in files:
                os.remove(os.path.join(clients_dir, file))

            os.rmdir(clients_dir)

    
    def test_process_client_from_file(self):
        clients_dir = TestClientUtils.get_clients_dir()
        client_file_name = os.path.join(clients_dir, 'test_client_1.cl')

        client_utils.process_client_from_file(client_file_name)

        client_dict = config_utils.read_config_file(client_file_name)

        current_protocol_pids = client_utils.get_port_pid_dict(client_dict['socat_pids_tcp'].split(','))

        for pid in current_protocol_pids.values():
            self.assertTrue(socat_utils.is_socat_process_running(int(pid)))

        socat_utils.kill_all_socat_processes()


    def test_process_client_from_message_and_file(self):
        clients_dir = TestClientUtils.get_clients_dir()

        msg = 'client=test_client_2;current_ip=2a02:908:1b3:4fe0::d878;tunnel_ports_tcp=80-80,12451-12656,100-200;tunnel_ports_udp=40-20;#VALID'
        client_utils.process_client_from_message(msg, clients_dir)

        client_file_name = os.path.join(os.path.dirname(__file__), 'clients', 'test_client_2.cl')
        self.assertTrue(os.path.isfile(client_file_name))

        client_dict = config_utils.read_config_file(client_file_name)

        current_protocol_pids = client_utils.get_port_pid_dict(client_dict['socat_pids_tcp'].split(','))

        for pid in current_protocol_pids.values():
            self.assertTrue(socat_utils.is_socat_process_running(int(pid)))

        socat_utils.kill_all_socat_processes()


    def test_process_client_from_message(self):
        clients_dir = TestClientUtils.get_clients_dir()

        msg = 'client=test_client_3;current_ip=2a02:908:1b3:4fe0::d878;tunnel_ports_tcp=80-80,12451-12656,100-200;tunnel_ports_udp=40-20;#VALID'
        client_utils.process_client_from_message(msg, clients_dir)

        client_file_name = os.path.join(os.path.dirname(__file__), 'clients', 'test_client_3.cl')
        self.assertTrue(os.path.isfile(client_file_name))

        client_dict = config_utils.read_config_file(client_file_name)

        current_protocol_pids = client_utils.get_port_pid_dict(client_dict['socat_pids_tcp'].split(','))

        for pid in current_protocol_pids.values():
            self.assertTrue(socat_utils.is_socat_process_running(int(pid)))

        os.remove(os.path.join(clients_dir, 'test_client_3.cl'))
        socat_utils.kill_all_socat_processes()


    def test_change_clients_ip(self):

        msg = 'client=test_client_4;current_ip=2a02:908:1b3:4fe0::d878;tunnel_ports_tcp=50312-50312;tunnel_ports_udp=50313-50313;#VALID'
        client_dict = client_utils.get_client_dict_from_message(msg)

        client_utils.process_protocols(client_dict)

        self.assertTrue(client_dict['socat_pids_tcp'])
        self.assertTrue(client_dict['socat_pids_udp'])

        client_dict['current_ip'] = "2a02:908:1b3:4fe0::d876"

        client_utils.process_protocols(client_dict)


        self.assertTrue(client_dict['socat_pids_tcp'])
        self.assertTrue(client_dict['socat_pids_udp'])

        socat_utils.kill_all_socat_processes()


if(__name__ == '__main__'):
    unittest.main()
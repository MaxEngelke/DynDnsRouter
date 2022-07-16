from socket import socket
import unittest
import ipaddress
import socket
import os
from dyndns_utils import config_utils

class TestConfigUtils(unittest.TestCase):

    @classmethod
    def setUpClass(cls):

        root_dir = os.path.dirname(__file__)

        test_client_file = os.path.join(root_dir, 'client.cfg')
        if os.path.isfile(test_client_file) == False:
            with open(test_client_file, 'w') as cf:
                cf.write('client=test_client\n')
                cf.write('server_ip=::1\n')
                cf.write('server_port=1\n')
                cf.write('current_ip=::1\n')
                cf.write('tunnel_ports=12451-12656:73085\n')

    @classmethod
    def tearDownClass(cls):
        root_dir = os.path.dirname(__file__)
        if os.path.isdir(root_dir):

            files = os.listdir(root_dir)
            for file in files:
                if file.endswith('.cfg'):
                    os.remove(os.path.join(root_dir, file))


    def test_read_config(self):
        dir = os.path.dirname(__file__)
        conf = config_utils.read_config_file(os.path.join(dir, 'client.cfg'))
        self.assertIn("client", conf)
        self.assertIn("server_ip", conf)
        self.assertIn("server_port", conf)
        self.assertIn("current_ip", conf)
        self.assertIn("tunnel_ports", conf)


    def test_write_config(self):
        dir = os.path.dirname(__file__)
        conf = config_utils.read_config_file(os.path.join(dir, 'client.cfg'))
        testPort = "5625,80"
        conf["tunnel_ports"] = testPort
        config_utils.write_config_file(os.path.join(dir,'client_test.cfg'), conf)
        conf_test = config_utils.read_config_file(os.path.join(dir,'client_test.cfg'))
        self.assertEqual(conf_test['tunnel_ports'], testPort)


    def test_get_ip_addres(self):
        ip = ipaddress.ip_address(config_utils.get_ip_address_as_string())
        self.assertTrue(ip.is_global)

    def test_get_ip_version(self):
        self.assertEqual(socket.AF_INET, config_utils.get_ip_version('192.168.0.1'))
        self.assertEqual(socket.AF_INET6, config_utils.get_ip_version('::1'))


if(__name__ == '__main__'):
    unittest.main()
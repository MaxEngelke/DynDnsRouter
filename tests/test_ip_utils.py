import unittest
import ipaddress
import socket

from dyndns_utils import ip_utils

class TestIPUtils(unittest.TestCase):

    def test_get_ipv6_address(self):
        ip = ipaddress.ip_address(ip_utils.get_ip_address_as_string())
        self.assertTrue(ip.is_global)


    def test_get_ipv4_address(self):
        ip = ipaddress.ip_address(ip_utils.get_ip_address_as_string('ipv4'))
        self.assertTrue(ip.is_global)


    def test_get_ip_version(self):
        self.assertEqual(socket.AF_INET, ip_utils.get_ip_version('192.168.0.1'))
        self.assertEqual(socket.AF_INET6, ip_utils.get_ip_version('::1'))


if(__name__ == '__main__'):
    unittest.main()
import unittest

from dyndns_utils import socat_utils

class TestSocatUtils(unittest.TestCase):


    def test_start_and_stop_socat_processes(self):
        socat_utils.kill_all_socat_processes()

        pid1, err  = socat_utils.start_socat_process_ipv6_to_ipv6_tunnel('tcp', '56841', '::1', '63251')
        pid2, err  = socat_utils.start_socat_process_ipv4_to_ipv6_tunnel('tcp', '56842', '::1', '63252')
        pid3, err  = socat_utils.start_socat_process_ipv6_to_ipv6_tunnel('udp', '56843', '::1', '63253')
        pid4, err  = socat_utils.start_socat_process_ipv4_to_ipv6_tunnel('udp', '56844', '::1', '63254')
        pid5, err  = socat_utils.start_socat_process_ip_to_ipv6_tunnel('tcp', '56845', '::1', '63255')
        sp = socat_utils.get_socat_pids()

        self.assertEqual(len(sp), 5)
        self.assertIn(pid1, sp)
        self.assertIn(pid2, sp) 
        self.assertIn(pid3, sp)    
        self.assertIn(pid4, sp)  
        self.assertIn(pid5, sp)          

        socat_utils.kill_all_socat_processes()

        sp_after_terminate = socat_utils.get_socat_pids()
        self.assertEqual(len(sp_after_terminate), 0)


if(__name__ == '__main__'):
    unittest.main()


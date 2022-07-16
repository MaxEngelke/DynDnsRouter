from genericpath import isfile
import unittest
import os
from dyndns_utils import crypto_utils

class TestCryptoUtils(unittest.TestCase):


    @classmethod
    def get_certs_dir(cls) -> str:
        root_dir = os.path.dirname(__file__)
        return os.path.join(root_dir, 'certs')

    @classmethod
    def setUpClass(cls):

        certs_dir = cls.get_certs_dir()
        if os.path.isdir(certs_dir) == False:
            os.mkdir(certs_dir)

    @classmethod
    def tearDownClass(cls):
        certs_dir = cls.get_certs_dir()
        if os.path.isdir(certs_dir):

            files = os.listdir(certs_dir)
            for file in files:
                os.remove(os.path.join(certs_dir, file))

            os.rmdir(certs_dir)

    def test_create_key(self):
        private, public = crypto_utils.create_key(4096, 65537)

        self.assertIsNotNone(private)
        self.assertIsNotNone(public)


    def test_store_keys(self):
        private, public = crypto_utils.create_key(2048, 65537)

        certs_dir = TestCryptoUtils.get_certs_dir()

        private_key_file = os.path.join(certs_dir, 'test_private_key.pem')
        if (os.path.isfile(private_key_file)):
            os.remove(private_key_file)

        public_key_file = os.path.join(certs_dir, 'test_public_key.pem')
        if (os.path.isfile(public_key_file)):
            os.remove(public_key_file)

        crypto_utils.store_private_key(private, private_key_file)
        crypto_utils.store_public_key(public, public_key_file)

        self.assertTrue(os.path.isfile(private_key_file))
        self.assertTrue(os.path.isfile(public_key_file))


    def test_load_keys_and_decrypt_public_to_private(self):
        private, public = crypto_utils.create_key(2048, 65537)

        certs_dir = TestCryptoUtils.get_certs_dir()

        private_key_file = os.path.join(certs_dir,'test_load_private_key.pem')
        public_key_file = os.path.join(certs_dir,'test_load_public_key.pem')

        crypto_utils.store_private_key(private, private_key_file)
        crypto_utils.store_public_key(public, public_key_file)

        msg = 'testmessage'

        encrypted = crypto_utils.get_encrypted_message(public, msg)

        new_private_key = crypto_utils.read_private_key(private_key_file, None)

        self.assertEqual(msg, crypto_utils.get_decrypted_message(encrypted, new_private_key))


if(__name__ == '__main__'):
    unittest.main()
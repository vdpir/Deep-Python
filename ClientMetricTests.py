import unittest

from unittest.mock import patch
from solution import Client

class MyTestCase(unittest.TestCase):
    def mocked_init(self, server_ip, server_port, timeout=None):
        return

    @patch('solution.Client.__init__', mocked_init)
    def setUp(self):
        self.client = Client('127.0.0.1', 1001)

    #def test_something(self):
    #    self.assertEqual(True, False)

    def mocked_get_data(self):
        return 'ok\npalm.cpu 0.5 1150864248\npalm.cpu 2.0 1150864247\neardrum.cpu 3.0 1150864250\n\n'

    def mocked_set_data(self, string_to_write):
        return None

    @patch('solution.Client.send_data', mocked_set_data)
    @patch('solution.Client.get_data', mocked_get_data)
    def test_client_get(self):
        self.assertEqual(self.client.get('*'), {'palm.cpu': [(1150864247, 2.0), (1150864248, 0.5)], 'eardrum.cpu': [(1150864250, 3.0)]})





if __name__ == '__main__':
    unittest.main()

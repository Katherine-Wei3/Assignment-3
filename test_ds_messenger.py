from ds_messenger import DirectMessager
import unittest

class TestDSMessenger(unittest.TestCase):
    def __init__(self):
        self.ds_messenger = DirectMessager('127.0.0.1', 'username', 'password')
        self.assertEqual(self.ds_messenger, True)

    def test_send(self):
        self.assertEqual(self.ds_messenger.send('message', 'friend'), True)

    def test_retrieve_new(self):
        self.assertEqual(self.ds_messenger.retrieve_new, )
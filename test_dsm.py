from ds_messenger import DirectMessenger
import unittest
from collections import namedtuple

Message = namedtuple('Message', ['message', 'direction', 'name', 'timestamp'])

class TestDSMessenger(unittest.TestCase):
    def setUp(self):
        self.dm = DirectMessenger('127.0.0.1', 'username', 'password')

    def test_send(self):
        self.assertTrue(self.dm.send('testing_message', 'username'))
    
    def test_retrieve_new(self):
        new_messages = self.dm.retrieve_new()
        self.assertEqual(new_messages, [])

    def test_retrieve_all(self):
        messages = self.dm.retrieve_all()
        self.assertEqual(messages, [{"message": "testing_message", "recipient": "username", "timestamp": "1747846396.924108", "status": "sent"}, {"message": "testing_message", "from": "username", "timestamp": "1747846396.924108", "status": "read"}])

if __name__ == "__main__":
    unittest.main()
    
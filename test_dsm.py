from ds_messenger import DirectMessenger
import unittest
from collections import namedtuple

Message_received = namedtuple('Message_received', ['message', 'from_name', 'timestamp', 'status'])
Message_sent = namedtuple('Message_sent', ['message', 'recipient', 'timestamp', 'status'])

class TestDSMessenger(unittest.TestCase):
    def test_send_and_retrieve_new(self):
        dm_b = DirectMessenger('127.0.0.1', 'B', '456')
        dm_b.send('testing_msg', 'A')
        dm_a = DirectMessenger('127.0.0.1', 'A', '123')
        new_messages = dm_a.retrieve_new()
        self.assertIsInstance(new_messages, list)
        
        dm_b.close()
        dm_a.close()

    def test_send_and_retrieve_all(self):
        dm_b = DirectMessenger('127.0.0.1', 'B', '456')
        dm_b.send('hello', 'A')
        messages = dm_b.retrieve_all()
        self.assertIsInstance(messages, list)

        dm_b.close()

if __name__ == "__main__":
    unittest.main()
    
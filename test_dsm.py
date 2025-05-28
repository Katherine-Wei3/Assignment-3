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

    def test_init_sets_attributes(self):
        dm = DirectMessenger('127.0.0.1', 'A', '123')
        self.assertEqual(dm.username, 'A')
        self.assertEqual(dm.password, '123')
        self.assertTrue(str(dm.notebook_path).endswith('A_notebook.json'))
        dm.close()

    def test_send_without_connection(self):
        dm = DirectMessenger('badhost', 'A', '123')
        with self.assertRaises(ConnectionError):
            dm.send('msg', 'B')
        dm.close()

    def test_notebook_saves_and_loads(self):
        dm = DirectMessenger('127.0.0.1', 'A', '123')
        dm.nb.add_contact_and_message(str(dm.notebook_path), 'B', 'test message')
        dm.nb.save(str(dm.notebook_path))
        dm2 = DirectMessenger('127.0.0.1', 'A', '123')
        dm2.nb.load(str(dm.notebook_path))
        self.assertIn('B', dm2.nb.chats)
        self.assertIn('test message', dm2.nb.chats['B'])
        dm.close()
        dm2.close()

if __name__ == "__main__":
    unittest.main()
    
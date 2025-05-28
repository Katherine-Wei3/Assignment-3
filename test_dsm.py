from ds_messenger import DirectMessenger
import unittest
from collections import namedtuple
import json
import os

Message_received = namedtuple('Message_received', ['message', 'from_name', 'timestamp', 'status'])
Message_sent = namedtuple('Message_sent', ['message', 'recipient', 'timestamp', 'status'])

class TestDSMessenger(unittest.TestCase):
    def test_send_and_retrieve_new(self):
        dm_b = DirectMessenger('127.0.0.1', 'B', '456')
        dm_b.send('testing_msg', 'A')
        dm_a = DirectMessenger('127.0.0.1', 'A', '123')
        new_messages = dm_a.retrieve_new()
        testing_msg = next((m for m in new_messages if getattr(m, 'message', None) == 'testing_msg'), None)
        self.assertIsInstance(new_messages, list)
        self.assertIsNotNone(testing_msg)
        self.assertEqual(testing_msg.message, 'testing_msg')
        self.assertEqual(testing_msg.from_name, 'B')
        self.assertIsInstance(testing_msg.timestamp, str)

        dm_b.close()
        dm_a.close()

    def test_send_and_retrieve_all(self):
        dm_b = DirectMessenger('127.0.0.1', 'B', '456')
        dm_b.send('hello', 'A')
        messages = dm_b.retrieve_all()
        self.assertIsInstance(messages, list)
        hello_msg = next((m for m in messages if getattr(m, 'message', None) == 'hello'), None)
        self.assertIsNotNone(hello_msg)
        self.assertEqual(hello_msg.message, 'hello')
        self.assertEqual(hello_msg.recipient, 'A')
        self.assertIsInstance(hello_msg.timestamp, str)
        dm_b.close()

    def test_init_sets_attributes(self):
        dm_a = DirectMessenger('127.0.0.1', 'A', '123')
        self.assertEqual(dm_a.username, 'A')
        self.assertEqual(dm_a.password, '123')
        self.assertTrue(str(dm_a.notebook_path).endswith('A_notebook.json'))
        dm_a.close()

    def test_send_without_connection(self):
        # Should raise ConnectionError on bad host
        with self.assertRaises(ConnectionError):
            DirectMessenger('badhost', 'A', '123')
        # Should raise ConnectionError if send_file is missing
        dm = DirectMessenger.__new__(DirectMessenger)  # create instance without __init__
        dm.username = 'A'
        dm.password = '123'
        dm.notebook_path = 'dummy.json'
        with self.assertRaises(ConnectionError):
            dm.send('msg', 'B')

    def test_notebook_saves_and_loads(self):
        dm_a = DirectMessenger('127.0.0.1', 'A', '123')
        dm_a.nb.add_contact_and_message(str(dm_a.notebook_path), 'B', 'test message')
        dm_a.nb.save(str(dm_a.notebook_path))
        dm_a.close()
        dm2 = DirectMessenger('127.0.0.1', 'A', '123')
        dm2.nb.load(str(dm2.notebook_path))
        self.assertIn('B', dm2.nb.chats)
        self.assertIn('test message', dm2.nb.chats['B'])
        dm2.close()

    def test_close_handles_missing_attributes(self):
        dm = DirectMessenger.__new__(DirectMessenger)
        # Should not raise even if send_file, recv, client are missing
        try:
            dm.close()
        except Exception as e:
            self.fail(f"close() raised {e}")

    def test_save_method(self):
        dm = DirectMessenger('127.0.0.1', 'A', '123')
        test_data = {'foo': 'bar'}
        filename = 'test_save.json'
        dm.save(filename, test_data)
        with open(filename, 'r') as f:
            loaded = json.load(f)
        self.assertEqual(loaded, test_data)
        os.remove(filename)
        dm.close()

    def test_retrieve_new_not_connected(self):
        dm = DirectMessenger.__new__(DirectMessenger)
        dm.username = 'A'
        dm.password = '123'
        dm.notebook_path = 'dummy.json'
        result = dm.retrieve_new()
        self.assertEqual(result, [])

    def test_retrieve_all_not_connected(self):
        dm = DirectMessenger.__new__(DirectMessenger)
        dm.username = 'A'
        dm.password = '123'
        dm.notebook_path = 'dummy.json'
        result = dm.retrieve_all()
        self.assertEqual(result, [])
        
if __name__ == "__main__":
    try:
        unittest.main()
    except ConnectionRefusedError:
        pass

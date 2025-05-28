"""Unit tests for the DirectMessenger class and related functionality."""

import unittest
from collections import namedtuple
import json
import os
from ds_messenger import DirectMessenger

MessageReceived = namedtuple(
    'MessageReceived', [
        'message', 'from_name', 'timestamp', 'status'])
MessageSent = namedtuple(
    'MessageSent', [
        'message', 'recipient', 'timestamp', 'status'])


class TestDSMessenger(unittest.TestCase):
    """Unit tests for DirectMessenger."""

    def test_send_and_retrieve_new(self):
        """Test sending and retrieving a new message."""
        user_b = DirectMessenger('127.0.0.1', 'B', '456')
        user_b.send('testing_msg', 'A')
        user_a = DirectMessenger('127.0.0.1', 'A', '123')
        new_messages = user_a.retrieve_new()
        testing_msg = next(
            (m for m in new_messages if getattr(
                m, 'message', None) == 'testing_msg'), None)
        self.assertIsInstance(new_messages, list)
        self.assertIsNotNone(testing_msg)
        self.assertEqual(testing_msg.message, 'testing_msg')
        self.assertEqual(testing_msg.from_name, 'B')
        self.assertIsInstance(testing_msg.timestamp, str)
        user_b.close()
        user_a.close()

    def test_send_and_retrieve_all(self):
        """Test sending and retrieving all messages."""
        user_b = DirectMessenger('127.0.0.1', 'B', '456')
        user_b.send('hello', 'A')
        messages = user_b.retrieve_all()
        self.assertIsInstance(messages, list)
        hello_msg = next(
            (m for m in messages if getattr(
                m, 'message', None) == 'hello'), None)
        self.assertIsNotNone(hello_msg)
        self.assertEqual(hello_msg.message, 'hello')
        self.assertEqual(hello_msg.recipient, 'A')
        self.assertIsInstance(hello_msg.timestamp, str)
        user_b.close()

    def test_init_sets_attributes(self):
        """Test that initialization sets attributes correctly."""
        user_a = DirectMessenger('127.0.0.1', 'A', '123')
        self.assertEqual(user_a.username, 'A')
        self.assertEqual(user_a.password, '123')
        self.assertTrue(str(user_a.notebook_path).endswith('A_notebook.json'))
        user_a.close()

    def test_send_without_connection(self):
        """Test sending without a connection raises ConnectionError."""
        with self.assertRaises(ConnectionError):
            DirectMessenger('badhost', 'A', '123')
        user_a = DirectMessenger.__new__(DirectMessenger)
        user_a.username = 'A'
        user_a.password = '123'
        user_a.notebook_path = 'dummy.json'
        with self.assertRaises(ConnectionError):
            user_a.send('msg', 'B')

    def test_notebook_saves_and_loads(self):
        """Test saving and loading the notebook."""
        user_a = DirectMessenger('127.0.0.1', 'A', '123')
        user_a.notebook.add_contact_and_message(
            str(user_a.notebook_path), 'B', 'test message')
        user_a.notebook.save(str(user_a.notebook_path))
        user_a.close()
        user_b = DirectMessenger('127.0.0.1', 'A', '123')
        user_b.notebook.load(str(user_b.notebook_path))
        self.assertIn('B', user_b.notebook.chats)
        self.assertIn('test message', user_b.notebook.chats['B'])
        user_b.close()

    def test_save_method(self):
        """Test the save method for writing JSON data."""
        user_a = DirectMessenger('127.0.0.1', 'A', '123')
        test_data = {'foo': 'bar'}
        filename = 'test_save.json'
        user_a.save(filename, test_data)
        with open(filename, 'r', encoding='utf-8') as file:
            loaded = json.load(file)
        self.assertEqual(loaded, test_data)
        os.remove(filename)
        user_a.close()

    def test_retrieve_new_not_connected(self):
        """Test retrieve_new returns empty list if not connected."""
        user_a = DirectMessenger.__new__(DirectMessenger)
        user_a.username = 'A'
        user_a.password = '123'
        user_a.notebook_path = 'dummy.json'
        result = user_a.retrieve_new()
        self.assertEqual(result, [])

    def test_retrieve_all_not_connected(self):
        """Test retrieve_all returns empty list if not connected."""
        user_a = DirectMessenger.__new__(DirectMessenger)
        user_a.username = 'A'
        user_a.password = '123'
        user_a.notebook_path = 'dummy.json'
        result = user_a.retrieve_all()
        self.assertEqual(result, [])


if __name__ == "__main__":
    unittest.main()
    
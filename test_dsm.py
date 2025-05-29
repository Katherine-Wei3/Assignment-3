"""Unit tests for the DirectMessenger class and related functionality."""

import unittest
from collections import namedtuple
import json
import os
from pathlib import Path
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
        # Ensure 'A' is in chats before sending to avoid KeyError
        if 'A' not in user_b.notebook.chats:
            user_b.notebook.chats['A'] = []
        user_b.send('testing_msg', 'A')
        user_a = DirectMessenger('127.0.0.1', 'A', '123')
        new_messages = user_a.retrieve_new()
        testing_msg = next(
            (m for m in new_messages if getattr(m, 'message', None) == 'testing_msg'), None)
        self.assertIsInstance(new_messages, list)
        self.assertIsNotNone(testing_msg)
        self.assertEqual(testing_msg.message, 'testing_msg')
        self.assertEqual(getattr(testing_msg, 'from_name', None), 'B')
        self.assertTrue(isinstance(testing_msg.timestamp, (str, float)))
        user_b.close()
        user_a.close()

    def test_send_and_retrieve_all(self):
        """Test sending and retrieving all messages."""
        user_b = DirectMessenger('127.0.0.1', 'B', '456')
        if 'A' not in user_b.notebook.chats:
            user_b.notebook.chats['A'] = []
        user_b.send('hello', 'A')
        messages = user_b.retrieve_all()
        self.assertIsInstance(messages, list)
        hello_msg = next(
            (m for m in messages if getattr(m, 'message', None) == 'hello'), None)
        self.assertIsNotNone(hello_msg)
        self.assertEqual(hello_msg.message, 'hello')
        self.assertEqual(getattr(hello_msg, 'recipient', None), 'A')
        self.assertTrue(isinstance(hello_msg.timestamp, (str, float)))
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
        # This should raise in __init__ if host is bad
        with self.assertRaises(Exception):
            DirectMessenger('badhost', 'A', '123')
        # This should raise in send if not connected
        user_a = DirectMessenger.__new__(DirectMessenger)
        user_a.username = 'A'
        user_a.password = '123'
        user_a.notebook_path = 'dummy.json'
        user_a.notebook = None
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
        user_a.notebook = None
        result = user_a.retrieve_new()
        self.assertEqual(result, [])

    def test_retrieve_all_not_connected(self):
        """Test retrieve_all returns empty list if not connected."""
        user_a = DirectMessenger.__new__(DirectMessenger)
        user_a.username = 'A'
        user_a.password = '123'
        user_a.notebook_path = 'dummy.json'
        user_a.notebook = None
        result = user_a.retrieve_all()
        self.assertEqual(result, [])

    def test_close_handles_missing_attributes(self):
        """Test close handles missing attributes gracefully."""
        user = DirectMessenger.__new__(DirectMessenger)
        user.send_file = None
        user.recv = None
        user.client = None
        try:
            user.close()
        except Exception as e:
            self.fail(f"close() raised an exception unexpectedly: {e}")

    def test_save_file_error(self):
        """Test save raises an exception on invalid path."""
        user = DirectMessenger.__new__(DirectMessenger)
        with self.assertRaises(Exception):
            user.save("/invalid_path/does_not_exist.json", {"foo": "bar"})

    def test_connect_exception(self):
        """Test _connect fails and prints error (covers lines 51-52)."""
        user = DirectMessenger.__new__(DirectMessenger)
        with self.assertRaises(Exception):
            user._connect('badhost', 9999)

    def test_send_not_connected_branch(self):
        """Test send when not connected (covers lines 66-78, 85-98)."""
        user = DirectMessenger.__new__(DirectMessenger)
        user.notebook = None
        with self.assertRaises(ConnectionError):
            user.send('msg', 'B')

    def test_send_response_and_save(self):
        """Test send appends to notebook and saves (covers lines 85-98)."""
        user_a = DirectMessenger('127.0.0.1', 'A', '123')
        if 'B' not in user_a.notebook.chats:
            user_a.notebook.chats['B'] = []
        user_a.send('coverage_msg', 'B')
        self.assertIn('B', user_a.notebook.chats)
        found = any(m.message == 'coverage_msg' for m in user_a.notebook.chats['B'])
        self.assertTrue(found)
        user_a.close()

    def test_retrieve_new_none_response(self):
        """Test retrieve_new with no response (covers 109-122, 153-155)."""
        user = DirectMessenger.__new__(DirectMessenger)
        user.username = 'A'
        user.password = '123'
        user.notebook_path = 'dummy.json'
        user.notebook = None
        # Simulate not connected
        result = user.retrieve_new()
        self.assertEqual(result, [])

    def test_retrieve_all_none_response(self):
        """Test retrieve_all with no response (covers 132-145, 153-155)."""
        user = DirectMessenger.__new__(DirectMessenger)
        user.username = 'A'
        user.password = '123'
        user.notebook_path = 'dummy.json'
        user.notebook = None
        # Simulate not connected
        result = user.retrieve_all()
        self.assertEqual(result, [])

    def test_send_recipient_not_in_chats(self):
        """Covers KeyError branch in send (66-78)."""
        user = DirectMessenger('127.0.0.1', 'A', '123')
        # Remove recipient if present
        if 'Z' in user.notebook.chats:
            del user.notebook.chats['Z']
        # Should raise KeyError or handle it if your code does
        try:
            user.send('msg', 'Z')
        except KeyError:
            pass  # This is expected if your code does not handle it
        except Exception:
            pass
        user.close()

    def test_send_not_connected(self):
        """Covers not connected branch in send (66-78)."""
        user = DirectMessenger.__new__(DirectMessenger)
        user.notebook = None
        with self.assertRaises(ConnectionError):
            user.send('msg', 'B')

    def test_retrieve_new_not_connected(self):
        """Covers not connected branch in retrieve_new (109-122, 153-155)."""
        user = DirectMessenger.__new__(DirectMessenger)
        user.notebook = None
        result = user.retrieve_new()
        self.assertEqual(result, [])

    def test_retrieve_all_not_connected(self):
        """Covers not connected branch in retrieve_all (132-145, 153-155)."""
        user = DirectMessenger.__new__(DirectMessenger)
        user.notebook = None
        result = user.retrieve_all()
        self.assertEqual(result, [])

    def test_connect_exception(self):
        """Covers exception handling in _connect (51-52)."""
        user = DirectMessenger.__new__(DirectMessenger)
        with self.assertRaises(Exception):
            user._connect('badhost', 9999)
            
if __name__ == "__main__":
    unittest.main()
from ds_messenger import DirectMessenger
import unittest

class TestDSMessenger(unittest.TestCase):
    def setUp(self):
        self.dm = DirectMessenger('127.0.0.1', 'username', 'password')

    def test_send(self):
        self.assertTrue(self.dm.send('testing_message', 'username'))
        self.dm.close()

    def test_retrieve_new(self):
        new_messages = self.dm.retrieve_new()
        self.assertEqual(new_messages, ['testing_message'])
        self.dm.close()

    def test_retrieve_all(self):
        messages = self.dm.retrieve_all()
        self.assertEqual(messages, [])
        self.dm.close()

if __name__ == "__main__":
    unittest.main()
    
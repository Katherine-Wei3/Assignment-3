import unittest
import json
from ds_protocol import (
    auth_request,
    extract_json,
    direct_message_request,
    fetch_request,
    _extract_messages_received,
    _extract_messages_sent
)

class TestDSProtocol(unittest.TestCase):
    def test_auth_request(self):
        req = auth_request("alice", "pw123")
        self.assertIn('"username": "alice"', req)
        self.assertIn('"password": "pw123"', req)

    def test_direct_message_request(self):
        req = direct_message_request("token123", "bob", "hi there")
        self.assertIn('"token": "token123"', req)
        self.assertIn('"directmessage"', req)
        self.assertIn('"entry": "hi there"', req)
        self.assertIn('"recipient": "bob"', req)

    def test_fetch_request(self):
        req = fetch_request("token123", "all")
        self.assertIn('"token": "token123"', req)
        self.assertIn('"messages": "all"', req)

    def test_extract_json_valid(self):
        json_msg = '{"response": {"type": "ok", "message": "Welcome", "token": "abc"}}'
        result = extract_json(json_msg)
        self.assertEqual(result.type, "ok")
        self.assertEqual(result.message, "Welcome")
        self.assertEqual(result.token, "abc")

    def test_extract_json_decode_error(self):
        # Covers JSONDecodeError branch
        result = extract_json("not a json string")
        self.assertIsNone(result)

    def test_extract_json_missing_response(self):
        # Covers generic exception branch (simulate missing 'response')
        with self.assertRaises(Exception):
            extract_json(json.dumps({"notresponse": {}}))

    def test_extract_messages_received_and_sent_all_branches(self):
        # Covers: no 'from', no 'recipient', both present, empty messages
        json_obj = {
            "response": {
                "messages": [
                    {"message": "hi", "timestamp": "123"},  # neither
                    {"message": "yo", "from": "alice", "timestamp": "124"},  # received
                    {"message": "sup", "recipient": "bob", "timestamp": "125"},  # sent
                    {"message": "hey", "from": "eve", "recipient": "bob", "timestamp": "126"},  # both
                ]
            }
        }
        received = _extract_messages_received(json_obj)
        sent = _extract_messages_sent(json_obj)
        # Only messages with 'from' are received
        self.assertEqual(len(received), 2)
        self.assertEqual(received[0].from_name, "alice")
        self.assertEqual(received[1].from_name, "eve")
        # Only messages with 'recipient' are sent
        self.assertEqual(len(sent), 2)
        self.assertEqual(sent[0].recipient, "bob")
        self.assertEqual(sent[1].recipient, "bob")

    def test_extract_messages_received_empty(self):
        # Covers line 53: no 'from' key
        obj = {"response": {"messages": [{"message": "hi", "timestamp": "1"}]}}
        result = _extract_messages_received(obj)
        self.assertEqual(result, [])

    def test_extract_messages_sent_empty(self):
        # Covers line 57-62: no 'recipient' key
        obj = {"response": {"messages": [{"message": "hi", "timestamp": "1"}]}}
        result = _extract_messages_sent(obj)
        self.assertEqual(result, [])

    def test_extract_messages_both(self):
        # Covers both branches: both 'from' and 'recipient'
        obj = {"response": {"messages": [
            {"message": "hi", "from": "alice", "timestamp": "1"},
            {"message": "yo", "recipient": "bob", "timestamp": "2"}
        ]}}
        received = _extract_messages_received(obj)
        sent = _extract_messages_sent(obj)
        self.assertEqual(len(received), 1)
        self.assertEqual(len(sent), 1)
    
    def test_extract_json_no_message_or_messages(self):
        # Covers lines 46-53: response with neither 'message' nor 'messages'
        json_msg = '{"response": {"type": "ok"}}'
        result = extract_json(json_msg)
        self.assertEqual(result.type, "ok")
        self.assertIsNone(result.message)
        self.assertIsNone(result.token)

    def test_extract_json_raises_dsp_error(self):
        # Covers lines 61-62: generic exception branch
        # Simulate a response that will cause a KeyError inside extract_json
        bad_json = '{"response": {"type": "ok", "messages": [{"foo": "bar"}]}}'
        with self.assertRaises(Exception):  # DSPError is a subclass of Exception
            extract_json(bad_json)

    def test_extract_messages_received_no_from(self):
        # Covers lines 86-94: _extract_messages_received with no 'from' key
        obj = {"response": {"messages": [{"message": "hi", "timestamp": "1"}]}}
        result = _extract_messages_received(obj)
        self.assertEqual(result, [])
    
    
if __name__ == "__main__":
    unittest.main()
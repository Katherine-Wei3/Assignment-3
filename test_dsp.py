from ds_protocol import auth_request, extract_json, direct_message_request, fetch
import unittest
from collections import namedtuple
import json

Message_received = namedtuple('Message_received', ['message', 'from_name', 'timestamp', 'status'])

class TestDSProtocol(unittest.TestCase):
    def test_extract_json(self):
        json_msg = '{"response": {"type": "ok", "message": "Welcome back, ohhimark", "token": "07da3ddc-6b9a-4734-b3ca-f0aa7ff22360"}}'
        result = extract_json(json_msg)
        self.assertEqual(result.type, 'ok')
        self.assertEqual(result.message, 'Welcome back, ohhimark')
        self.assertEqual(result.token, '07da3ddc-6b9a-4734-b3ca-f0aa7ff22360')

    def test_auth_request(self):
        json_msg = '{"authenticate": {"username": "<USERNAME>", "password": "<PASSWORD>"}}'
        self.assertEqual(auth_request("<USERNAME>", "<PASSWORD>"), json_msg)

    def test_direct_message_request(self):
        json_msg = '{"token": "<TOKEN>", "directmessage": {"entry": "<MESSAGE>", "recipient": "<RECIPIENT>", "timestamp": "<TIMESTAMP>"}}'
        self.assertEqual(direct_message_request("<TOKEN>", "<RECIPIENT>", "<MESSAGE>", "<TIMESTAMP>"), json_msg)

    def test_fetch(self):
        json_msg = '{"token": "<TOKEN>", "fetch": "<FETCH_TYPE>"}'
        self.assertEqual(fetch("<TOKEN>", "<FETCH_TYPE>"), json_msg)

    def test_extract_message(self):
        json_msg = json.dumps(
        {
            "response": {
                "type": "ok",
                "messages": [
                    {
                        "message": "Are you there?!",
                        "from": "markb",
                        "timestamp": "1603167689.3928561"
                    },
                    {
                        "message": "Text me ASAP",
                        "recipient": "thebeemoviescript",
                        "timestamp": "1603167689.3928561"
                    }
                ]
            }
        })
        msg1 = Message_received("Are you there?!", "markb", "1603167689.3928561", None)
        msg2 = Message_received("Text me ASAP", "thebeemoviescript", "1603167689.3928561", None)
        lst = [msg1, msg2]
        # print(extract_json(json_msg).message)  # DEBUG
        self.assertEqual(extract_json(json_msg).message, lst)
        self.assertEqual(extract_json(json_msg).type, 'ok')

if __name__ == "__main__":
    unittest.main()
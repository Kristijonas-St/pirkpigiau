import unittest
from unittest.mock import patch
from speech_response_feature.speech_response import say_formatted_response

@patch('speech_response_feature.speech_response.speak')
class TestSpeechResponse(unittest.TestCase):
    def test_say_formatted_response_found(self, mock_speak):
        say_formatted_response(True, "bananai", "Rimi", "1.25")
        mock_speak.assert_called_once()
        spoken_text = mock_speak.call_args[0][0]

        expected_response = "Preke, bananai, pigiausia, Rimi, 1 euras, 25 centai"
        self.assertEqual(spoken_text, expected_response)

    def test_say_formatted_response_not_found(self, mock_speak):
        say_formatted_response(False, "ananasai", "IKI", None)
        mock_speak.assert_called_once()
        spoken_text = mock_speak.call_args[0][0]

        expected_response = "Prekė ananasai nerasta"
        self.assertEqual(spoken_text, expected_response)

if __name__ == '__main__':
    unittest.main()

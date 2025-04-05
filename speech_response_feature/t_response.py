import unittest
from unittest.mock import patch

from speech_response_feature.speech_response import say_formatted_response

class TestSpeechResponse(unittest.TestCase):
    @patch('speech_response_feature.speech_response.speak')
    def test_say_formatted_response_found(self, mock_speak):
        say_formatted_response(True, "bananai", "Rimi", "1,25 €")
        mock_speak.assert_called_once()
        spoken_text = mock_speak.call_args[0][0]

        self.assertIn("bananai", spoken_text)
        self.assertIn("eur", spoken_text)
        self.assertIn("Rimi", spoken_text)

    @patch('speech_response_feature.speech_response.speak')
    def test_say_formatted_response_not_found(self, mock_speak):
        say_formatted_response(False, "ananasai", "IKI", None)
        mock_speak.assert_called_once_with("Prekė ananasai nerasta")

if __name__ == '__main__':
    unittest.main()

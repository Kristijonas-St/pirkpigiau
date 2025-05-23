import time
from unittest.mock import patch
from scraping_feature.scraping_feature import ScrapingRequest
from voice_recognition.voice_recognition import VoiceRecognizer
import whisper

@patch.object(whisper.Whisper, 'transcribe')
@patch('voice_recognition.voice_recognition.VoiceRecognizer.record_audio', return_value="test_audio.wav")
@patch('requests.get')
@patch('scraping_feature.scraping_feature.RimiScraper.scrape')
def test_voice_recognition_and_scraping(mock_scrape, mock_get, mock_record_audio, mock_transcribe):
    mock_scrape.return_value = ("pomidorai", 1.29 , "URL", "Succesful")
    mock_transcribe.return_value = {"text": "pomidorai"}
    recognizer = VoiceRecognizer()

    start_time = time.time()
    result_voice = recognizer.recognize_speech_whisper()
    scraping_result = ScrapingRequest("Rimi", result_voice).scrape_price()
    end_time = time.time()

    assert scraping_result is not None, f"Scraping returned None"
    assert result_voice == "pomidorai", f"Recognized {result_voice}"
    mock_record_audio.assert_called_once()
    mock_transcribe.assert_called_once_with("test_audio.wav", language="lt")
    assert (end_time - start_time) < 10, f"Processing took too long: {end_time - start_time:.2f}s"
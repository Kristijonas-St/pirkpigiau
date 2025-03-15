import streamlit as st
import whisper
import sounddevice as sd
import numpy as np
import tempfile
import wave

st.info("Įkeliama balso atpažinimo funkcija (gali užtrukti kelias sekundes)")
model = whisper.load_model("small")

class VoiceRecognizer:
    def __init__(self):
        self.model = model
    def record_audio(self, duration=3, samplerate=16000):
        st.info("🎙️ Kalbėkite dabar...")
        recording = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=1, dtype=np.int16)
        sd.wait()

        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio:
            with wave.open(temp_audio.name, 'wb') as wf:
                wf.setnchannels(1)
                wf.setsampwidth(2)
                wf.setframerate(samplerate)
                wf.writeframes(recording.tobytes())
            return temp_audio.name

    def recognize_speech_whisper(self):
        audio_file = self.record_audio()
        st.info("🔄 Apdorojama kalba...")

        result = model.transcribe(audio_file, language="lt")
        return result["text"].strip()

class StreamLitOutputEditor:
    def __init__(self):
        self.voice_recognizer = VoiceRecognizer()

        if "recognized_text" not in st.session_state:
            st.session_state.recognized_text = ""

        if "scrape_result" not in st.session_state:
            st.session_state.scrape_result = ""
    def display_scrape_result(self):
        st.title("🎙️ Pigiausių prekių paieška balsu")
        if st.button("🎤 Pasakyti prekę"):
            st.session_state.recognized_text = self.voice_recognizer.recognize_speech_whisper()

        if st.session_state.recognized_text:
            edited_text = st.text_input("Atpažintas žodis:", value=st.session_state.recognized_text)

            if edited_text != st.session_state.recognized_text:
                pass

        st.write(st.session_state.scrape_result)
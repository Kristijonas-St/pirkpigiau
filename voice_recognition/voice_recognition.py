import streamlit as st
import whisper
import sounddevice as sd
import numpy as np
import tempfile
import wave


st.info("Įkeliama Whisper AI modelis... (gali užtrukti kelias sekundes)")
model = whisper.load_model("small")  # Options: "tiny", "base", "small", "medium", "large"

def record_audio(duration=3, samplerate=16000):
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


def recognize_speech_whisper():
    audio_file = record_audio()
    st.info("🔄 Apdorojama kalba...")

    result = model.transcribe(audio_file, language="lt")
    return result["text"].strip()


st.title("🎙️ Pigiausių prekių paieška su balsu (Whisper AI)")
if st.button("🎤 Pasakyti prekę"):
    spoken_text = recognize_speech_whisper()
    st.write(f"✅ Atpažinta kalba: **{spoken_text}**")

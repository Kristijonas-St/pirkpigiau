import streamlit as st
from scraping_feature.scraping_feature import ScrapingRequest
from speech_response_feature.speech_response import say_formatted_response
from voice_recognition.voice_recognition import StreamLitOutputEditor

def perform_scraping(item_name):
    request = ScrapingRequest(shop_name, item_name)
    data = request.scrape_price()
    if not data:
        return "Nepavyko rasti prekės."
    elif request.cheapest_item:
        result = f"{shop_name.upper()}: Pigiausias variantas: [{data.item_name}]({data.item_url}) už {data.cheapest_item}"
        say_formatted_response(data.item_name, shop_name, data.cheapest_item)
        return result
    return "Nepavyko rasti prekės."

app = StreamLitOutputEditor()
shop_name = "Rimi"
st.title("🎙️ Pigiausių prekių paieška balsu")

if "recognized_text" not in st.session_state:
    st.session_state.recognized_text = ""
if "scrape_result" not in st.session_state:
    st.session_state.scrape_result = ""

try:
    if st.button("🎤 Pasakyti prekę"):
        st.session_state.recognized_text = app.voice_recognizer.recognize_speech_whisper()
        if st.session_state.recognized_text:
            st.session_state.scrape_result = perform_scraping(st.session_state.recognized_text)

    if st.session_state.recognized_text:
        edited_text = st.text_input("Atpažintas žodis:", value=st.session_state.recognized_text)
        if edited_text != st.session_state.recognized_text:
            st.session_state.recognized_text = edited_text
            st.session_state.scrape_result = perform_scraping(edited_text)

    st.markdown(st.session_state.scrape_result, unsafe_allow_html=True)
except Exception as e:
    st.error("Nepavyko rasti prekės :( Pataisykite atpažintą žodį arba pabandykite dar kartą.")
    edited_text = st.text_input("Atpažintas žodis:", value=st.session_state.recognized_text)
    if edited_text != st.session_state.recognized_text:
        st.session_state.recognized_text = edited_text
        st.session_state.scrape_result = perform_scraping(edited_text)
    st.markdown(st.session_state.scrape_result, unsafe_allow_html=True)

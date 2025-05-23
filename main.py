import streamlit as st
from scraping_feature.scraping_feature import ScrapingRequest
from speech_response_feature.speech_response import say_formatted_response
from voice_recognition.voice_recognition import VoiceRecognizer
import time

def perform_scraping(item_name, shops):
    data = []
    results = dict()
    voice_responses = []
    index = 0
    is_found = False

    for shop in shops:
        request = ScrapingRequest(shop, item_name)
        data.append(request.scrape_price())

        if data[index]:
            is_found = True
            price = float(data[index].cheapest_item)
            message = f"{shop.upper()}: Pigiausias variantas: [{data[index].item_name}]({data[index].item_url}) už "
            results[message] = price
            voice_responses.append((is_found, data[index].item_name, shop, data[index].cheapest_item))
        else:
            is_found = False
            price = float('inf')
            message = f"{shop.upper()}: Prekė {item_name} nerasta."
            results[message] = price
            voice_responses.append((is_found, item_name, shop, None))

        index += 1

    sorted_results = sorted(results.items(), key=lambda x: x[1])
    return sorted_results, voice_responses

app = VoiceRecognizer()
shops = ["Rimi", "Maxima", "IKI"]
st.title("🎙️ Pigiausių prekių paieška balsu")

if "recognized_text" not in st.session_state:
    st.session_state.recognized_text = ""
if "scrape_result" not in st.session_state:
    st.session_state.scrape_result = []
if "voice_responses" not in st.session_state:
    st.session_state.voice_responses = []
if "favorites" not in st.session_state:
    st.session_state.favorites = []
if "clear_after_response" not in st.session_state:
    st.session_state.clear_after_response = False
if "last_response_time" not in st.session_state:
    st.session_state.last_response_time = None
if "theme" not in st.session_state:
    st.session_state.theme = "light"
if "from_voice_input" not in st.session_state:
    st.session_state.from_voice_input = False
if "last_input_method" not in st.session_state:
    st.session_state.last_input_method = "Įvesti ranka"
if "theme_changed" not in st.session_state:
    st.session_state.theme_changed = False
if "skip_voice_response_once" not in st.session_state:
    st.session_state.skip_voice_response_once = False

theme_toggle = st.toggle("🌙 Perjungti temą", key="theme_toggle")

if theme_toggle and st.session_state.theme != "dark":
    st.session_state.theme = "dark"
    st.session_state.theme_changed = True
    st.session_state.skip_voice_response_once = True
elif not theme_toggle and st.session_state.theme != "light":
    st.session_state.theme = "light"
    st.session_state.theme_changed = True
    st.session_state.skip_voice_response_once = True
theme = st.session_state.theme

if theme == "dark":
    st.markdown("""
        <style>
        body, .stApp{
            background-color: #0E1117;
            color: #31333F;
            h1{
                color: #FAFAFA;
            }
        }
        h1, p{
            color: #FAFAFA;
        }
        button{
            p{
                color: #31333F;   
            }
        }
        </style>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
        <style>
        body, .stApp {
            background-color: #FFFFFF;
            color: #31333F;
        }
        </style>
    """, unsafe_allow_html=True)

input_method = st.radio("Pasirinkite įvedimo būdą:", ("Įvesti ranka", "Įrašyti balsu"))

if input_method != st.session_state.last_input_method:
    current_theme = st.session_state.theme
    st.session_state.update({
        "recognized_text": "",
        "scrape_result": [],
        "voice_responses": [],
        "clear_after_response": False,
        "from_voice_input": False,
        "last_input_method": input_method,
        "theme": current_theme,
    })
    if not st.session_state.theme_changed:
        st.session_state.has_said_response = False

    st.session_state.theme_changed = False

    st.rerun()

if input_method == "Įvesti ranka":
    with st.form("manual_input_form"):
        new_input = st.text_input("Įveskite prekės pavadinimą:", value=st.session_state.recognized_text)
        submitted = st.form_submit_button("🔍 Ieškoti")

    if submitted and new_input and new_input != st.session_state.recognized_text:
        st.session_state.recognized_text = new_input
        st.session_state.scrape_result, st.session_state.voice_responses = perform_scraping(new_input, shops)
        st.session_state.clear_after_response = True
        st.session_state.last_response_time = time.time()
        st.session_state.from_voice_input = False
        st.session_state.has_said_response = False
        st.session_state.skip_voice_response_once = False

elif st.button("🎤 Pasakyti prekę"):
    st.session_state.recognized_text = app.recognize_speech_whisper()
    st.session_state.from_voice_input = True

    if st.session_state.recognized_text:
        st.session_state.scrape_result, st.session_state.voice_responses = perform_scraping(st.session_state.recognized_text, shops)
        st.session_state.clear_after_response = True
        st.session_state.last_response_time = time.time()
        st.session_state.has_said_response = False
        st.session_state.skip_voice_response_once = False

if st.session_state.from_voice_input and st.session_state.recognized_text:
    edited_text = st.text_input("Atpažintas žodis:", value=st.session_state.recognized_text)
    if edited_text != st.session_state.recognized_text:
        st.session_state.recognized_text = edited_text
        st.session_state.scrape_result, st.session_state.voice_responses = perform_scraping(edited_text, shops)
        st.session_state.clear_after_response = True
        st.session_state.last_response_time = time.time()
        st.session_state.has_said_response = False
        st.session_state.skip_voice_response_once = False

for i, result in enumerate(st.session_state.scrape_result):
    item_text = f"{result[0]}{result[1]}€" if result[1] != float('inf') else result[0]
    st.markdown(item_text, unsafe_allow_html=True)

    if result[1] != float('inf'):
        if st.button("❤️ Į patikusias", key=f"fav-{i}"):
            st.session_state.favorites.append(item_text)
            st.success("Prekė pridėta į patikusias!")

if st.session_state.voice_responses and not st.session_state.has_said_response:
    if st.session_state.skip_voice_response_once:
        st.session_state.skip_voice_response_once = False
        st.session_state.has_said_response = True
    else:
        cheapest_response = None
        for response in st.session_state.voice_responses:
            if response[0]:
                if cheapest_response is None or float(response[3]) < float(cheapest_response[3]):
                    cheapest_response = response

        if cheapest_response:
            say_formatted_response(*cheapest_response)
        else:
            say_formatted_response(False, st.session_state.recognized_text, "", None)

        st.session_state.has_said_response = True

if st.session_state.favorites:
    st.subheader("🧺 Patikusios prekės:")
    for favorite in st.session_state.favorites:
        st.markdown(f"- {favorite}", unsafe_allow_html=True)

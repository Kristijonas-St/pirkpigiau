import streamlit as st
import sounddevice as sd
import tempfile
import os
import time
import subprocess
import gtts

from scraping_feature.scraping_feature import ScrapingRequest

maxima_url = "https://www.maxima.lt/pasiulymai"
fixed_item_url = "https://barbora.lt/produktai/citrinos-3-4-d-1-kg"
item_to_search = "Citrinos"

st.title("Maxima.lt pigiausios prekės")

def form_euro_and_cent_case(price_value):
    euro = int(price_value)
    if euro == 1 or str(euro)[-1] == "1":
        euro_case = "euras"
    elif euro == 0 or str(euro)[-1] == "0":
        euro_case = "eurų"
    else:
        euro_case = "eurai"

    cents = round((price_value % 1) * 100)
    if cents == 1 or str(cents)[-1] == "1":
        cent_case = "centas"
    elif cents == 0 or str(cents)[-1] == "0":
        cent_case = "centų"
    else:
        cent_case = "centai"

    return euro_case, cent_case

def speak(text, lang="lt"):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_file:
        filename = temp_file.name

    tts = gtts.gTTS(text, lang=lang)
    tts.save(filename)

    if os.name == "nt":
        os.startfile(filename)
    else:
        subprocess.Popen(["mpg321", filename])

    time.sleep(5)
    for _ in range(3):
        try:
            os.remove(filename)
            break
        except PermissionError:
            time.sleep(2)


if st.button("Pasakykite prekę"):
    request = ScrapingRequest("Maxima", maxima_url, item_to_search).scrape_price()

    if request.error_message:
        st.write(request.error_message)
    elif request.cheapest_item:
        name, price = request.cheapest_item
        st.markdown(f"Pigiausias variantas: [{name}]({fixed_item_url}) už {price}", unsafe_allow_html=True)
        
        price_value = float(price.replace(" €", "").replace(",", "."))
        euro_case, cent_case = form_euro_and_cent_case(price_value)
        speech_response = f"Preke, {item_to_search}, pigiausia, Maximoje, {int(price_value)}, {euro_case}, {round((price_value % 1) * 100)}, {cent_case}"
        speak(speech_response)

    else:
        st.write("Nepavyko rasti prekės")




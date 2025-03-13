import streamlit as st
from scraping_feature.scraping_feature import ScrapingRequest

maxima_url = "https://www.maxima.lt/pasiulymai"
fixed_item_url = "https://barbora.lt/produktai/citrinos-3-4-d-1-kg"
item_to_search = "Citrinos"

st.title("Maxima.lt pigiausios prekės")

if st.button("Pasakykite prekę"):
    request = ScrapingRequest("Maxima", maxima_url, item_to_search).scrape_price()

    if request.error_message:
        st.write(request.error_message)
    elif request.cheapest_item:
        name, price = request.cheapest_item
        st.markdown(f"Pigiausias variantas: [{name}]({fixed_item_url}) už {price}", unsafe_allow_html=True)
    else:
        st.write("Nepavyko rasti prekės")

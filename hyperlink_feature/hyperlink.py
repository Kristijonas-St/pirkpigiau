import streamlit as st

st.title("HYPERLINK EXAMPLE")

iki_link = "https://lastmile.lt/product/IKI/Citrinos-2205"
maxima_link = "https://barbora.lt/produktai/citrinos-3-4-d-1-kg"
rimi_link = "https://www.rimi.lt/e-parduotuve/lt/produktai/vaisiai-darzoves-ir-geles/vaisiai-ir-uogos/citrinos/citrinos-c3-4-1-kl-1-kg/p/211080"

with st.container():
    st.markdown(
        f"""
        <div style="
            padding: 20px; 
            text-align: center; 
            border-radius: 10px;
            width: 300px;
            margin: auto;
            background-color: #f9f9f9;">
            <h2>Citrinos</h2>
            <p><a href="{iki_link}" target="_blank">IKI</a></p>
            <p><a href="{rimi_link}" target="_blank">RIMI</a></p>
            <p><a href="{maxima_link}" target="_blank">MAXIMA</a></p>
        </div>
        """,
        unsafe_allow_html=True
    )

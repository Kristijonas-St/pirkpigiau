import streamlit as st

# Set page title
st.title("Streamlit Frame Example")

# Create a frame using st.container()
with st.container():
    st.markdown(
        """
        <div style="
            border: 2px solid black; 
            padding: 20px; 
            text-align: center; 
            border-radius: 10px;
            width: 300px;
            margin: auto;
            background-color: #f9f9f9;">
            <h2 style="color: black;">
                <a href="https://lastmile.lt/product/IKI/Citrinos-2205" target="_blank" style="text-decoration: none; color: black;">
                    Citrinos
                </a>
            </h2>
        </div>
        """,
        unsafe_allow_html=True
    )

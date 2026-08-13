import streamlit as st
from components.sidebar import render_sidebar

st.title("DataVision AI")
menu = render_sidebar()
st.write(f"Seleccionaste: {menu}")
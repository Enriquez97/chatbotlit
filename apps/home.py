import streamlit as st
from utils.styles import styles

def home():
    styles()
    st.title("Home :frame_with_picture:")
    st.write(f"Bienvenido {st.session_state['username']} - {st.session_state['empresa_name']}")
    st.image(image=st.session_state["profile_img"])
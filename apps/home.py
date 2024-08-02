import streamlit as st
from utils.styles import styles
from apps.login import cookies

def home():
    styles()
    st.title("Home :frame_with_picture:")
    st.write(f"Bienvenido {st.session_state['username']} - {st.session_state['empresa_name']}")
    #st.image(image=st.session_state["profile_img"])
def home3():
    styles()
    st.title("Home :frame_with_picture:")
    st.write(f"Bienvenidow {st.session_state['username']} - {st.session_state['empresa_name']}")
    
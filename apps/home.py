import streamlit as st
import pandas as pd
from utils.styles import styles
#from apps.cookies import cookie_controller
def home():
    styles(1)
    #log_cookies = cookie_controller.get("logged_in")
    #if log_cookies:
    
    st.title("Home :frame_with_picture:")
    st.write(f"Bienvenido {st.session_state['username']} - {st.session_state['empresa_name']}")
    #with st.container(border=1):
    
    #st.image(image=st.session_state["profile_img"])
def home3():
    styles(1)
    
    st.title("Home :frame_with_picture:")
    st.write(f"Bienvenidow {st.session_state['username']} - {st.session_state['empresa_name']}")
    
    
    
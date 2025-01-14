import streamlit as st
from apps.cookies import cookies_manager

def logout():
    cookie_manager = cookies_manager()
    cookie_manager.delete("session_token")
    st.session_state['logged_in'] = False
    st.rerun()
    

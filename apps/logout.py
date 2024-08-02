import streamlit as st
from apps.login import cookies

def logout():
    st.session_state['logged_in'] = False
    cookies["username"] = ""
    cookies.save()
    st.rerun()
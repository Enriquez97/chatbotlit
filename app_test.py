import streamlit as st
from menu import menu

LOGO_NISIRA = "https://www.nisira.com.pe/images/Logo/logo2.png"


st.set_page_config(
    page_title="ChatBot",
    page_icon=LOGO_NISIRA,
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'About': "Nisira System"
    }
)
st.markdown("""
<style>

[data-testid="block-container"] {
    padding-left: 2rem;
    padding-right: 2rem;
    padding-top: 1rem;
    padding-bottom: 0rem;
    margin-bottom: -7rem;
}

[data-testid="stVerticalBlock"] {
    padding-left: 0rem;
    padding-right: 0rem;
}

[data-testid="stMetric"] {
    background-color: #393939;
    text-align: center;
    padding: 15px 0;
}

[data-testid="stMetricLabel"] {
  display: flex;
  justify-content: center;
  align-items: center;
}

[data-testid="stMetricDeltaIcon-Up"] {
    position: relative;
    left: 38%;
    -webkit-transform: translateX(-50%);
    -ms-transform: translateX(-50%);
    transform: translateX(-50%);
}

[data-testid="stMetricDeltaIcon-Down"] {
    position: relative;
    left: 38%;
    -webkit-transform: translateX(-50%);
    -ms-transform: translateX(-50%);
    transform: translateX(-50%);
}

</style>
""", unsafe_allow_html=True)

# Initialize st.session_state.role to None
if "role" not in st.session_state:
    st.session_state.role = None

# Retrieve the role from Session State to initialize the widget
st.session_state._role = st.session_state.role

def set_role():
    # Callback function to save the role selection to Session State
    st.session_state.role = st.session_state._role


# Selectbox to choose role
st.selectbox(
    "Select your role:",
    [None, "user", "admin", "super-admin"],
    key="_role",
    on_change=set_role,
)
menu() # Render the dynamic menu!
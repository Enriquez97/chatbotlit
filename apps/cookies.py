from extra_streamlit_components import CookieManager
import uuid

def generate_session_token():
    return str(uuid.uuid4())

def cookies_manager():
    return CookieManager()

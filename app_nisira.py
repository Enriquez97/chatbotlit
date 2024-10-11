import streamlit as st
from constants import LOGO_NISIRA
from apps.login import login_2
from routes import pages_rol,account_pages
from utils.auth import get_data_user
from utils.data_transform import decoding_avatar
from extra_streamlit_components import CookieManager
from datetime import datetime,timedelta
import uuid
from utils.auth import authenticate

st.set_page_config(
            page_title="Nisira",
            page_icon=LOGO_NISIRA,
            layout="wide",
            initial_sidebar_state="auto",
)

cookie_manager = CookieManager()

def generate_session_token():
    return str(uuid.uuid4())

def login():
    st.markdown("""
    <style>
    .container {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 100vh;
        flex-direction: column;
    }
    .form-container {
        width: 300px;
        padding: 20px;
        box-shadow: 0 0 15px rgba(0, 0, 0, 0.2);
        border-radius: 10px;
    }
    .logo {
        text-align: center;
        margin-bottom: 0px;
    }
    .logo img {
        max-width: 100px;
    }
    .title {
        text-align: center;
        font-size: 45px;
        font-weight: bold;
        margin-bottom: 20px;
        margin-top: 1px;
    }
    [data-testid="stForm"]{
        width : 380px;
        align-self : center;
    }
    </style>
    """, unsafe_allow_html=True)
    #   st.markdown('<div class="container">', unsafe_allow_html=True)

        # Logo
    st.markdown('<div class="logo"><img src="https://www.nisira.com.pe/images/Logo/logo2.png" alt="Logo"></div>', unsafe_allow_html=True)
        
        # Nombre
    st.markdown('<div class="title" style="letter-spacing: -.015em;"><b class="colorT1" style="color:#01414b;">Bien</b><b class="colorT2" style="color:#fd0;">venido</b></div>', unsafe_allow_html=True)
    with st.form("login"):   
        
        
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")   
        submitted = st.form_submit_button("Login")  
        
        authenticated_user = authenticate(username, password)
        if submitted:  
            if authenticated_user:
                #cookie_controller.set("logged_in",authenticated_user)
                st.session_state['username'] = username   
                st.session_state['logged_in'] = authenticated_user
                #cookies["username"] = username
                
                st.success(f"Bienvenido {authenticated_user[0]}")
                session_token = generate_session_token()
                expires_at = (datetime.now() + timedelta(hours=1)).isoformat()
                expires_at_str = datetime.strptime(expires_at[:-7], '%Y-%m-%dT%H:%M:%S')
                cookie_manager.set("session_token", session_token, expires_at=expires_at_str, key=f"session_{username}")
                #print(cookie_manager)
                st.session_state['session_token'] = cookie_manager.get("session_token")
                #print(st.session_state['session_token'])
                #cookies.save()
                st.rerun()
            else:
                st.error("Usuario o contraseña incorrectos")

def logout():
    cookie_manager.delete("session_token")
    st.session_state['logged_in'] = False
    st.rerun()



if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
    

#st.session_state['logged_in']        
if st.session_state['logged_in']:#st.session_state['logged_in'] and 
        data = get_data_user(st.session_state['username'])
        #print(data)
        st.session_state['profile_img'] = f"data:image/jpeg;base64,{data[1]}"#decoding_avatar(,width=50,height=50)
        st.session_state['empresa_ruc'] = data[2]
        st.session_state['empresa_rubro'] = data[3]
        st.session_state['empresa_name'] = data[4]
        st.session_state['empresa_img'] =decoding_avatar(data[5]) 
        st.session_state['servicio_ip'] = data[6]
        st.session_state['servicio_key'] = data[7]
        st.session_state['servicio_tipo'] = data[8]
        st.session_state['servicio_parquet'] = data[9]
        st.session_state['profile_rol'] = data[10]
        
        
        pg = st.navigation( pages_rol(role=st.session_state['profile_rol'],rubro = st.session_state['empresa_rubro']) | {"Account": account_pages})
        st.logo(st.session_state['empresa_img'])
        st.markdown(
            f"""
            <style>
                
                [data-testid="stSidebarNav"]::before {{
                    content: "{st.session_state['username']}";
                    margin-left: 20px;
                    font-size: 20px;
                    display: block;
                }}
            </style>
            """,
            unsafe_allow_html=True,
        )
        
else:
    pg = st.navigation([st.Page(login)],position="sidebar")
    #print(f"ESTADO DEL LOGIN: {st.session_state['logged_in']}")    
pg.run()

#if __name__ == '__main__':
#    main()


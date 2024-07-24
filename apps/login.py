import streamlit as st
from utils.auth import authenticate

    
def login():
    
    st.title("Login")
    
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        #authenticated_user = authenticate(username, password)
        #print(f"EVENTO DE CLICK EN EL BOTON LOGIN: {authenticated_user}")
        #if authenticated_user:
        
        st.session_state['username'] = "admnisira"    
        st.session_state['logged_in'] = True
        #st.success(f"Bienvenido {admnisira}")
        st.rerun()
            #st.experimental_rerun()
        #else:
        #    st.error("Usuario o contraseña incorrectos")
def login_2():
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
        width : 450px;
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
                
                st.session_state['username'] = username   
                st.session_state['logged_in'] = authenticated_user
                st.success(f"Bienvenido {authenticated_user[0]}")
                st.rerun()
            else:
                st.error("Usuario o contraseña incorrectos")
"""



def login():
    
    st.title("Login")
    
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        authenticated_user = authenticate(username, password)
        if authenticated_user:
            st.session_state['username'] = authenticated_user[0]    
            st.session_state['profile_img'] = authenticated_user[1]
            st.session_state['empresa_ruc'] = authenticated_user[2]
            st.session_state['empresa_rubro'] = authenticated_user[3]
            st.session_state['empresa_name'] = authenticated_user[4]
            st.session_state['empresa_img'] = authenticated_user[5]
            st.session_state['servicio_ip'] = authenticated_user[6]
            st.session_state['servicio_key'] = authenticated_user[7]
            st.session_state['servicio_tipo'] = authenticated_user[8]
            st.session_state['servicio_parquet'] = authenticated_user[9]
            st.session_state['profile_rol'] = authenticated_user[10]
            st.session_state['logged_in'] = True
            st.success(f"Bienvenido {authenticated_user[0]}")
            st.rerun()
            #st.experimental_rerun()
        else:
            st.error("Usuario o contraseña incorrectos")

"""
import streamlit as st
from constants import LOGO_NISIRA
from apps.login import login,login_2

from routes import page_dict,account_pages
from utils.auth import get_data_user
from utils.data_transform import decoding_avatar



def main() -> None:     
    st.set_page_config(
        page_title="Nisira",
        page_icon=LOGO_NISIRA,
        layout="wide",
        initial_sidebar_state="auto",
    )
    
    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False
        
    if 'username' not in st.session_state:
        st.session_state['username'] = ''
    if 'empresa_img' not in st.session_state:
        st.session_state['empresa_img'] = ''
        
        
    if st.session_state['logged_in']:
        data = get_data_user(st.session_state['username'])
        st.session_state['profile_img'] = decoding_avatar(data[1],width=50,height=50)
        st.session_state['empresa_ruc'] = data[2]
        st.session_state['empresa_rubro'] = data[3]
        st.session_state['empresa_name'] = data[4]
        st.session_state['empresa_img'] =decoding_avatar(data[5]) 
        st.session_state['servicio_ip'] = data[6]
        st.session_state['servicio_key'] = data[7]
        st.session_state['servicio_tipo'] = data[8]
        st.session_state['servicio_parquet'] = data[9]
        st.session_state['profile_rol'] = data[10]
        pg = st.navigation( page_dict | {"Account": account_pages})
        st.logo(st.session_state['empresa_img'], icon_image=st.session_state['empresa_img'])
    else:
        pg = st.navigation([st.Page(login_2)])
    #print(f"ESTADO DEL LOGIN: {st.session_state['logged_in']}")    
    pg.run()

if __name__ == '__main__':
    main()


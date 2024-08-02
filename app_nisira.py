import streamlit as st
from constants import LOGO_NISIRA
from apps.login import login_2
from routes import page_dict,account_pages
from utils.auth import get_data_user
from utils.data_transform import decoding_avatar



#def main():     
st.set_page_config(
        page_title="Nisira",
        page_icon=LOGO_NISIRA,
        layout="wide",
        #initial_sidebar_state="auto",
    )

if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False
#if "logged_in" not in st.session_state:
#    if "username" in cookies and cookies["username"]:
#            st.session_state['username'] = cookies["username"]
#            st.session_state['logged_in'] = True
#    else:
#            st.session_state['logged_in'] = False
        
#if 'username' not in st.session_state:
#        st.session_state['username'] = ''
#if 'empresa_img' not in st.session_state:
#        st.session_state['empresa_img'] = ''
        
        
if st.session_state['logged_in']:
        
        data = get_data_user(st.session_state['username'])
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
        
        
        pg = st.navigation( page_dict | {"Account": account_pages})
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
        pg = st.navigation([st.Page(login_2)],position="sidebar")
    #print(f"ESTADO DEL LOGIN: {st.session_state['logged_in']}")    
pg.run()

#if __name__ == '__main__':
#    main()


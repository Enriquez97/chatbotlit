import streamlit as st
from openai import OpenAI
import pandas as pd
import numpy as np



#st.title("Nisira Bot")
LOGO_NISIRA = "https://www.nisira.com.pe/images/Logo/logo2.png"


#fig = px.pie(long_df, labels="nation", values="count", title="Long-Form Input")

st.set_page_config(
    page_title="NisiraBot",
    page_icon=LOGO_NISIRA,
    #layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'About': "Nisira System"
    }
)
#col1, col2= st.columns(2, gap='small')
#with col1:
st.header('Nisira Bot')
    
#with col2:
    #st.image(LOGO_NISIRA,use_column_width = False, width = 80)
ww = st.text_input("")
client = OpenAI(api_key=ww)#ww

# Confiracion del modelo usado
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

# Iniciando el chat
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    avatar_rol = None if message["role"] == "user" else LOGO_NISIRA
    with st.chat_message(message["role"],avatar=avatar_rol):
        st.markdown(message["content"])


if prompt := st.chat_input("Alguna consulta?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
        
    # Display assistant response in chat message container
    with st.chat_message("assistant",avatar=LOGO_NISIRA):
        stream = client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        )
        response = st.write_stream(stream)
    st.session_state.messages.append({"role": "assistant", "content": response})

#st.plotly_chart(fig, theme="streamlit", use_container_width=True)
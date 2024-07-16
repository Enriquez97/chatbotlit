import streamlit as st
import pickle
import os
from dotenv import load_dotenv
from streamlit_extras.add_vertical_space import add_vertical_space
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.llms import OpenAI
from langchain.chains.question_answering import load_qa_chain
from langchain_community.callbacks.manager import get_openai_callback

LOGO_NISIRA = "https://www.nisira.com.pe/images/Logo/logo2.png"


st.markdown(
    """
    <style>
        section[data-testid="stSidebar"] {
            width: 450px !important; # Set the width to your desired value
        }
    </style>
    """,
    unsafe_allow_html=True,
)
#col1, col2= st.columns(2, gap='small')
#with col1:
def list_files_in_directory(directory):
    try:
        files = os.listdir(directory)
        return [file for file in files if os.path.isfile(os.path.join(directory, file))]
    except Exception as e:
        print(f"Error: {e}")
        return []
def pdf_text(archivos):
    string_ =""
    for pdf in archivos:
        pdf_reader = PdfReader(f"./source/{pdf}")
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
            text = text.replace("..", "")
        string_= string_+text
    return string_

texto = pdf_text(list_files_in_directory("./source"))

load_dotenv()



st.header("Chatbot Nisira :robot_face:")
text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len
            )
chunks = text_splitter.split_text(text=texto)
embeddings = OpenAIEmbeddings()
VectorStore = FAISS.from_texts(chunks, embedding=embeddings)
    ##
if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages from history on app rerun
for message in st.session_state.messages:
        avatar_rol = None if message["role"] == "user" else LOGO_NISIRA
        with st.chat_message(message["role"],avatar=avatar_rol):
            st.markdown(message["content"])
    ##

if query:= st.chat_input("Cual es su consulta?"):
        messages = st.container()   
        messages.chat_message("user").write(query)
        docs = VectorStore.similarity_search(query=query, k=3)
 
        llm = OpenAI()#
        chain = load_qa_chain(llm=llm, chain_type="stuff")
        with get_openai_callback() as cb:
            response = chain.run(input_documents=docs, question=query)
            with st.sidebar:
                st.title('Precio por query')    
                st.write(cb)  
                #add_vertical_space(5)
                st.write('Nisira Systems')
        messages.chat_message("assistant",avatar=LOGO_NISIRA).write(response)
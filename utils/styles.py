import streamlit as st

def styles(pt = 3):
    st.markdown("""
        <style>
               .block-container {
                    padding-top: %srem;
                    padding-bottom: 0rem;
                    padding-left: 2.5rem;
                    padding-right: 2.5rem;
                }
                [data-testid="stVerticalBlockBorderWrapper"]{
                    padding: 1px;
                }
                [data-testid="stHeader"]{
                    height: 2.5rem;
                }
                
        </style>
    """%(pt), unsafe_allow_html=True)

def style_sidebar_cb():
    st.markdown(
        """
        <style>
            section[data-testid="stSidebar"] {
                width: 336px !important; # Set the width to your desired value
            }
        </style>
        """,
        unsafe_allow_html=True,
    )
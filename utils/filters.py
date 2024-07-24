import streamlit as st
import pandas as pd

def filter_dataframe(columns_size = [],df = None, name_columns ={}):#, title = None
    #if title:
    columns = st.columns(columns_size)

    dat = []
    for (name, col) ,i in zip(name_columns.items(),range(len(columns_size))) :
        
        with columns[i]:
            value = st.selectbox(name,list(sorted(df[col].unique())),key=col,index=None, placeholder="")
            
            dat.append(value)
        
    return dat
                
                
        #col_title.title("Costos de Campaña :herb:")
        
    
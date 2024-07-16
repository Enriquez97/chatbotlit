import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import plotly.express as px
from menu import menu_with_redirect
from vega_datasets import data
import altair as alt
# Redirect to app.py if not logged in, otherwise show the navigation menu
menu_with_redirect()
st.markdown("""
        <style>
               .block-container {
                    padding-top: 3rem;
                    padding-bottom: 0rem;
                    padding-left: 5rem;
                    padding-right: 5rem;
                }
                [data-testid="stVerticalBlockBorderWrapper"]{
                    padding: 1px;
                }
        </style>
""", unsafe_allow_html=True)
# Verify the user's role
if st.session_state.role not in ["super-admin"]:
    st.warning("You do not have permission to view this page.")
    st.stop()
    
df_bg = pd.read_parquet('./data/finanzas.parquet', engine='pyarrow')
print(df_bg.columns)

col_title, col_formato, col_year, col_trimestre, col_mes, col_moneda = st.columns([5,3,1,1,1,1])
with col_title:
    st.title("Balance de Comprobación")
with col_formato:
    selected_formato = st.selectbox("Formato",list(df_bg.formato.unique()))
with col_year:
    selected_year = st.selectbox("Año", list(sorted(df_bg["Año"].unique())),index=None,placeholder = "")
with col_trimestre:
    selected_trimestre = st.selectbox("Trimestre",list(sorted(df_bg["Trimestre"].unique())),index=None,placeholder = "")
with col_mes:
    selected_mes = st.selectbox("Mes", list(sorted(df_bg["Mes_num"].unique())),index=None,placeholder = "")
with col_moneda:
    selected_moneda = st.selectbox("Moneda", ("PEN","USD"))



moneda = 'saldomof' if selected_moneda == 'PEN' else 'saldomex'

df = df_bg.copy()
activo_df = df[df['titulo1']=='ACTIVO']
activo_p3_df = activo_df.groupby(['titulo1','titulo3'])[[moneda]].sum().sort_values(moneda, ascending=True).reset_index()
pasivo_df = df[df['titulo1']=='PASIVO']
pasivo_p3_df = pasivo_df.groupby(['titulo1','titulo3'])[[moneda]].sum().sort_values(moneda, ascending=True).reset_index()
print(activo_p3_df)
print(activo_p3_df.columns)
"""
fig_2 = px.bar(activo_p3_df, x=moneda, y='titulo3',height=320, orientation='h',)
fig_2.update_traces(hovertemplate='<br>'+"Activo"+': <b>%{y}</b><br>'+selected_moneda+': <b>%{x:,.1f}</b>',cliponaxis=False,)
fig_2.update_layout(xaxis_title='<b>'+selected_moneda+'</b>',yaxis_title='<b>'+"Partida"+'</b>')
fig_2.update_layout(xaxis_tickformat = ',',bargap=0.20,margin=dict(r = 20, t = 40,l=20,b = 20))
fig_2.update_layout(title = "Activo")
fig_2.update_layout(title=dict(text="<b>Activo</b>", font=dict(size=25), automargin=True, yref='paper'))
            
fig_3 = px.bar(pasivo_p3_df, x=moneda, y='titulo3', height=320, orientation='h',)
fig_3.update_traces(hovertemplate='<br>'+"Pasivo"+': <b>%{y}</b><br>'+selected_moneda+': <b>%{x:,.1f}</b>',cliponaxis=False,)
fig_3.update_layout(xaxis_title='<b>'+selected_moneda+'</b>',yaxis_title='<b>'+"Partida"+'</b>')
fig_3.update_layout(xaxis_tickformat = ',',bargap=0.20,margin=dict(r = 20, t = 40,l=20,b = 20))

fig_3.update_layout(title=dict(text="<b>Pasivo</b>", font=dict(size=25), automargin=True, yref='paper'))
"""          


col_activo, col_pasivo = st.columns([6,6])

#col_activo.container(st.plotly_chart(fig_2, theme="streamlit", use_container_width=True))
with col_activo:
    #source = data.barley()
    
    #st.bar_chart(source, x="variety", y="yield", color="site", horizontal=True)
    container = st.container(border=True)
    #container.plotly_chart(fig_2, theme="streamlit", use_container_width=True)
    #st.plotly_chart(fig_2, theme="streamlit", use_container_width=True)
with col_pasivo:
    container = st.container(border=True)
    #container.plotly_chart(fig_3, theme="streamlit", use_container_width=True)

col_1, col_2 = st.columns([6,6])

with col_1:
    container = st.container(border=True)
    container.bar_chart(activo_p3_df, x="titulo3", y=moneda,horizontal=True,height= 320)

with col_2:
    container = st.container(border=True)
    source = data.barley()
    st.bar_chart(source, x="variety", y="yield", color="site", horizontal=True)
    #container.bar_chart(pasivo_p3_df, x="titulo3", y=moneda,horizontal=True,height= 320)
    

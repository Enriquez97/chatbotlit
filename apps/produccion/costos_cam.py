import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import plotly.express as px
import altair as alt
#from menu import menu_with_redirect
from vega_datasets import data
import altair as alt

import folium
from streamlit_folium import st_folium
from folium.map import Popup

from utils.charts_altair import test_altair_chart
from utils.charts_plotly import test_plotly_chart
from utils.filters import filter_dataframe
from utils.styles import styles
# Redirect to app.py if not logged in, otherwise show the navigation menu
#menu_with_redirect()
styles()

    
df = pd.read_parquet('./source/data/costos.parquet', engine='pyarrow')

#data_test = filter_dataframe([4,4,4],df, {"Año":"AÑO_CAMPAÑA","Variedad":"VARIEDAD","Lote":"CONSUMIDOR"})
#print(data_test)

col_title, col_year, col_var, col_lote, col_moneda= st.columns([4,2,2,2,2])
col_title.title("Costos Campaña:herb:")
with col_year:
    select_year = st.selectbox("Año",list(sorted(df["AÑO_CAMPAÑA"].unique())))
    if select_year != None:
        df = df[df["AÑO_CAMPAÑA"]==select_year]
with col_var:
    select_variedad = st.selectbox("Variedad",list(sorted(df["VARIEDAD"].unique())),index=None, placeholder="")
    if select_variedad != None:
        df = df[df["VARIEDAD"]==select_variedad]
with col_lote:   
    selected_lote = st.selectbox("Lote",list(sorted(df["CONSUMIDOR"].unique())),index=None, placeholder="")
    if selected_lote != None:
        df = df[df["CONSUMIDOR"]==selected_lote]

with col_moneda:
    selected_moneda = st.selectbox("Moneda", ("PEN","USD"))

moneda = 'SALDO_MOF' if selected_moneda == 'PEN' else 'SALDO_MEX'


columns_row_1 = st.columns(3)
with columns_row_1[0]:
    culti_df = df.groupby(["CULTIVO"])[[moneda,"AREA_CAMPAÑA"]].sum().sort_values(moneda,ascending=True).reset_index()
    fig = px.bar(culti_df, x=moneda, y="CULTIVO", orientation='h', title= "Costos por Cultivo",height=400)
    event_cultivo = st.plotly_chart(fig, key="iris", on_select="rerun",theme="streamlit")
with columns_row_1[1]:
    variedad_df = df.groupby(["VARIEDAD"])[[moneda,"AREA_CAMPAÑA"]].sum().sort_values(moneda,ascending=True).reset_index()
    fig = px.bar(variedad_df    , x=moneda, y="VARIEDAD", orientation='h', title= "Costos por Variedad",height=400)
    event_variedad = st.plotly_chart(fig, on_select="rerun",theme="streamlit")

with columns_row_1[2]:
    tipo_gasto_df = df.groupby('TIPO')[[moneda]].sum().reset_index()
    fig = px.pie(tipo_gasto_df, values=moneda, names='TIPO', title= "Tipo de Costo")
    fig.update_traces(textposition='inside', textinfo='percent+label')
    event_tipo_gasto = st.plotly_chart(fig, on_select="rerun",theme="streamlit")
    
dff = df[df["POLYGON"].notna()]


def create_first_list_3(x,y):
    coordenadas = eval(x)[0]
    lat = coordenadas[0]
    lon = coordenadas[1]
    return [y,lon,lat]

dff = dff.groupby(["CONSUMIDOR","POLYGON"])[["AREA_CAMPAÑA"]].sum().reset_index()


columns_row_2= st.columns([5,8])


with columns_row_2[0]:
    try:
        dff['first_point_coor'] = dff.apply(lambda x: create_first_list_3(x['POLYGON'],x['CONSUMIDOR']),axis=1)
        locations =list(dff['first_point_coor'].values)
        location_= locations[-1]
        m = folium.Map(location=[location_[1],location_[2]], zoom_start=13)
        for location in locations:
            popup_content = f"""
            <div style="font-size: 26px; font-weight: bold;">
                {location[0]}
            </div>
            """
            popup = Popup(popup_content, max_width=300)
            folium.Marker(
                [location[1], location[2]], 
                popup=location[0],
                icon=folium.Icon(icon="plant-wilt")
            ).add_to(m)
        st_folium(m,width=800,height=400)
    except:
        m = folium.Map(location=[-8.344009690811388, -73.69108684083663], zoom_start=5)
        st_folium(m,width=800,height=400)

with columns_row_2[1]:
    lote_df = df.groupby(["CONSUMIDOR"])[[moneda,"AREA_CAMPAÑA"]].sum().sort_values(moneda,ascending=True).reset_index()
    fig = px.bar(lote_df, x="CONSUMIDOR", y= moneda, orientation='v', title= "Costos por Lote",height=400)
    event_lote = st.plotly_chart(fig, on_select="rerun",theme="streamlit")
    


    
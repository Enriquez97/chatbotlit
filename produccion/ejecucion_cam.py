import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import plotly.express as px
import altair as alt
#from menu import menu_with_redirect
from vega_datasets import data
import altair as alt
from streamlit_dynamic_filters import DynamicFilters

# Redirect to app.py if not logged in, otherwise show the navigation menu
#menu_with_redirect()
st.markdown("""
        <style>
               .block-container {
                    padding-top: 1rem;
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
if st.session_state.role not in ["Test"]:
    st.warning("You do not have permission to view this page.")
    st.stop()
    
df = pd.read_parquet('./data/agricola_.parquet', engine='pyarrow')
print(df.columns)
st.title("Ejecución de Campaña :herb:")

columns = st.columns(5)
with columns[0]:
    select_cultivo =st.selectbox("Cultivo",list(sorted(df["CULTIVO"].unique())))
    if select_cultivo != None:
        df = df[df["CULTIVO"]==select_cultivo]
        
with columns[1]:
    select_recurso =st.selectbox("Recurso",list(sorted(df["DSCVARIABLE"].unique())))
    if select_recurso != None:
        df = df[df["DSCVARIABLE"]==select_recurso]
        
with columns[2]:
    selected_campaña =st.selectbox("Campaña-Cultivo",list(sorted(df["AÑO_CULTIVO"].unique())),index=None, placeholder="")
    if selected_campaña != None:
        df = df[df["AÑO_CULTIVO"]==selected_campaña]
with columns[3]:
    selected_variedad =st.selectbox("Variedad",list(sorted(df["VARIEDAD"].unique())),index=None, placeholder="")
    if selected_variedad != None:
        df = df[df["VARIEDAD"]==selected_variedad]
with columns[4]:
    selected_lote = st.selectbox("Lote",list(sorted(df["CONSUMIDOR"].unique())),index=None, placeholder="")
    if selected_lote != None:
        df = df[df["CONSUMIDOR"]==selected_lote]

dff = df.groupby(["AÑO_CULTIVO","DSCVARIABLE"])[["CANTIDAD"]].sum().reset_index()
st_df = df.groupby(["AÑO_CULTIVO","week"])[["CANTIDAD"]].sum().reset_index()
#st.dataframe(df)
c = (
   alt.Chart(dff)
   .mark_bar()
   .encode(x="AÑO_CULTIVO", 
           y="CANTIDAD",#alt.Y('Partidas').sort('-x'),
           #color = "DSCVARIABLE",
           text="CANTIDAD", 
           tooltip=["AÑO_CULTIVO", "CANTIDAD"],
           
    )
   .properties(
    title=f'Cultivos por Campaña ({select_cultivo})',
    height=400
    )
)


hover = alt.selection_single(
    fields=["week"],
    nearest=True,
    on="mouseover",
    empty="none",
)


d = (
   alt.Chart(st_df)
   .mark_line()
   .encode(x="week", 
           y="CANTIDAD",#alt.Y('Partidas').sort('-x'),
           color = alt.Color('AÑO_CULTIVO').title("Campaña"),
           text="CANTIDAD", 
           tooltip=["AÑO_CULTIVO","week", "CANTIDAD"],
           
    )
   .properties(
    title=f'{select_recurso} por Semana',
    height=400
    )
)
points = d .transform_filter(hover).mark_circle(size=65)

tooltips = (
    alt.Chart(st_df)
    .mark_rule()
    .encode(
        x="week",
        y="CANTIDAD",
        opacity=alt.condition(hover, alt.value(0.3), alt.value(0)),
        tooltip=[
            alt.Tooltip("week", title="Semana"),
            alt.Tooltip("AÑO_CULTIVO", title="Campaña"),
            alt.Tooltip("CANTIDAD", title="Cantidad"),
        ],
    )
    .add_selection(hover)
)
data_layer = d + points + tooltips
columns_graph = st.columns(2)
with columns_graph[0]:
    st.altair_chart(c, use_container_width=True,theme="streamlit")

with columns_graph[1]:
    st.altair_chart(data_layer, use_container_width=True,theme="streamlit")
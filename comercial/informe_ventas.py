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
    
df_bg = pd.read_parquet('./data/finanzas.parquet', engine='pyarrow')

df_bg["Año"] = df_bg["Año"].astype("string")
df_bg["Trimestre"] = df_bg["Trimestre"].astype("string")
df_bg["Mes_"] = df_bg["Mes_"].astype("string")

st.title("Balance de Comprobación")
col_formato,col_year,col_tri,col_mes,col_moneda= st.columns([3,2,2,2,1])

with col_formato:
    selected_formato =st.selectbox("Formato",list(sorted(df_bg["formato"].unique())))
df_bg = df_bg[df_bg['formato'] == selected_formato]
with col_year:
    selected_year =st.selectbox("Año",list(sorted(df_bg["Año"].unique())),index=None, placeholder="")
    if selected_year != None:
        df_bg = df_bg[df_bg['Año'] == selected_year]
with col_tri:
    selected_tri =st.selectbox("Trimestre",list(sorted(df_bg["Trimestre"].unique())),index=None, placeholder="")
    if selected_tri != None:
        df_bg = df_bg[df_bg['Trimestre'] == selected_tri]
with col_mes:
    selected_mes =st.selectbox("Mes",list(sorted(df_bg["Mes_"].unique())),index=None, placeholder="")
    if selected_mes != None:
        df_bg = df_bg[df_bg['Mes_'] == selected_mes]
    #dynamic_filters  = DynamicFilters(df=df_bg, filters=['Año', 'Trimestre', 'Mes_'])
    #dynamic_filters .display_filters(location='columns', num_columns=3,gap="small")
with col_moneda:
    selected_moneda = st.selectbox("Moneda", ("PEN","USD"))


moneda = 'saldomof' if selected_moneda == 'PEN' else 'saldomex'

#######################################
df = df_bg.copy()

activo_df = df[df['titulo1']=='ACTIVO']
activo_p3_df = activo_df.groupby(['titulo1','titulo3'])[[moneda]].sum().sort_values(moneda, ascending=True).reset_index()
activo_p3_df = activo_p3_df.rename(columns = {"titulo3":"Partidas",moneda:selected_moneda})


pasivo_df = df[df['titulo1']=='PASIVO']
pasivo_p3_df = pasivo_df.groupby(['titulo1','titulo3'])[[moneda]].sum().sort_values(moneda, ascending=True).reset_index()
pasivo_p3_df = pasivo_p3_df.rename(columns = {"titulo3":"Partidas",moneda:selected_moneda})

act_pas_corr_df = df[df['titulo2'].isin(['ACTIVO CORRIENTE','PASIVO CORRIENTE','ACTIVOS CORRIENTES','PASIVOS CORRIENTES'])]
corr_pivot_df = pd.pivot_table(act_pas_corr_df,index=['periodo','Año', 'Mes', 'Mes_num', 'Mes_', 'Trimestre'],values= moneda,columns='titulo2',aggfunc='sum').reset_index()
try:
    corr_pivot_df['Fondo de Maniobra'] = corr_pivot_df['ACTIVO CORRIENTE'] - corr_pivot_df['PASIVO CORRIENTE']
except:
    corr_pivot_df['Fondo de Maniobra'] = corr_pivot_df['ACTIVO CORRIENTE'] - corr_pivot_df['PASIVOS CORRIENTES']
fondo_mani_df = corr_pivot_df.groupby(['Mes_num','Mes_'])[['Fondo de Maniobra']].sum().sort_values('Mes_num',ascending = True).reset_index()

c = (
   alt.Chart(activo_p3_df)
   .mark_bar()
   .encode(x=selected_moneda, 
           y=alt.Y('Partidas').sort('-x'),
           text=selected_moneda, 
           tooltip=["Partidas", alt.Tooltip(f'{selected_moneda}:Q', format=',.2f')],
           
    )
   .properties(
    title='ACTIVO',
    height=350
    )
)
c = c + c.mark_text(align='left', dx=1).encode(text=alt.Text(f'{selected_moneda}:Q', format=',.0f'))

d = (
   alt.Chart(pasivo_p3_df)
   .mark_bar()
   .encode(x=selected_moneda, 
           y=alt.Y('Partidas').sort('-x'),
           text=selected_moneda, 
           tooltip=["Partidas", alt.Tooltip(f'{selected_moneda}:Q', format=',.2f')],
           
    )
   .properties(
    title='PASIVO',
    height=350
    )
)
d = d + d.mark_text(align='left', dx=1).encode(text=alt.Text(f'{selected_moneda}:Q', format=',.0f'))


custom_order = ["Ene","Feb","Mar","Abr","May","Jun","Jul","Ago","Set","Oct","Nov","Dic"]
g = (
   alt.Chart(fondo_mani_df) 
   .mark_bar()
   .encode(x=alt.X('Mes_:N', title="Mes", sort= custom_order), 
           y="Fondo de Maniobra",
           text="Fondo de Maniobra", 
           tooltip=[ "Mes_",alt.Tooltip(f'{"Fondo de Maniobra"}:Q', format=',.2f')],
           
    )
   .properties(
    title='Fondo de Maniobra'
    )
)
g = g + g.mark_text(align='center',baseline='bottom',dy=-5).encode(text=alt.Text(f'{"Fondo de Maniobra"}:Q', format=',.0f'))

col_activo, col_pasivo = st.columns([6,6])
col_activo.altair_chart(c, use_container_width=True,theme="streamlit")
col_pasivo.altair_chart(d, use_container_width=True,theme="streamlit")

st.altair_chart(g, use_container_width=True,theme="streamlit")

st.dataframe(df)
#dynamic_filters.display_df()


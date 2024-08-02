import streamlit as st
import pandas as pd
import numpy as np

import plotly.express as px
import altair as alt
from utils.styles import styles
from utils.api import APIConnector,send_get_dataframe
from utils.data_transform import *
from utils.charts_altair import ALTAIR
from apps.login import cookies


class Comercial:
    #def __init__(self, ip: st.session_state['servicio_ip'], token : st.session_state['servicio_key']):#, data_login: dict
    #    self.ip = ip
    #    self.token = token
    def informe_ventas():
        cookies['username'] = st.session_state['username']
        cookies.save()
        styles(pt=1)    
        
        if st.session_state['servicio_ip']:
            
            #dataframe = APIConnector(st.session_state['servicio_ip'],st.session_state['servicio_key']).send_get_dataframe(endpoint="nsp_rpt_ventas_detallado")
            dataframe = send_get_dataframe(ip = st.session_state['servicio_ip'],token=st.session_state['servicio_key'], endpoint="nsp_rpt_ventas_detallado")
            df = transform_nsp_rpt_ventas_detallado(dataframe)
            print(df.columns)
            
            st.title("Informe de Ventas")
            columns_filters =  st.columns([1,2,2,2,2,2,1])
            with columns_filters[0]:
                selected_year =st.selectbox("Año",list(sorted(df["Año"].unique())))
                if selected_year != None:
                    df = df[df['Año'] == selected_year]
            with columns_filters[1]:
                selected_cliente =st.selectbox("Cliente",list(sorted(df["Cliente"].unique())),index=None, placeholder="")
                if selected_cliente != None:
                    df = df[df['Cliente'] == selected_cliente]
            with columns_filters[2]:
                selected_tipo_venta =st.selectbox("Tipo de Venta",list(sorted(df["Tipo de Venta"].unique())),index=None, placeholder="")
                if selected_tipo_venta != None:
                    df = df[df['Tipo de Venta'] == selected_tipo_venta]
            with columns_filters[3]:
                selected_grupo_producto =st.selectbox("Grupo de Producto",list(sorted(df["Grupo Producto"].unique())),index=None, placeholder="")
                if selected_grupo_producto != None:
                    df = df[df['Grupo Producto'] == selected_grupo_producto]
            with columns_filters[4]:
                selected_grupo_cliente=st.selectbox("Grupo de Cliente",list(sorted(df["Grupo Cliente"].unique())),index=None, placeholder="")
                if selected_grupo_cliente != None:
                    df = df[df['Grupo Cliente'] == selected_grupo_cliente]
            with columns_filters[5]:
                selected_producto =st.selectbox("Producto",list(sorted(df["Producto"].unique())),index=None, placeholder="")
                if selected_producto != None:
                    df = df[df['Producto'] == selected_producto]
            with columns_filters[6]:
                selected_moneda = st.selectbox("Moneda", ("PEN","USD"))
                importe = "Importe Soles" if selected_moneda == "PEN" else "Importe Dolares"
            
            productos_df_20=df.groupby(['Producto','Grupo Producto','Subgrupo Producto'])[[importe]].sum().sort_values(importe,ascending=True).tail(20).reset_index()
            vendedor_df = df.groupby(['Vendedor'])[[importe]].sum().sort_values(importe,ascending=True).reset_index()
            departamento_df = df.groupby(['Departamento'])[[importe]].sum().sort_values(importe,ascending=True).reset_index()
            #meses_df_12 = df.groupby(['Mes','Mes Num'])[[importe]].sum().reset_index().sort_values('Mes Num',ascending=True).reset_index()
            fecha_df =df.groupby(["Fecha"])[[importe]].sum().reset_index()
            #meses_df_12['Porcentaje']=(meses_df_12[importe]/meses_df_12[importe].sum())*100
            #meses_df_12['Porcentaje']=meses_df_12['Porcentaje'].map('{:,.1f}%'.format)
            grupo_p_df = df.groupby(["Grupo Producto"])[[importe]].sum().sort_values(importe,ascending=True).reset_index()
            grupo_c_df = df.groupby(["Grupo Cliente"])[[importe]].sum().sort_values(importe,ascending=True).reset_index()
            
            col_row_1 = st.columns([5,3.5,3.5])
            with col_row_1[0]:
                ALTAIR(dataframe = productos_df_20,titulo = "Ranking 20 Productos",height = 350).bar(x = importe,y = "Producto",horizontal=True)
            with col_row_1[1]:
                ALTAIR(dataframe = vendedor_df,titulo = "Ventas por Vendedor",height = 350).pie(value = importe, color = "Vendedor")
            with col_row_1[2]:
                ALTAIR(dataframe = departamento_df,titulo = "Ventas por Departamento",height = 350).pie(value = importe, color = "Departamento")
           
            col_row_2 = st.columns([4.5,7.5])
            with col_row_2[0]:
                fig = px.line(fecha_df, x="Fecha", y=importe, title='Ventas por Fecha',height=380)
                fig.update_layout(autosize=True,margin=dict(t = 50,b=20 ) )#l = left, r = 40, b= 40, 
                st.plotly_chart(fig, theme="streamlit")
                
            
            with col_row_2[1]: 
                fig_1 = px.bar(grupo_p_df, x='Grupo Producto', y= importe,height=380, title = "Ventas por Grupo de Producto")
                fig_1.update_layout(autosize=True,margin=dict(t = 40))
                fig_2 = px.bar(grupo_c_df, x='Grupo Cliente', y= importe,height=380, title = "Ventas por Grupo de Cliente")
                fig_2.update_layout(autosize=True,margin=dict(t = 40, ),bargap=0.7)
                #ALTAIR(dataframe = grupo_p_df,titulo = "Ventas por Mes",height = 400).bar(x = "Grupo Producto" ,y = importe,horizontal=False, sort=True,mark_text=False)
                tab1, tab2 = st.tabs(["All-Grupo Producto", "All-Grupo Cliente"])
                with tab1:
                    st.plotly_chart(fig_1, theme="streamlit")
                with tab2:
                    st.plotly_chart(fig_2, theme="streamlit")
            #st.dataframe(df)
        else:
            st.title("Error")
        
    #df_bg = pd.read_parquet('./source/data/finanzas.parquet', engine='pyarrow')

import streamlit as st
import pandas as pd
import numpy as np
import datetime
from datetime import timedelta,datetime,date
from utils.styles import styles
from utils.api import send_get_dataframe
from utils.data_transform import *
from utils.charts_altair import ALTAIR
from utils.charts_plotly import *

class Logistica:
    
    def stocks():
        styles(pt=3)  
        if st.session_state['servicio_ip']:
            dataframe = send_get_dataframe(ip = st.session_state['servicio_ip'],token=st.session_state['servicio_key'], endpoint="nsp_stocks")
            #dataframe = APIConnector(st.session_state['servicio_ip'],st.session_state['servicio_key']).send_get_dataframe(endpoint="nsp_stocks")
            df = transform_nsp_stocks(dataframe)
            print(df.columns)
            
            col_row_head = st.columns([6,1,2,2,1])
            with col_row_head[0]:
                st.title("Stocks")
            with col_row_head[1]:
                selected_year =st.selectbox("Año",list(sorted(df["Año"].unique())),index=None, placeholder="")
                if selected_year != None:
                    df = df[df['Año'] == selected_year]
            with col_row_head[2]:
                selected_gp =st.selectbox("Grupo Producto",list(sorted(df["Grupo Producto"].unique())),index=None, placeholder="")
                if selected_gp != None:
                    df = df[df['Grupo Producto'] == selected_gp]
            with col_row_head[3]:
                selected_ra =st.selectbox("Rango antigüedad",list(sorted(df["Rango antigüedad del stock"].unique())),index=None, placeholder="")
                if selected_ra != None:
                    df = df[df['Rango antigüedad del stock'] == selected_ra]
            with col_row_head[4]:
                selected_moneda = st.selectbox("Moneda", ("PEN","USD"))
                valorizado = "Stock Valorizado Soles" if selected_moneda == "PEN" else "Stock Valorizado Dolares"
            
            ## AGRUPACIONES
            moneda = 'Soles' if selected_moneda == 'PEN' else 'Dolares'
            gp_dff = df.groupby(["Grupo Producto"])[[valorizado]].sum().reset_index() 
            top_10_df= df.groupby(['Producto'])[[valorizado]].sum().sort_values([valorizado],ascending = True).tail(10).reset_index()   
            rango_stock_df = df.groupby(['Rango antigüedad del stock'])[[valorizado]].sum().sort_values(['Rango antigüedad del stock']).reset_index()
            rango_stock_count_df = df.groupby(['Rango antigüedad del stock'])[['Producto']].count().sort_values(['Rango antigüedad del stock']).reset_index()
            #pr_dff = df.groupby([""])[[valorizado]].sum().reset_index() 
            fig_stock_var_y2 = figure_stock_var_y2(df=df, height = 330, moneda = moneda,title="Stock Valorizado y N° Items por mes y año")
            fig_pie_stock = pie_(df = rango_stock_df,label_col = 'Rango antigüedad del stock', value_col = valorizado,title = "Stock Valorizado segun Antigüedad", textinfo = 'percent+label+value' , textposition = 'inside',height = 330, showlegend = False, textfont_size = 12, hole = 0,)
            fig_pie_stock_count = pie_(df = rango_stock_count_df,label_col = 'Rango antigüedad del stock', value_col = 'Producto',title = "Nro Items segun Antigüedad", textinfo = 'percent+label+value' , textposition = 'inside',height = 330, showlegend = False, textfont_size = 12, hole = 0,)
            fig_bar_realative_ventas = figure_bar_relative(df = df, height = 330, eje_color = 'ABC Ventas', title = 'Porcentaje Stock por ABC Ventas', var_numerico = valorizado)
            fig_bar_realative_stock =figure_bar_relative(df = df, height = 330, eje_color = 'ABC Stock', title = 'Porcentaje Stock por ABC Stock Valorizado', var_numerico = valorizado)
            ### END AGRUPACIONES
            col_row_1 = st.columns([7,5])
            
            with col_row_1[0]:
                #ALTAIR(dataframe = gp_dff,titulo = "Stock Valorizado por Grupo de Producto",height = 350).bar(x = valorizado,y = "Grupo Producto",horizontal=True)
                st.plotly_chart(fig_stock_var_y2,theme="streamlit")
            with col_row_1[1]:
                ALTAIR(dataframe = gp_dff,titulo = "Stock Valorizado por Grupo de Producto",height = 330).bar(x = valorizado,y = "Grupo Producto",horizontal=True)
            col_row_3 = st.columns(2)
            col_row_3[0].plotly_chart(fig_bar_realative_ventas,theme="streamlit")
            col_row_3[1].plotly_chart(fig_bar_realative_stock,theme="streamlit")
            
            col_row_2 = st.columns(3)
            with col_row_2[0]:
                ALTAIR(dataframe = top_10_df,titulo = "Top 10 Productos por Stock Valorizado",height = 350).bar(x = valorizado,y = "Producto",horizontal=True)
            with col_row_2[1]:
                st.plotly_chart(fig_pie_stock,theme="streamlit")
            with col_row_2[2]:
                st.plotly_chart(fig_pie_stock_count,theme="streamlit")
    def estado_inventario():
        styles(pt=1)  
        if st.session_state['servicio_ip']:
            dataframe = send_get_dataframe(
                ip = st.session_state['servicio_ip'],
                token=st.session_state['servicio_key'], 
                endpoint="STOCKALMVAL",
                params= { 'EMPRESA':'001','SUCURSAL':'','ALMACEN': '','FECHA':str(datetime.now())[:10].replace('-', ""), 'IDGRUPO':'','SUBGRUPO':'','DESCRIPCION':'','IDPRODUCTO':''}
            )
            #dataframe = APIConnector(st.session_state['servicio_ip'],st.session_state['servicio_key']).send_get_dataframe(endpoint="nsp_stocks")
            df = transform_stockalmval(dataframe)
            df['Última Fecha Ingreso']=df['Última Fecha Ingreso'].apply(lambda a: pd.to_datetime(a).date())
            #print(df.columns)
            first_date =str(df['Última Fecha Ingreso'].min())
            first_datetype =date(int(first_date[:4]),int(first_date[-5:-3]),int(first_date[-2:]))
            last_datetype = datetime.now()
            st.title("Estado de Inventario")
            print(df.info())
            col_row_1 = st.columns(6)
            with col_row_1[0]:
                selected_date_first = st.date_input(label = "Fecha Inicio", value = first_datetype, min_value = first_datetype, max_value=last_datetype)
                if selected_date_first != None:
                    df = df[(df['Última Fecha Ingreso']>=selected_date_first)]
            with col_row_1[1]:
                selected_date_last = st.date_input(label = "Fecha Final", value = last_datetype, min_value = first_datetype, max_value=last_datetype)
                if selected_date_last != None:
                    df = df[(df['Última Fecha Ingreso']<=selected_date_last)]
            #df = df[(df['Última Fecha Ingreso']>=selected_date_first)&(df['Última Fecha Ingreso']<=selected_date_last)]
            
            
            with col_row_1[2]:
                selected_almacen = st.selectbox("Almacén",list(sorted(df["Almacén"].unique())),index=None, placeholder="")
                if selected_almacen != None:
                    df = df[df["Almacén"]==selected_almacen]
            with col_row_1[3]:
                selected_tipo = st.selectbox("Tipo",list(sorted(df["Tipo"].unique())),index=None, placeholder="",disabled=True)
                if selected_tipo != None:
                    df = df[df["Tipo"]==selected_tipo]
            
            
            with col_row_1[4]:
                selected_grupo = st.selectbox("Grupo",list(sorted(df["Grupo"].unique())),index=None, placeholder="",disabled=True)   
                if selected_tipo != None:
                    df = df[df["Grupo"]==selected_grupo]     
            with col_row_1[5]:
                selected_moneda = st.selectbox("Moneda", ("PEN","USD"))
                moneda = 'Importe Soles' if selected_moneda == 'PEN' else 'Importe Dolares'
                
            pie_estado_inv_dff = df.groupby(['Estado Inventario'])[['Tipo']].count().reset_index()
            pie_estado_inv_dff = pie_estado_inv_dff.rename(columns = {'Tipo':'Número de Registros'})
            responsable_df = df.groupby(['Responsable Ingreso'])[['Tipo']].count().sort_values('Tipo',ascending=True).reset_index()
            responsable_df = responsable_df.rename(columns = {'Tipo':'Número de Registros'})
            table_dff = df[['Sucursal', 'Almacén', 'Tipo','Grupo','Sub Grupo','Producto','Responsable Ingreso','Última Fecha Ingreso', 'Última Fecha Salida','Duracion_Inventario','Stock',moneda]]
            
            #st.dataframe(df,hide_index = True)   
            columns_row_1 = st.columns([8,4])
            with columns_row_1[0]:
                tab1,tab2,tab3,tab4 = st.tabs(["Sucursal", "Almacén","Tipo","Grupo"])
                with tab1:
                    st.plotly_chart(figure_stock_alm_y2(df = df, height = 300 , moneda = moneda, tipo = "Sucursal"),theme="streamlit")
                with tab2:
                    st.plotly_chart(figure_stock_alm_y2(df = df, height = 300 , moneda = moneda, tipo = "Almacén"),theme="streamlit")
                with tab3:
                    st.plotly_chart(figure_stock_alm_y2(df = df, height = 300 , moneda = moneda, tipo = "Tipo"),theme="streamlit")   
                with tab4:
                    st.plotly_chart(figure_stock_alm_y2(df = df, height = 300 , moneda = moneda, tipo = "Grupo"),theme="streamlit") 
                st.dataframe(table_dff,hide_index = True, height=330)
            with columns_row_1[1]:
                #ALTAIR(pie_estado_inv_dff,"dsds",height=330).pie(value="Número de Registros",color="Estado Inventario")
                st.plotly_chart( pie_(df = pie_estado_inv_dff,label_col = 'Estado Inventario', value_col = "Número de Registros",title = "Estado", textinfo = 'percent+label' , textposition = 'outside',height = 370, showlegend = False, textfont_size = 12, hole = .6),theme="streamlit") 
                ALTAIR(dataframe = responsable_df,titulo = "Responsable",height = 350).bar(x = 'Número de Registros',y = "Responsable Ingreso",horizontal=True)
import streamlit as st
import pandas as pd
import numpy as np
from constants import MESES_ORDER
import plotly.express as px
import altair as alt
from utils.styles import styles
from utils.api import APIConnector,send_get_dataframe
from utils.data_transform import *
from utils.charts_altair import ALTAIR
from utils.charts_plotly import *



class Comercial:
    #def __init__(self, ip: st.session_state['servicio_ip'], token : st.session_state['servicio_key']):#, data_login: dict
    #    self.ip = ip
    #    self.token = token
    def informe_ventas():
        styles(pt=1)    
        
        if st.session_state['servicio_ip']:
            #st.session_state['servicio_parquet'] = data[9]
            #dataframe = APIConnector(st.session_state['servicio_ip'],st.session_state['servicio_key']).send_get_dataframe(endpoint="nsp_rpt_ventas_detallado")
            if st.session_state['servicio_parquet'] == True:
                dataframe =  pd.read_parquet(f"http://{st.session_state['servicio_ip']}:3005/read-parquet/nsp_rpt_ventas_detallado.parquet")
            else:
                dataframe = send_get_dataframe(ip = st.session_state['servicio_ip'],token=st.session_state['servicio_key'], endpoint="nsp_rpt_ventas_detallado")
            df = transform_nsp_rpt_ventas_detallado(dataframe)
            
            
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
            productos_df_20[importe] = productos_df_20[importe].astype(float)
            vendedor_df = df.groupby(['Vendedor'])[[importe]].sum().sort_values(importe,ascending=True).reset_index()
            vendedor_df[importe] = vendedor_df[importe].astype(float)
            departamento_df = df.groupby(['Departamento'])[[importe]].sum().sort_values(importe,ascending=True).reset_index()
            departamento_df[importe] = departamento_df[importe].astype(float)
            #meses_df_12 = df.groupby(['Mes','Mes Num'])[[importe]].sum().reset_index().sort_values('Mes Num',ascending=True).reset_index()
            fecha_df =df.groupby(["Fecha"])[[importe]].sum().reset_index()
            #meses_df_12['Porcentaje']=(meses_df_12[importe]/meses_df_12[importe].sum())*100
            #meses_df_12['Porcentaje']=meses_df_12['Porcentaje'].map('{:,.1f}%'.format)
            grupo_p_df = df.groupby(["Grupo Producto"])[[importe]].sum().sort_values(importe,ascending=True).reset_index()
            subgrupo_p_df = df.groupby(["Subgrupo Producto"])[[importe]].sum().sort_values(importe,ascending=True).reset_index()
            grupo_c_df = df.groupby(["Grupo Cliente"])[[importe]].sum().sort_values(importe,ascending=True).reset_index()
            
            print(productos_df_20.info())
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
                
                fig_3 = px.bar(subgrupo_p_df, x='Subgrupo Producto', y= importe,height=380, title = "Ventas por Subgrupo de Cliente")
                fig_3.update_layout(autosize=True,margin=dict(t = 40, ),bargap=0.5)
                #ALTAIR(dataframe = grupo_p_df,titulo = "Ventas por Mes",height = 400).bar(x = "Grupo Producto" ,y = importe,horizontal=False, sort=True,mark_text=False)
                tab1, tab2, tab3 = st.tabs(["All-Grupo Producto","All-Subgrupo Producto", "All-Grupo Cliente"])
                with tab1:
                    st.plotly_chart(fig_1, theme="streamlit")
                with tab2:
                    st.plotly_chart(fig_3, theme="streamlit")
                with tab3:
                    st.plotly_chart(fig_2, theme="streamlit")
            #st.dataframe(df)
        else:
            st.title("Error")
    
    def comparativo_ventas():
        styles(pt=1)    
        
        if st.session_state['servicio_ip']:
            
            if st.session_state['servicio_parquet'] == True:
                dataframe =  pd.read_parquet(f"http://{st.session_state['servicio_ip']}:3005/read-parquet/nsp_rpt_ventas_detallado.parquet")
            else:
                dataframe = send_get_dataframe(ip = st.session_state['servicio_ip'],token=st.session_state['servicio_key'], endpoint="nsp_rpt_ventas_detallado")
            df = transform_nsp_rpt_ventas_detallado(dataframe)
            df["Año"] = df["Año"].astype("string")
            
            head_filters =  st.columns([6,3,1])
            head_filters[0].title("Comparativo de Ventas")
            with head_filters[1]:
                selected_year =st.multiselect("Año",list(sorted(df["Año"].unique())),placeholder = "")
                if len(selected_year) > 0:
                    df = df[df['Año'].isin(selected_year)]
            with head_filters[2]:
                selected_moneda = st.selectbox("Moneda", ("PEN","USD"))
                importe = "Importe Soles" if selected_moneda == "PEN" else "Importe Dolares"
                    
                    
            columns_filters =  st.columns([2,2,2,2])
            with columns_filters[0]:
                selected_sucursal =st.selectbox("Sucursal",list(sorted(df["Sucursal"].unique())),index=None, placeholder="")
                if selected_sucursal != None:
                    df = df[df['Sucursal'] == selected_sucursal]
            with columns_filters[1]:
                selected_tipoventa =st.selectbox("Tipo de Venta",list(sorted(df["Tipo de Venta"].unique())),index=None, placeholder="")
                if selected_tipoventa != None:
                    df = df[df['Tipo de Venta'] == selected_tipoventa]
            with columns_filters[2]:
                selected_grupo_producto =st.selectbox("Grupo de Producto",list(sorted(df["Grupo Producto"].unique())),index=None, placeholder="")
                if selected_grupo_producto != None:
                    df = df[df['Grupo Producto'] == selected_grupo_producto]
            with columns_filters[3]:
                selected_grupo_cliente =st.selectbox("Grupo de Cliente",list(sorted(df["Grupo Cliente"].unique())),index=None, placeholder="")
                if selected_grupo_cliente != None:
                    df = df[df['Grupo Cliente'] == selected_grupo_cliente]
            
            
            #st.toast(str(df.shape[0]), icon='🎉')
            genre = st.radio(
                "Variable de Análisis",
                ["Año", "Tipo de Venta", "Grupo Producto","Grupo Cliente","Sucursal","Vendedor","Pais","Departamento","Tipo de Condicion"],
                index=True,
                horizontal=True
            )
            if genre == "Año":
                dff = df.groupby(["Año","Mes"])[[importe]].sum().reset_index()
                fig = px.bar(dff, x="Mes", y=importe,color='Año', barmode='group',height=300,category_orders = {"Mes": MESES_ORDER},title=f"Ventas por Año-Meses")
            else:
                dff = df.groupby(["Año",genre])[[importe]].sum().reset_index()
                fig = px.bar(dff, x='Año', y=importe,color=genre, barmode='group',height=300,title=f"{genre} por Año")
                
            fig.update_xaxes(type='category')
            fig.update_layout(yaxis_tickformat = ',')
            fig.update_layout(margin=dict(r = 20, b = 40, t = 50))
            event = st.plotly_chart(fig,theme="streamlit",key="iris", on_select="rerun") 
            col_graphs =  st.columns([6,3,3])
            try:
                element_filter = event["selection"]["points"][0]["legendgroup"]
                event_df_line = df.groupby(["Año","Mes","Mes Num",genre])[[importe]].sum().sort_values("Mes Num").reset_index()
                event_df_line = event_df_line[event_df_line[genre]==element_filter]
                event_df_pie = event_df_line.groupby(["Año"])[[importe]].sum().sort_values(importe).reset_index()
                with col_graphs[0]:
                    
                    fig_line = px.line(event_df_line, x="Mes", y=importe, color="Año",title=f"{genre} - {element_filter}",height=300,category_orders = {"Mes": MESES_ORDER})
                    fig_line.update_layout(autosize=True,margin=dict(t = 50,b=20 ) )#l = left, r = 40, b= 40, 
                    fig_line.update_layout(hovermode="x unified",yaxis_tickformat = ',')
                    fig_line.update_layout(legend=dict(orientation="h",yanchor="bottom",y=1.02, xanchor="right",x=1),legend_title="")
                        
                    st.plotly_chart(fig_line, theme="streamlit")
                        
                with col_graphs[1]:
                    #ALTAIR(dataframe = event_df_pie,titulo = element_filter,height = 350).pie(value = importe, color = "Año")
                    st.plotly_chart(pie_(df=event_df_pie,label_col="Año",value_col=importe,height=300,title=element_filter,title_font_size = 12,hole=.3,showlegend=False,t=30, b=10, l=10, r=10), theme="streamlit")
                    
            except:
                pass
            st.dataframe(df,hide_index=True)

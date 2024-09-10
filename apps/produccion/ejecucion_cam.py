import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import plotly.express as px
import altair as alt
from utils.data_transform import *
import altair as alt
from utils.api import send_get_dataframe,read_apis_sync
from utils.styles import styles
import folium
from streamlit_folium import st_folium
from folium.map import Popup


class Produccion:
    def ejecucion_campania():
        styles(pt=1)
        if st.session_state['servicio_ip']:
            if st.session_state['empresa_name'] =="NISIRA":
                df = pd.read_parquet('./source/data/agricola_.parquet', engine='pyarrow')
            else:
                consumidores_df=send_get_dataframe(ip = st.session_state['servicio_ip'],token=st.session_state['servicio_key'], endpoint="nsp_datos_consumidores")
                variedad_df=send_get_dataframe(ip = st.session_state['servicio_ip'],token=st.session_state['servicio_key'], endpoint="nsp_datos_variedades_cultivos")
                cultivos_df=send_get_dataframe(ip = st.session_state['servicio_ip'],token=st.session_state['servicio_key'], endpoint="nsp_datos_cultivos")
                fertilizacion_df=send_get_dataframe(ip = st.session_state['servicio_ip'],token=st.session_state['servicio_key'], endpoint="nsp_datos_plan_fertilizacion")
                df = cleanVariablesAgricolas(consumidores_df,variedad_df,cultivos_df,fertilizacion_df)
            #df = pd.read_parquet('./source/data/agricola_.parquet', engine='pyarrow')
            
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

            #st.dataframe(df)
            multi_selection = alt.selection_point(name="multi", toggle=True, encodings=["x"])
            c = (
            alt.Chart(dff)
            .mark_bar()
            .encode(x="AÑO_CULTIVO", 
                    y="CANTIDAD",#alt.Y('Partidas').sort('-x'),
                    color = alt.condition(multi_selection, "AÑO_CULTIVO:N", alt.value("lightgray"),),
                    text="CANTIDAD", 
                    tooltip=["AÑO_CULTIVO", "CANTIDAD"],
                    
                )
            .properties(
                title=f'Cultivos por Campaña ({select_cultivo})',
                height=400
                ).add_params(multi_selection)
            )



            columns_graph = st.columns(2)
            with columns_graph[0]:
                event_data = st.altair_chart(c, use_container_width=True,theme="streamlit",on_select="rerun")
                
            with columns_graph[1]:
                
                hover = alt.selection_single(
                fields=["week"],
                nearest=True,
                on="mouseover",
                empty="none",
                )
                ## df pross
                st_df = df.groupby(["AÑO_CULTIVO","week"])[["CANTIDAD"]].sum().reset_index()
                campaña = event_data["selection"]["multi"]#[0]["AÑO_CULTIVO"]
                if len(campaña) == 1:
                    st_df = st_df[st_df["AÑO_CULTIVO"]==campaña[0]["AÑO_CULTIVO"]] 
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
                st.altair_chart(data_layer, use_container_width=True,theme="streamlit")
                
            col_pie, col_lote= st.columns([4,8])   
            with col_pie:
                var_df = df.groupby(["VARIEDAD"])[["CANTIDAD"]].sum().reset_index()  
                campaña = event_data["selection"]["multi"]#[0]["AÑO_CULTIVO"]
                if len(campaña) == 1:
                    var_df = df.groupby(["VARIEDAD","AÑO_CULTIVO"])[["CANTIDAD"]].sum().reset_index() 
                    var_df = var_df[var_df["AÑO_CULTIVO"]==campaña[0]["AÑO_CULTIVO"]]   

                base =alt.Chart(var_df).mark_arc(innerRadius=50).encode(
                    theta="CANTIDAD:Q",
                    color="VARIEDAD:N",
                ).properties(
                    title=f'Variedades',
                    height=300
                )

                st.altair_chart(base, use_container_width=True,theme="streamlit")

            with col_lote:
                lote_df = df.groupby(["CONSUMIDOR"])[["CANTIDAD"]].sum().reset_index()
                campaña = event_data["selection"]["multi"]
                if len(campaña) == 1:
                    lote_df = df.groupby(["CONSUMIDOR","AÑO_CULTIVO"])[["CANTIDAD"]].sum().reset_index() 
                    lote_df = lote_df[lote_df["AÑO_CULTIVO"]==campaña[0]["AÑO_CULTIVO"]]
                bar_lotes = (
                alt.Chart(lote_df)
                .mark_bar()
                .encode(x="CONSUMIDOR", 
                        y="CANTIDAD",#alt.Y('Partidas').sort('-x'),
                        #color = alt.condition(multi_selection, "AÑO_CULTIVO:N", alt.value("lightgray"),),
                        text="CANTIDAD", 
                        tooltip=["CONSUMIDOR", "CANTIDAD"],
                        
                    )
                .properties(
                    title=f'Lotes',
                    height=300
                    )
                )
                st.altair_chart(bar_lotes, use_container_width=True,theme="streamlit")
    def costos_campania():
        styles(pt=1)
        if st.session_state['servicio_ip']:
            if st.session_state['empresa_name'] =="NISIRA":
                df = pd.read_parquet('./source/data/costos.parquet', engine='pyarrow')
            else:
                
                df_costos_campana = send_get_dataframe(ip = st.session_state['servicio_ip'],token=st.session_state['servicio_key'], endpoint="nsp_datos_detalle_costos_campana")
                consumidores_df=send_get_dataframe(ip = st.session_state['servicio_ip'],token=st.session_state['servicio_key'], endpoint="nsp_datos_consumidores")
                variedad_df=send_get_dataframe(ip = st.session_state['servicio_ip'],token=st.session_state['servicio_key'], endpoint="nsp_datos_variedades_cultivos")
                cultivos_df=send_get_dataframe(ip = st.session_state['servicio_ip'],token=st.session_state['servicio_key'], endpoint="nsp_datos_cultivos")
            #fertilizacion_df=send_get_dataframe(ip = st.session_state['servicio_ip'],token=st.session_state['servicio_key'], endpoint="nsp_datos_plan_fertilizacion")
            #df = cleanVariablesAgricolas(consumidores_df,variedad_df,cultivos_df,fertilizacion_df)
            
                df= costosAgricolas(df_costos_campana,consumidores_df,cultivos_df,variedad_df)
            
            #df = pd.read_parquet('./source/data/costos.parquet', engine='pyarrow')

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
            try :    
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
                    
            except:
                 
                lote_df = df.groupby(["CONSUMIDOR"])[[moneda,"AREA_CAMPAÑA"]].sum().sort_values(moneda,ascending=True).reset_index()
                fig = px.bar(lote_df, x="CONSUMIDOR", y= moneda, orientation='v', title= "Costos por Lote",height=400)
                event_lote = st.plotly_chart(fig, on_select="rerun",theme="streamlit")
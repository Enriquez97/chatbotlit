import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import plotly.express as px

import altair as alt
from utils.styles import styles
from utils.api import APIConnector,send_get_dataframe
from utils.data_transform import *
from utils.charts_plotly import *


class Finanzas:    
    def balance_general():
        styles(pt=1)
        if st.session_state['servicio_ip']:
            if st.session_state['empresa_name'] == "GRUPO RESEDISA S.A.C.":
                dataframe =  pd.read_parquet("source/data/RESEDISA/nsp_etl_situacion_financiera_resedisa.parquet")
            else:
                dataframe = send_get_dataframe(ip = st.session_state['servicio_ip'],token=st.session_state['servicio_key'], endpoint="nsp_etl_situacion_financiera")
            df_bg = transform_nsp_etl_situacion_financiera(df=dataframe)
            
            df_bg["Año"] = df_bg["Año"].astype("string")
            df_bg["Trimestre"] = df_bg["Trimestre"].astype("string")
            df_bg["Mes_"] = df_bg["Mes_"].astype("string")
            test_dff = df_bg.groupby(["titulo1","titulo2","titulo3"]).count().reset_index()
            st.title("Balance General")
            #st.dataframe(test_dff)
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
    def balance_ap():
        styles(pt=1)
        if st.session_state['servicio_ip']:
            if st.session_state['empresa_name'] == "GRUPO RESEDISA S.A.C.":
                dataframe =  pd.read_parquet("source/data/RESEDISA/nsp_etl_situacion_financiera_resedisa.parquet")
            else:
                dataframe = send_get_dataframe(ip = st.session_state['servicio_ip'],token=st.session_state['servicio_key'], endpoint="nsp_etl_situacion_financiera")
            df_bg = transform_nsp_etl_situacion_financiera(df=dataframe)
            df_bg["Año"] = df_bg["Año"].astype("string")
            df_bg["Trimestre"] = df_bg["Trimestre"].astype("string")
            df_bg["Mes_"] = df_bg["Mes_"].astype("string")
            colors_ = px.colors.qualitative.Bold+px.colors.qualitative.Set3
            #st.title("Activo & Pasivo")
            col_title,col_formato,col_year,col_tri,col_mes,col_moneda= st.columns([4,2,1,2,1,1])
            
            col_title.title("Activo & Pasivo")
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
            df = df_bg.copy()
            ap_dff = df[df['titulo1'].isin(['ACTIVO','PASIVO'])]
            
            ap_df = ap_dff.groupby(['titulo1'])[[moneda]].sum().reset_index()
            ap_df[moneda] = ap_df[moneda].abs()
            fig_pie = pie_(
                    df = ap_df, 
                    label_col = 'titulo1', 
                    value_col = moneda, 
                    title = 'ACTIVO & PASIVO',
                    height=330,
                    showlegend = True,
                    dict_color={'ACTIVO':'#7a9c9f','PASIVO':'#ccaa14'},
                    hole = .6,
                    textinfo = 'label+percent+value',
                    textposition = "outside"
            )
            line_df = ap_dff.groupby(['Año','Mes_num','Mes_','titulo1'])[[moneda]].sum().reset_index()
            line_df[moneda] = line_df[moneda].abs()
            line_pivot_dff = pd.pivot_table(line_df,index=['Año','Mes_num', 'Mes_'],values=moneda,columns='titulo1',aggfunc='sum').reset_index()
            line_pivot_dff['Year-Month'] = line_pivot_dff['Año'] +'-'+ line_pivot_dff['Mes_']
            
            fig_line = line_traces_(df = line_pivot_dff, height = 330 , trace = ['ACTIVO','PASIVO'],colors = ['#7a9c9f','#ccaa14'],ejex=['Year-Month'],hover_unified=True,title="Activo vs Pasivo")
            
            activo_df = df[df['titulo1']=='ACTIVO']
            activo3_df = activo_df.groupby(['Año','Mes_num','Mes_','titulo3'])[[moneda]].sum().reset_index()
            activo3_df['Year-Month'] = activo3_df['Año'] +'-'+ activo3_df['Mes_']
            fig_activo = px.bar(activo3_df, y=activo3_df[moneda], x=activo3_df['Year-Month'],color = 'titulo3',color_discrete_sequence =colors_,custom_data=['titulo3'] )
            fig_activo.update_layout(uniformtext_minsize=8, uniformtext_mode='hide',height = 300)
            fig_activo.update_layout(barmode='relative',legend_title_text = 'Activo')
            fig_activo.update_traces(cliponaxis=False)
            fig_activo.update_xaxes(tickfont=dict(size=11),showticklabels = True) 
            fig_activo.update_yaxes(tickfont=dict(size=11),showticklabels = True)
            fig_activo.update_layout(
                margin = dict( l = 20, r = 40, b = 50, t = 40),
                xaxis_title = '<b>'+'Mes'+'</b>',
                yaxis_title = '<b>'+''+'</b>',
                legend=dict(font=dict(size=11))
            )                                                                           #'%{customdata}%'
            fig_activo.update_traces(hovertemplate='<br><b>%{x}</b><br><b>%{customdata[0]}</b><br><b>%{y:,.2f}</b>',hoverlabel=dict(font_size=13))
            fig_activo.update_layout(title=dict(text="<b>Composición del Activo</b>", font=dict(size=22), automargin=True, yref='paper'))
            
            
            pasivo_df = df[df['titulo1']=='PASIVO']
            pasivo3_df = pasivo_df.groupby(['Año','Mes_num','Mes_','titulo3'])[[moneda]].sum().reset_index()
            pasivo3_df['Year-Month'] = pasivo3_df['Año'] +'-'+ pasivo3_df['Mes_']
            fig_pasivo = px.bar(pasivo3_df, y=pasivo3_df[moneda], x=pasivo3_df['Year-Month'],color = 'titulo3',color_discrete_sequence =colors_,custom_data=['titulo3'])
            fig_pasivo.update_layout(uniformtext_minsize=8, uniformtext_mode='hide',height = 300)
            fig_pasivo.update_layout(barmode='relative',legend_title_text = 'Pasivo')
            fig_pasivo.update_traces(cliponaxis=False)
            fig_pasivo.update_xaxes(tickfont=dict(size=11),showticklabels = True) 
            fig_pasivo.update_yaxes(tickfont=dict(size=11),showticklabels = True)
            fig_pasivo.update_layout(
                margin = dict( l = 20, r = 40, b = 50, t = 40,),
                xaxis_title = '<b>'+'Mes'+'</b>',
                yaxis_title = '<b>'+''+'</b>',
                legend=dict(font=dict(size=11))
            )
            fig_pasivo.update_traces(hovertemplate='<br><b>%{x}</b><br><b>%{customdata[0]}</b><br><b>%{y:,.2f}</b>', hoverlabel=dict(font_size=13))
            fig_pasivo.update_layout(title=dict(text="<b>Composición del Pasivo</b>", font=dict(size=22), automargin=True, yref='paper'))
            
            col_1_row = st.columns([4,8])
            col_1_row[0].plotly_chart(fig_pie)
            col_1_row[1].plotly_chart(fig_line)
            col_2_row = st.columns(1)
            col_2_row[0].plotly_chart(fig_activo)
            col_3_row = st.columns(1)
            col_3_row[0].plotly_chart(fig_pasivo)
    def analisis_activo():
        styles(pt=1)
        if st.session_state['servicio_ip']:
            if st.session_state['empresa_name'] == "GRUPO RESEDISA S.A.C.":
                dataframe =  pd.read_parquet("source/data/RESEDISA/nsp_etl_situacion_financiera_resedisa.parquet")
            else:
                dataframe = send_get_dataframe(ip = st.session_state['servicio_ip'],token=st.session_state['servicio_key'], endpoint="nsp_etl_situacion_financiera")
            df_bg = transform_nsp_etl_situacion_financiera(df=dataframe)
            df_bg["Año"] = df_bg["Año"].astype("string")
            years=sorted(df_bg['Año'].unique())
            df_bg["Trimestre"] = df_bg["Trimestre"].astype("string")
            df_bg["Mes_"] = df_bg["Mes_"].astype("string")
            #st.title("Activo & Pasivo")
            col_title,col_formato,col_year,col_tri,col_mes,col_moneda= st.columns([3,2,3,1,1,1])
            
            col_title.title("ACTIVO")
            with col_formato:
                selected_formato =st.selectbox("Formato",list(sorted(df_bg["formato"].unique())))
            df_bg = df_bg[df_bg['formato'] == selected_formato]
            with col_year:
                selected_year =st.multiselect("Año",list(sorted(df_bg["Año"].unique())), [years[-1]])
                if len(selected_year) > 0:
                    df_bg = df_bg[df_bg['Año'].isin(selected_year) ]
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
            colors_ = px.colors.qualitative.Bold+px.colors.qualitative.Set3
            ##########
            df = df_bg.copy()
            activo_dff = df[df['titulo1'].isin(['ACTIVO'])]
            ap_df = activo_dff.groupby(['titulo2'])[[moneda]].sum().reset_index()
            ap_df[moneda] = ap_df[moneda].abs()
            year_act_df = activo_dff.groupby(['Año','Mes_num','Mes_'])[[moneda]].sum().reset_index()
            year_df = pd.pivot_table(year_act_df,index=['Mes_num', 'Mes_'],values=moneda,columns='Año',aggfunc='sum').reset_index()
            act2_df = activo_dff.groupby(['Año','Mes_num','Mes_','titulo2'])[[moneda]].sum().reset_index()
            act2_pv_df = pd.pivot_table(act2_df,index=['Año','Mes_num', 'Mes_'],values=moneda,columns='titulo2',aggfunc='sum').reset_index()
            act2_pv_df['Year-Month'] = act2_pv_df['Año'] +'-'+ act2_pv_df['Mes_']
            
            act4_df = activo_dff.groupby(['titulo4'])[[moneda]].sum().sort_values(moneda).reset_index()
            fig_pie = pie_(
                    df = ap_df, 
                    label_col = 'titulo2', 
                    value_col = moneda, 
                    title = 'Activo',
                    height=330,
                    showlegend = True,
                    dict_color={'ACTIVO CORRIENTE':'#2B4CEA','ACTIVO NO CORRIENTE':'#974EE6','ACTIVOS NO CORRIENTES':'#974EE6'},
                    hole = .6,
                    textinfo = 'label+percent',
                    textposition='outside',
                    
            )
            fig_line_years = line_traces_(df = year_df, height = 330 , trace = sorted(year_act_df['Año'].unique()),colors = colors_,ejex=['Mes_'],title="Activo - Año Comparativo")
            fig_line_2 = line_traces_(df = act2_pv_df, height = 330 , trace = act2_df['titulo2'].unique(),colors = colors_,ejex=['Year-Month'],title="Activo - Corriente vs No Corriente")
            fig_bar = px.bar(act4_df, x='titulo4', y= moneda,height=330, title = "Cuentas")
            fig_bar.update_layout(autosize=True,margin=dict(t = 40),xaxis_title="",yaxis_title="")
            col_1_row = st.columns([4,8])
            col_1_row[0].plotly_chart(fig_pie)
            col_1_row[1].plotly_chart(fig_line_years)
            col_2_row = st.columns(2)
            col_2_row[0].plotly_chart(fig_line_2)
            col_2_row[1].plotly_chart(fig_bar)
            
    def analisis_pasivo():
        styles(pt=1)
        if st.session_state['servicio_ip']:
            if st.session_state['empresa_name'] == "GRUPO RESEDISA S.A.C.":
                dataframe =  pd.read_parquet("source/data/RESEDISA/nsp_etl_situacion_financiera_resedisa.parquet")
            else:
                dataframe = send_get_dataframe(ip = st.session_state['servicio_ip'],token=st.session_state['servicio_key'], endpoint="nsp_etl_situacion_financiera")
            df_bg = transform_nsp_etl_situacion_financiera(df=dataframe)
            df_bg["Año"] = df_bg["Año"].astype("string")
            years=sorted(df_bg['Año'].unique())
            df_bg["Trimestre"] = df_bg["Trimestre"].astype("string")
            df_bg["Mes_"] = df_bg["Mes_"].astype("string")
            #st.title("Activo & Pasivo")
            col_title,col_formato,col_year,col_tri,col_mes,col_moneda= st.columns([3,2,3,1,1,1])
            
            col_title.title("PASIVO")
            with col_formato:
                selected_formato =st.selectbox("Formato",list(sorted(df_bg["formato"].unique())))
            df_bg = df_bg[df_bg['formato'] == selected_formato]
            with col_year:
                selected_year =st.multiselect("Año",list(sorted(df_bg["Año"].unique())), [years[-1]])
                if len(selected_year) > 0:
                    df_bg = df_bg[df_bg['Año'].isin(selected_year) ]
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
            colors_ = px.colors.qualitative.Bold+px.colors.qualitative.Set3
            ##
            df = df_bg.copy()
            pasivo_dff = df[df['titulo1'].isin(['PASIVO'])]
            ap_df = pasivo_dff.groupby(['titulo2'])[[moneda]].sum().reset_index()
            ap_df[moneda] = ap_df[moneda].abs()
            
            year_act_df = pasivo_dff.groupby(['Año','Mes_num','Mes_'])[[moneda]].sum().reset_index()
            year_df = pd.pivot_table(year_act_df,index=['Mes_num', 'Mes_'],values=moneda,columns='Año',aggfunc='sum').reset_index()
            #ap_df[col_moneda] = ap_df[col_moneda].abs()
            
            pas2_df = pasivo_dff.groupby(['Año','Mes_num','Mes_','titulo2'])[[moneda]].sum().reset_index()
            pas2_pv_df = pd.pivot_table(pas2_df,index=['Año','Mes_num', 'Mes_'],values=moneda,columns='titulo2',aggfunc='sum').reset_index()
            pas2_pv_df['Year-Month'] = pas2_pv_df['Año'] +'-'+ pas2_pv_df['Mes_']
            
            
            pas4_df = pasivo_dff.groupby(['titulo4'])[[moneda]].sum().sort_values(moneda).reset_index()
            
            fig_pie = pie_(
                    df = ap_df, 
                    label_col = 'titulo2', 
                    value_col = moneda, 
                    title = 'Pasivo', 
                    height=330,
                    showlegend = True,
                    dict_color={'PASIVO CORRIENTE':'#2B4CEA','PASIVO NO CORRIENTE':'#974EE6','PASIVOS CORRIENTES':'#2B4CEA','PASIVOS NO CORRIENTES':'#974EE6'},
                    hole = .6,
                    textinfo = 'percent+value',
                    textposition='outside'
                )
            fig_line_years = line_traces_(df = year_df, height = 330 , trace = sorted(year_act_df['Año'].unique()),colors = colors_,ejex=['Mes_'],title="Pasivo - Año Comparativo")
            fig_line_2 = line_traces_(df = pas2_pv_df, height = 330 , trace = pas2_df['titulo2'].unique(),colors = colors_,ejex=['Year-Month'],title="Pasivo - Corriente vs No Corriente")
            fig_bar = px.bar(pas4_df, x='titulo4', y= moneda,height=330, title = "Cuentas")
            fig_bar.update_layout(autosize=True,margin=dict(t = 40),xaxis_title="",yaxis_title="")
            col_1_row = st.columns([4,8])
            col_1_row[0].plotly_chart(fig_pie)
            col_1_row[1].plotly_chart(fig_line_years)
            col_2_row = st.columns(2)
            col_2_row[0].plotly_chart(fig_line_2)
            col_2_row[1].plotly_chart(fig_bar)
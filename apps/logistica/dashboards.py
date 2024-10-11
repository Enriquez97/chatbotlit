import streamlit as st
import pandas as pd
import numpy as np
import datetime
from datetime import timedelta,datetime,date
from utils.styles import styles
from utils.api import send_get_dataframe,read_apis_sync
from utils.data_transform import *
from utils.charts_altair import ALTAIR
from utils.charts_plotly import *
from concurrent.futures import ThreadPoolExecutor
import plotly.express as px
class Logistica:
    
    def stocks():
        styles(pt=3)  
        if st.session_state['servicio_ip']:
            if st.session_state['servicio_parquet'] == True:
                dataframe =  pd.read_parquet(f"http://{st.session_state['servicio_ip']}:3005/read-parquet/nsp_stocks.parquet")
            else: 
                dataframe = send_get_dataframe(ip = st.session_state['servicio_ip'],token=st.session_state['servicio_key'], endpoint="nsp_stocks")
            #dataframe = APIConnector(st.session_state['servicio_ip'],st.session_state['servicio_key']).send_get_dataframe(endpoint="nsp_stocks")
            df = transform_nsp_stocks(dataframe)
            
            #print(df.columns)
            
            col_row_head = st.columns([4,2,2,2,1])
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
            #st.write(df.shape)
            #st.dataframe(df)
            gp_dff = df.groupby(["Grupo Producto"])[[valorizado]].sum().reset_index() 
            gp_dff[valorizado] = gp_dff[valorizado].astype(float)
            top_10_df= df.groupby(['Producto'])[[valorizado]].sum().sort_values([valorizado],ascending = True).tail(10).reset_index()   
            top_10_df[valorizado] = top_10_df[valorizado].astype(float)
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
            if st.session_state['servicio_parquet'] == True:
                dataframe =  pd.read_parquet(f"http://{st.session_state['servicio_ip']}:3005/read-parquet/STOCKALMVAL.parquet")
            else:
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
    
    def gestion_stock():
        styles(pt=1)  
        if st.session_state['servicio_ip']:
            consumoalm_params = {'C_EMP':'001','C_SUC':'','C_ALM': '','C_FECINI':str(datetime.now()- timedelta(days = 6 * 30))[:8].replace('-', "")+str('01')  ,'C_FECFIN':str(datetime.now())[:10].replace('-', ""),'C_VALOR':'1','C_GRUPO':'','C_SUBGRUPO':'','C_TEXTO':'','C_IDPRODUCTO':'','LOTEP':'','C_CONSUMIDOR':''}
            saldosalm_params = {'EMPRESA':'001','SUCURSAL':'','ALMACEN': '','FECHA':str(datetime.now())[:10].replace('-', ""),'IDGRUPO':'','SUBGRUPO':'','DESCRIPCION':'','IDPRODUCTO':'','LOTEP':''}
            
            @st.cache_data(ttl=600)
            def threadpool_data(ip: None, tk: None):
                with ThreadPoolExecutor(max_workers=2) as executor:
                    consumos_api_alm_df = executor.submit(send_get_dataframe,ip,tk,consumoalm_params,"NSP_OBJREPORTES_CONSUMOSALM_DET_BI").result()
                    saldos_api_alm_df = executor.submit(send_get_dataframe,ip,tk,saldosalm_params,"NSP_OBJREPORTES_SALDOSALMACEN_BI").result()
                return consumos_api_alm_df,saldos_api_alm_df
            if st.session_state['servicio_parquet'] == True:
                consumos_api_alm_df =  pd.read_parquet(f"http://{st.session_state['servicio_ip']}:3005/read-parquet/NSP_OBJREPORTES_CONSUMOSALM_DET_BI.parquet")
                saldos_api_alm_df =  pd.read_parquet(f"http://{st.session_state['servicio_ip']}:3005/read-parquet/NSP_OBJREPORTES_SALDOSALMACEN_BI.parquet")

            else:
                consumos_api_alm_df,saldos_api_alm_df = threadpool_data(st.session_state['servicio_ip'],st.session_state['servicio_key'])
            
            saldos_api_alm_df = change_cols_saldosalm(saldos_api_alm_df)
            #input_df = saldos_api_alm_df.groupby(['SUCURSAL','ALMACEN','DSC_GRUPO','DSC_SUBGRUPO','MARCA'])[['STOCK']].sum().reset_index()
            #print(consumos_api_alm_df,saldos_api_alm_df)
            col_row_head = st.columns([3,2,2,2,1,1,1])
            
            with col_row_head[0]:
                st.title("Gestion Stock")
            with col_row_head[1]:
                selected_grupo =st.selectbox("Grupo",list(sorted(saldos_api_alm_df["DSC_GRUPO"].unique())),index=None, placeholder="")#,list(sorted(df["Almacén"].unique())),index=None, placeholder=""
                if selected_grupo != None:
                    saldos_api_alm_df = saldos_api_alm_df[saldos_api_alm_df['DSC_GRUPO'] == selected_grupo]
                    consumos_api_alm_df = consumos_api_alm_df[consumos_api_alm_df['DSC_GRUPO'] == selected_grupo]
            with col_row_head[2]:
                selected_subgrupo =st.selectbox("Subgrupo",list(sorted(saldos_api_alm_df["DSC_SUBGRUPO"].unique())),index=None, placeholder="")
                if selected_subgrupo != None:
                    saldos_api_alm_df = saldos_api_alm_df[saldos_api_alm_df['DSC_SUBGRUPO'] == selected_subgrupo]
                    consumos_api_alm_df = consumos_api_alm_df[consumos_api_alm_df['DSC_SUBGRUPO'] == selected_subgrupo]
            with col_row_head[3]:
                selected_marca =st.selectbox("Marca",list(sorted(saldos_api_alm_df["MARCA"].unique())),index=None, placeholder="")
                if selected_marca != None:
                    saldos_api_alm_df = saldos_api_alm_df[saldos_api_alm_df['MARCA'] == selected_marca]
            with col_row_head[4]:
                input_cpm_min =st.number_input("Cpm Min",value=None)
            with col_row_head[5]:
                input_cpm_max =st.number_input("Cpm Max",value=None)
            with col_row_head[6]:
                selected_moneda = st.selectbox("Moneda", ("PEN","USD"))
                
            row_1 = st.columns([3,10])
            with row_1[0]:
                selected_sucursal =st.selectbox("Sucursal",list(sorted(saldos_api_alm_df["SUCURSAL"].unique())),index=None, placeholder="")
                if selected_sucursal != None:
                    saldos_api_alm_df = saldos_api_alm_df[saldos_api_alm_df['SUCURSAL'] == selected_sucursal]
                    consumos_api_alm_df = consumos_api_alm_df[consumos_api_alm_df['SUCURSAL'] == selected_sucursal]
                selected_almacen =st.selectbox("Almacen",list(sorted(saldos_api_alm_df["ALMACEN"].unique())),index=None, placeholder="")
                if selected_almacen != None:
                    saldos_api_alm_df = saldos_api_alm_df[saldos_api_alm_df['ALMACEN'] == selected_almacen]
                    consumos_api_alm_df = consumos_api_alm_df[consumos_api_alm_df['ALMACEN'] == selected_almacen]
                input_codigo = st.text_input("Código o Descripción")
                #btn = st.button("Reset", type="primary",use_container_width=True)
            col_pu = 'PU_S' if selected_moneda == 'PEN' else 'PU_D'    
            sig = 'S/.' if selected_moneda == 'PEN' else '$'
            inv_val_moneda = 'INV_VALMOF' if selected_moneda == 'PEN' else 'INV_VALMEX'
            
            input_df = saldos_api_alm_df.groupby(['SUCURSAL','ALMACEN','DSC_GRUPO','DSC_SUBGRUPO','MARCA'])[['STOCK']].sum().reset_index() 
            ##
            #PRECIO UNITARIO PROM
            precio_unit_prom = saldos_api_alm_df.groupby(['COD_PRODUCTO'])[[col_pu]].mean().reset_index()
            precio_unit_prom = precio_unit_prom.rename(columns = {col_pu:'Precio Unitario Promedio'})
            precio_unit_prom['Precio Unitario Promedio'] = precio_unit_prom['Precio Unitario Promedio'].fillna(0).round(2)

            #
            consumos_alm_df = consumos_api_alm_df.groupby(['IDPRODUCTO'])[['CANTIDAD']].sum().reset_index()
            saldos_alm_group_df = saldos_api_alm_df.groupby(['DSC_GRUPO', 'DSC_SUBGRUPO', 'COD_PRODUCTO', 'DESCRIPCION', 'UM','MARCA'])[['PU_S','PU_D', 'STOCK', 'INV_VALMOF', 'INV_VALMEX']].sum().reset_index()
            saldos_alm_group_df = saldos_alm_group_df[saldos_alm_group_df['STOCK']>0]
            
            dff = saldos_alm_group_df.merge(consumos_alm_df, how='left', left_on=["COD_PRODUCTO"], right_on=["IDPRODUCTO"])
            
            dff = dff.merge(precio_unit_prom,how='left', left_on=["COD_PRODUCTO"], right_on=["COD_PRODUCTO"])
            dff.loc[dff.MARCA =='','MARCA']='NO ESPECIFICADO'   
            
            dff['CANTIDAD'] = dff['CANTIDAD'].fillna(0)
            dff['STOCK'] = dff['STOCK'].fillna(0)
            dff['Precio Unitario'] = dff[col_pu].fillna(0)
            dff['CANTIDAD'] = dff['CANTIDAD']/6
            dff['CANTIDAD'] = dff['CANTIDAD'].round(5)
            dff['Meses Inventario'] = dff.apply(lambda x: meses_inventario(x['CANTIDAD'],x['STOCK']),axis=1)
            try:
                dff['TI'] = 1/dff['CANTIDAD'].astype(float)
            except:
                dff['TI'] = 0
            dff['TI'] = dff['TI'].replace([np.inf],0)
            
            if input_codigo != None:
                dff = dff[(dff['COD_PRODUCTO'].str.contains(input_codigo))|(dff['DESCRIPCION'].str.contains(input_codigo))]
            
            if input_cpm_min != None and input_cpm_max != None:
                dff = dff[(dff['CANTIDAD']>=input_cpm_min)&(dff['CANTIDAD']<=input_cpm_max)]
            
            try:
                cpm = round(dff['CANTIDAD'].astype(float).mean(),2)
            except:
                cpm = "-"
            invval = f"{sig}{(int(round(dff[inv_val_moneda].sum(),0))):,}"
            meses_invet_prom = dff[dff['Meses Inventario']!='NO ROTA']
            stock = round(meses_invet_prom['Meses Inventario'].mean(),2)
            consumo = round(dff['TI'].mean(),2)
            total_stock = f"{(int(round(dff['STOCK'].sum(),0))):,}"
            
            mi_dff = dff[(dff['Meses Inventario']!='NO ROTA')]
            mi_dff = mi_dff[mi_dff['Meses Inventario']>0]
            
            df_mi_ =mi_dff.groupby(['COD_PRODUCTO','DESCRIPCION'])[['Meses Inventario']].sum().sort_values('Meses Inventario').reset_index().tail(30)
            df_mi_ = df_mi_.rename(columns = {"DESCRIPCION":'Producto'})
            fig_1 = px.bar(df_mi_, x='Producto', y= 'Meses Inventario', title = "Meses de Inventario Promedio por Producto")
            fig_1.update_layout(autosize=True,margin=dict(t = 40,b=10),height=270)
            fig_1.update_xaxes(showticklabels = False)
            df_table = dff[['DSC_GRUPO', 'DSC_SUBGRUPO', 'COD_PRODUCTO', 'DESCRIPCION', 'UM','MARCA','Precio Unitario Promedio', 'STOCK', inv_val_moneda,'IDPRODUCTO', 'CANTIDAD', 'Meses Inventario','TI']]
            df_table = df_table.drop(['IDPRODUCTO'], axis=1)
            df_table = df_table.rename(columns = {"DSC_GRUPO":'Grupo',"DSC_SUBGRUPO":"Subgrupo","COD_PRODUCTO":"Código","DESCRIPCION":"Producto","UM":"UMD","MARCA":"Marca","STOCK":"Stock",inv_val_moneda:f'Inventario Valorizado {selected_moneda}','CANTIDAD': f'Consumo Promedio Mensual','Meses Inventario':'Meses de Inventario'})
            
            
            sucursal_df = saldos_api_alm_df.groupby(['SUCURSAL'])[[inv_val_moneda]].sum().sort_values(inv_val_moneda).reset_index()
            almacen_df = saldos_api_alm_df.groupby(['ALMACEN'])[[inv_val_moneda]].sum().sort_values(inv_val_moneda).reset_index()
            grupo_df = saldos_api_alm_df.groupby(['DSC_GRUPO'])[[inv_val_moneda]].sum().sort_values(inv_val_moneda).reset_index()
            
            
            
            with row_1[1]:
                row_in_row_1 = st.columns(5)
                row_in_row_1[0].metric("CPM", cpm, "",label_visibility="visible",help="Consumo Promedio Mensual")
                row_in_row_1[1].metric("INV VAL", invval, "",label_visibility="visible",help="Inventario Valorizado")
                row_in_row_1[2].metric("TOTAL STOCK", total_stock, "",label_visibility="visible")
                row_in_row_1[3].metric("TI STOCK", stock, "",label_visibility="visible")
                row_in_row_1[4].metric("TI CON", consumo, "",label_visibility="visible")
                st.plotly_chart(fig_1,theme="streamlit")
                
            with st.expander("Detalle"):
                st.dataframe(df_table,hide_index=True)
            
            row_2= st.columns(3)
            row_2[0].plotly_chart(bar_horizontal(df = sucursal_df, height = 350, x= inv_val_moneda, y = 'SUCURSAL', name_x='Inventario Valorizado', name_y='Sucursal',title = "Sucursal por Inventario Valorizado",color = 'rgb(95, 70, 144)'),theme="streamlit")
            row_2[1].plotly_chart(bar_horizontal(df = almacen_df, height = 350, x= inv_val_moneda, y = 'ALMACEN', name_x='Inventario Valorizado', name_y='Almacen',title = "Almacen por Inventario Valorizado",color ='rgb(29, 105, 150)'),theme="streamlit")
            row_2[2].plotly_chart(bar_horizontal(df = grupo_df, height = 350, x= inv_val_moneda, y = 'DSC_GRUPO', name_x='Inventario Valorizado', name_y='Grupo Producto',title = "Grupo Producto por Inventario Valorizado",color = 'rgb(56, 166, 165)'),theme="streamlit")
            #if btn:
            #    st.write("test")
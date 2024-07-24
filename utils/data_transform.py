import pandas as pd
import numpy as np
import base64 
from io import BytesIO
from PIL import Image

def decoding_avatar(img_code = None,width = 200, height = 50): 
    code = base64.b64decode(img_code)
    return Image.open(BytesIO(code)).resize((width, height))

def mes_short(x):
    dict_mes = {1:'Ene',2:'Feb',3:'Mar',4:'Abr',5:'May',6:'Jun',7:'Jul',8:'Ago',9:'Set',10:'Oct',11:'Nov',12:'Dic'}
    return dict_mes[x]

def cal_trim(mes):
    if mes == 1 or mes == 2 or mes == 3:
        return 1
    elif mes == 4 or mes == 5 or mes == 6:
        return 2
    elif mes == 7 or mes == 8 or mes == 9:
        return 3
    elif mes == 10 or mes == 11 or mes == 12:
        return 4    
    
def meses_inventario(cpm,stock):
    if cpm == 0:
        return None
    else:
        return round(stock/cpm,2)    
    
def new_col_salidas(x):
    if x == '':
        return 'Sin Salida'
    else:
        return 'Tuvo Salida'

def semana_text(year, week):
        if len(str(week)) == 1:
            semana = '0'+ str(week)
        else:
            semana = str(week)
        return str(year)+'-'+'Sem'+''+str(semana)
                                          
def trimestre_text(year,trimestre):
        return str(year)+' '+'Trim '+str(trimestre)  

def transform_nsp_etl_situacion_financiera(df = None):
    df['periodo'] = df['periodo'].fillna('')
    df = df[df['periodo'] != '']
    df['titulo1']=df['titulo1'].str.strip()
    df['titulo2']=df['titulo2'].str.strip()
    df['titulo3']=df['titulo3'].str.strip()
    df['titulo4']=df['titulo4'].str.strip()
    df['Año']=df['periodo'].str[:4]
    df['Mes']=df['periodo'].str[4:]
    df['Mes_num']= df['Mes'].astype('int')
    df['Mes_'] = df.apply(lambda x: mes_short(x['Mes_num']),axis=1) 
    df['Trimestre'] = df.apply(lambda x: cal_trim(x['Mes_num']),axis=1)
    return df

def transform_nsp_stocks(df = None):
    
    df['mes'] = df['mes'].astype('int')
    df['Mes'] = df.apply(lambda x: mes_short(x['mes']),axis=1)
    df['Mes_text']=df['mes']
    df['Mes_text']=df['Mes_text'].replace(1,'Enero')
    df['Mes_text']=df['Mes_text'].replace(2,'Febrero')
    df['Mes_text']=df['Mes_text'].replace(3,'Marzo')
    df['Mes_text']=df['Mes_text'].replace(4,'Abril')
    df['Mes_text']=df['Mes_text'].replace(5,'Mayo')
    df['Mes_text']=df['Mes_text'].replace(6,'Junio')
    df['Mes_text']=df['Mes_text'].replace(7,'Julio')
    df['Mes_text']=df['Mes_text'].replace(8,'Agosto')
    df['Mes_text']=df['Mes_text'].replace(9,'Setiembre')
    df['Mes_text']=df['Mes_text'].replace(10,'Octubre')
    df['Mes_text']=df['Mes_text'].replace(11,'Noviembre')
    df['Mes_text']=df['Mes_text'].replace(12,'Diciembre')
    df = df.rename(columns = {
                     'dsc_producto':'Producto',
                     'dsc_grupo': 'Grupo Producto',
                     'dsc_subgrupo': 'Sub Grupo Producto',
                     'unid_medida': 'Unidad de medida',
                     'stock_unidades':'Stock en unidades',
                     'costo_unitario_mof':'Costo Unitario Soles',
                     'costo_unitario_mex':'Costo Unitario Dolares',
                     'stock_valorizado_mof':'Stock Valorizado Soles',
                     'stock_valorizado_mex':'Stock Valorizado Dolares',
                     'año':'Año',
                     'mes':'Mes_',
                     'venta_prom_unidades':'Venta prom 12 meses en UN',
                     'venta_prom_mof':'Venta prom 12 meses en monto Soles',
                     'venta_prom_mex':'Venta prom 12 meses en monto Dolares',
                     'costo_venta_prom_mof':'Costo de Venta prom 12 meses en monto Soles',
                     'costo_venta_prom_mex':'Costo de Venta prom 12 meses en monto Dolares',
                     'ABC_ventas':'ABC Ventas',
                     'ABC_stock':'ABC Stock',
                     'rango_antiguedad_stock':'Rango antigüedad del stock',
                     'rotacion':'Rotación',
                     'meses_stock': 'Meses de stock',
                     
          }
    )
    return df

def transform_stockalmval(df = None):
    df['ALMACEN'] = df['ALMACEN'].apply(lambda x: x.strip())
    df['tipo'] = df['tipo'].fillna('No Especificado')
    df['tipo'] = df['tipo'].apply(lambda x: x.strip())
    df['SUCURSAL'] = df['SUCURSAL'].apply(lambda x: x.strip())
    df['GRUPO'] = df['GRUPO'].apply(lambda x: x.strip())
    df['SUBGRUPO'] = df['SUBGRUPO'].apply(lambda x: x.strip())
    df['PRODUCTO'] = df['PRODUCTO'].apply(lambda x: x.strip())
    df['GRUPO2'] = df['GRUPO2'].fillna('')
    df['GRUPO2'] = df['GRUPO2'].apply(lambda x: x.strip())
    df['RESPONSABLEINGRESO'] = df['RESPONSABLEINGRESO'].fillna('No Especificado')
    df['RESPONSABLEINGRESO'] = df['RESPONSABLEINGRESO'].apply(lambda x: x.strip())
    df['RESPONSABLESALIDA'] = df['RESPONSABLESALIDA'].fillna('No Especificado')
    df['RESPONSABLESALIDA'] = df['RESPONSABLESALIDA'].apply(lambda x: x.strip())
    df['ULTFECHAINGRESO'] = pd.to_datetime(df['ULTFECHAINGRESO'].str[:-14], format="%Y-%m-%d")
    df['ULTFECHASALIDA'] = pd.to_datetime(df['ULTFECHASALIDA'].str[:-14], format="%Y-%m-%d")
    df['Duracion_Inventario'] = df['ULTFECHASALIDA']-df['ULTFECHAINGRESO']
    df['Duracion_Inventario'] = (df['Duracion_Inventario'].dt.days)
    df= df[df["ULTFECHAINGRESO"].notna()]
    df['Estado Inventario'] = df['ULTFECHASALIDA'].astype('string')
    df['Estado Inventario'] = df['Estado Inventario'].replace([np.nan],[''])
    df['Estado Inventario'] = df.apply(lambda x: new_col_salidas(x['Estado Inventario']),axis=1)
    df = df.drop(['codmodelo','modelo'], axis=1)
    dff = df.rename(columns = {
        'CODSUCURSAL': 'Código Sucursal', 
        'SUCURSAL'   : 'Sucursal',
        'CODALMACEN' : 'Código Almacén',
        'ALMACEN'    : 'Almacén',
        'codtipo'    : 'Código Tipo',
        'tipo'       : 'Tipo',
        'CODGRUPO'   : 'Código Grupo',
        'GRUPO'      : 'Grupo',
        'CODSUBGRUPO': 'Código Sub Grupo',
        'SUBGRUPO'   : 'Sub Grupo',
        'CODPRODUCTO': 'Código Producto',
        'PRODUCTO'   : 'Producto',
        'GRUPO2'     : 'Grupo 2',
        'RESPONSABLEINGRESO' : 'Responsable Ingreso',
        'RESPONSABLESALIDA'  : 'Responsable Salida',
        'MEDIDA'     : 'Unidad de Medida',
        'ESTADO'     : 'Estado',
        'STOCK'      : 'Stock',
        'IMPORTETOTALMOF' : 'Importe Soles',
        'IMPORTETOTALMEX' : 'Importe Dolares',
        'UBICACION'  : 'Ubicación',
        'ULTFECHAINGRESO' : 'Última Fecha Ingreso',
        'ULTFECHASALIDA'  : 'Última Fecha Salida',
        'MARCA'      : 'Marca',
        'TIPOMATERIAL': 'Tipo de Material',
        'desde'      : 'Desde',
        'hasta'      : 'Hasta'
    })
    return dff

def change_cols_saldosalm(df = None):
    df = df.rename(columns={
        'sucursal':'SUCURSAL',
        'almacen':'ALMACEN',
        'codproducto':'COD_PRODUCTO',
        'stock':'STOCK'   
    })
    df['DESCRIPCION'] = df['DESCRIPCION'].str.strip()
    df['SUCURSAL'] = df['SUCURSAL'].str.strip()
    df['ALMACEN'] = df['ALMACEN'].str.strip()
    df['DSC_GRUPO'] = df['DSC_GRUPO'].str.strip()
    df['DSC_SUBGRUPO'] = df['DSC_SUBGRUPO'].str.strip()
    df['MARCA'] = df['MARCA'].str.strip()
    df['MARCA'] = df['MARCA'].replace([''],['NO ESPECIFICADO'])
    return df

columns_drop_nsp_rpt_ventas_detallado = [
        'DOCUMENTO','IDCLIEPROV','MONEDA','TCAMBIO','PROYECTO','TCMONEDA','IDPRODUCTO','IDMEDIDA','VENTANA','IDCOBRARPAGARDOC', 
        'IDSERIE', 'UNDEX', 'EQUIVALENCIA','idtipocontenedor', 'idtipoprecio', 'DSC_PUERTODESTINO', 'DUA', 'glosa','IDCANAL',
        'CANAL', 'Lotep', 'ocompra','nro_contenedor','idconsumidor', 'IDCAMPANA', 'CONTADO', 'vencimiento'
    ]
columns_nsp_rpt_ventas_detallado = {
                                'SUCURSAL': 'Sucursal',
                                'FECHA': 'Fecha',
                                'RAZON_SOCIAL': 'Cliente',
                                'VENDEDOR':'Vendedor',
                                'TIPOMOVIMIENTO':'Tipo de Movimiento',
                                'TIPOVENTA': 'Tipo de Venta',
                                'CONDICION': 'Tipo de Condicion',
                                'DESCRIPCION': 'Producto',
                                'GRUPO': 'Grupo Producto',
                                'SUBGRUPO': 'Subgrupo Producto',
                                'MARCA': 'Marca Producto',
                                'CANTIDAD': 'Cantidad',
                                'PRECIOMOF':'P.U Soles',
                                'PRECIOMEX':'P.U Dolares',
                                'VVENTAMOF': 'Subtotal Soles',
                                'VVENTAMEX': 'Subtotal Dolares',
                                'IMPORTEMOF': 'Importe Soles',
                                'IMPORTEMEX': 'Importe Dolares',
                                'NroEmbarque': 'Número de Embarque',
                                'FechaEmbarque': 'Fecha de Embarque',
                                'PESONETO_PRODUCTO': 'Peso Producto', 
                                'DEPARTAMENTO': 'Departamento',
                                'PROVINCIA': 'Provincia', 
                                'DISTRITO': 'Distrito', 
                                'PAIS': 'Pais',
                                'CULTIVO': 'Cultivo', 
                                'VARIEDAD': 'Variedad', 
                                'FORMATO': 'Formato', 
                                'GRUPOCLIENTE': 'Grupo Cliente'
                                }
def transform_nsp_rpt_ventas_detallado(dataframe = pd.DataFrame()):
    dataframe = dataframe.drop(columns_drop_nsp_rpt_ventas_detallado, axis=1)
    dataframe = dataframe.rename(columns = columns_nsp_rpt_ventas_detallado)
    dataframe['Sucursal'] = dataframe['Sucursal'].str[4:]
    dataframe['Vendedor'] = dataframe['Vendedor'].str[4:]
    dataframe['Tipo de Movimiento'] = dataframe['Tipo de Movimiento'].str[5:]
    dataframe['Tipo de Venta'] = dataframe['Tipo de Venta'].str[4:]
    dataframe['Tipo de Condicion'] = dataframe['Tipo de Condicion'].str[4:]
    dataframe['Grupo Producto'] = dataframe['Grupo Producto'].str[5:]
    dataframe['Subgrupo Producto'] = dataframe['Subgrupo Producto'].str[4:]
    dataframe['Grupo Cliente'] = dataframe['Grupo Cliente'].str[3:]
    dataframe['Fecha'] = pd.to_datetime(dataframe['Fecha'].str[:-14], format="%Y-%m-%d")
    dataframe['Departamento'] = dataframe['Departamento'].fillna('NO ESPECIFICADO')
    dataframe['Sucursal'] = dataframe['Sucursal'].fillna('NO ESPECIFICADO')
    dataframe['Vendedor'] = dataframe['Vendedor'].fillna('NO ESPECIFICADO')
    dataframe['Tipo de Movimiento'] = dataframe['Tipo de Movimiento'].fillna('NO ESPECIFICADO')
    dataframe['Tipo de Venta'] = dataframe['Tipo de Venta'].fillna('NO ESPECIFICADO')
    dataframe['Tipo de Condicion'] = dataframe['Tipo de Condicion'].fillna('NO ESPECIFICADO')
    dataframe['Grupo Producto'] = dataframe['Grupo Producto'].fillna('NO ESPECIFICADO')
    dataframe['Subgrupo Producto'] = dataframe['Subgrupo Producto'].fillna('NO ESPECIFICADO')
    dataframe['Producto'] = dataframe['Producto'].apply(lambda x: x.strip())
    dataframe['Cliente'] = dataframe['Cliente'].apply(lambda x: x.strip())
    dataframe['Grupo Producto'] = dataframe['Grupo Producto'].apply(lambda x: x.strip())
    dataframe['Pais'] = dataframe['Pais'].str.rstrip()
    dataframe['Dia'] = dataframe['Fecha'].dt.day
    dataframe['Mes Num'] = dataframe['Fecha'].dt.month
    dataframe['Mes']=dataframe['Mes Num']
    dataframe['Mes']=dataframe['Mes'].replace(1,'Enero')
    dataframe['Mes']=dataframe['Mes'].replace(2,'Febrero')
    dataframe['Mes']=dataframe['Mes'].replace(3,'Marzo')
    dataframe['Mes']=dataframe['Mes'].replace(4,'Abril')
    dataframe['Mes']=dataframe['Mes'].replace(5,'Mayo')
    dataframe['Mes']=dataframe['Mes'].replace(6,'Junio')
    dataframe['Mes']=dataframe['Mes'].replace(7,'Julio')
    dataframe['Mes']=dataframe['Mes'].replace(8,'Agosto')
    dataframe['Mes']=dataframe['Mes'].replace(9,'Setiembre')
    dataframe['Mes']=dataframe['Mes'].replace(10,'Octubre')
    dataframe['Mes']=dataframe['Mes'].replace(11,'Noviembre')
    dataframe['Mes']=dataframe['Mes'].replace(12,'Diciembre')
    dataframe['Año'] =dataframe['Fecha'].dt.year
    dataframe['Año'] =dataframe['Fecha'].dt.year
    dataframe['Semana_'] = dataframe['Fecha'].dt.isocalendar().week.astype(int)
    dataframe['Semana'] = dataframe.apply(lambda x: semana_text(x['Año'], x['Semana_']),axis=1)
    dataframe['Trimestre_'] =dataframe['Fecha'].dt.quarter
    dataframe['Trimestre'] = dataframe.apply(lambda x: trimestre_text(x['Año'], x['Trimestre_']),axis=1)
    dataframe['Pais'] = dataframe['Pais'].replace([np.nan],['NO ESPECIFICADO'])
    dataframe['Cultivo'] = dataframe['Cultivo'].replace([''],['NO ESPECIFICADO'])
    dataframe['Variedad'] = dataframe['Variedad'].replace([''],['NO ESPECIFICADO'])
    dataframe['Departamento'] = dataframe['Departamento'].replace([''],['NO ESPECIFICADO'])
    return dataframe


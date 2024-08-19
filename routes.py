import streamlit as st
from apps.logout import logout
from apps.home import*
from apps.comercial.dashboards import Comercial
from apps.logistica.dashboards import Logistica
from apps.finanzas.dashboards import Finanzas
from apps.produccion.ejecucion_cam import Produccion

inicio = [st.Page(home,title="Home",icon = ":material/home:",)]
produccion = [
    st.Page(Produccion.ejecucion_campania,title="Ejecución Campaña",icon = ":material/psychiatry:",),
    st.Page(Produccion.costos_campania,title="Costos Campaña",icon = ":material/psychiatry:",)
]
finanzas = [
    st.Page(Finanzas.balance_general,title="Balance General",icon = ":material/send_money:"),
    st.Page(Finanzas.balance_ap,title="Activo & Pasivo",icon = ":material/send_money:"),
    st.Page(Finanzas.analisis_activo,title="Análisis del Activo",icon = ":material/send_money:"),
    st.Page(Finanzas.analisis_pasivo,title="Análisis del Pasivo",icon = ":material/send_money:")
]
comercial = [
    st.Page(Comercial.informe_ventas,title="Informe de Ventas",icon = ":material/storefront:",),
    st.Page(Comercial.comparativo_ventas,title="Comparativo de Ventas",icon = ":material/storefront:",)
]

logistica = [
    st.Page(Logistica.stocks,title="Stocks",icon = ":material/inventory:",),
    st.Page(Logistica.estado_inventario,title="Estado de Inventario",icon = ":material/inventory:"),
    st.Page(Logistica.gestion_stock,title="Gestión de Stock",icon = ":material/inventory:",)
]

def pages_rol(role : None, rubro: None):
    page_dict = {}
    if role == "Administrador":
        if rubro == "Agrícola" or rubro == "Agroindustrial":
            page_dict["Home"] = inicio
            page_dict["Finanzas"] = finanzas
            page_dict["Producción"] = produccion
            page_dict["Comercial"] = comercial
            page_dict["Logistica"] = logistica
        elif rubro == "Comercial":
            page_dict["Home"] = inicio
            page_dict["Finanzas"] = finanzas
            page_dict["Comercial"] = comercial
            page_dict["Logistica"] = logistica
        else:
            page_dict["Home"] = inicio
    else:
        page_dict["Home"] = inicio
    return page_dict
#page_dict = {}

account_pages = [
    st.Page(logout, title="Log out", icon=":material/logout:"),
    #st.Page("./apps/settings.py", title="Settings", icon=":material/settings:")
]


#page_dict["LLM"] = [
#    st.Page("./apps/llm/chat_bot.py",title="Chat Bot",icon = ":material/smart_toy:",)
#]
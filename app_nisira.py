import streamlit as st

LOGO_NISIRA = "https://www.nisira.com.pe/images/Logo/logo2.png"
st.set_page_config(
    page_title="Nisira",
    page_icon=LOGO_NISIRA,
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'About': "Nisira System"
    }
)
if "role" not in st.session_state:
    st.session_state.role = None

ROLES = [None, "Requester", "Responder", "Admin","Test"]


def login():

    st.header("Log in")
    role = st.selectbox("Choose your role", ROLES)

    if st.button("Log in"):
        st.session_state.role = role
        st.rerun()


def logout():
    st.session_state.role = None
    st.rerun()


role = st.session_state.role

logout_page = st.Page(logout, title="Log out", icon=":material/logout:")
settings = st.Page("settings.py", title="Settings", icon=":material/settings:")
request_1 = st.Page(
    "request/request_1.py",
    title="Request 1",
    icon=":material/help:",
    default=(role == "Requester"),
)
request_2 = st.Page(
    "request/request_2.py", title="Request 2", icon=":material/bug_report:"
)
respond_1 = st.Page(
    "respond/respond_1.py",
    title="Respond 1",
    icon=":material/healing:",
    default=(role == "Responder"),
)
respond_2 = st.Page(
    "respond/respond_2.py", title="Respond 2", icon=":material/handyman:"
)
admin_1 = st.Page(
    "admin/admin_1.py",
    title="Admin 1",
    icon=":material/person_add:",
    default=(role == "Admin"),
)
admin_2 = st.Page("admin/admin_2.py", title="Admin 2", icon=":material/security:")

balance_general = st.Page("finanzas/balance_general.py",title="Balance General",icon = ":material/send_money:",default=(role == "Test"))
#resumen_ventas = st.Page("comercial/resumen_ventas.py",title="Resumen de Ventas",icon = ":material/store:",)

##
chat_bot_openai = st.Page("llm/chat_bot.py",title="Chat Bot",icon = ":material/smart_toy:",)
##
recursos_agricolas = st.Page("produccion/ejecucion_cam.py",title="Ejecución Campaña",icon = ":material/psychiatry:",)

account_pages = [logout_page, settings]
request_pages = [request_1, request_2]
respond_pages = [respond_1, respond_2]
admin_pages = [admin_1, admin_2]
finanzas_pages = [balance_general]
llm_pages = [chat_bot_openai]
produccion = [recursos_agricolas]

#st.title("Request manager")
st.logo("images/nisira_logo.png", icon_image="images/logo_grande.jpg")

page_dict = {}
if st.session_state.role in ["Requester", "Admin"]:
    page_dict["Request"] = request_pages
if st.session_state.role in ["Responder", "Admin"]:
    page_dict["Respond"] = respond_pages
if st.session_state.role == "Admin":
    page_dict["Admin"] = admin_pages
if st.session_state.role == "Test":
    page_dict["LLM"] = llm_pages
    page_dict["Finanzas"] = finanzas_pages
    page_dict["Producción"] = produccion

if len(page_dict) > 0:
    pg = st.navigation( page_dict | {"Account": account_pages})
else:
    pg = st.navigation([st.Page(login)])

pg.run()
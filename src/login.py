import streamlit as st
import base64
from pathlib import Path

st.set_page_config(
    page_title="Rota Segura",
    page_icon="🗺️", 
)

st.markdown(
    """
    <style>
        [data-testid="stSidebar"] {
            display: none;
        }
        div[data-testid="stTextInput"] > div > div > input {
            background-color: #FFFFFF;
            color: #009CCC;
            border: 2px solid #009CCC;
            border-radius: 10px;
            height: 48px;
            padding-left: 15px;
            font-weight: 500;
        }
        [data-testid="stVerticalBlockBorderWrapper"] {
            background: white;
            padding: 60px;
            border-radius: 15px;
        }
        [data-testid="stAlertContainer"] {
            background: #EEEEEE;
            
        }
        div[data-testid="stTextInput"] > div > div > input::placeholder {
            color: #009CCC !important;
            opacity: 0.8 !important;
        }
        [data-testid="stButton"] button {
            background: linear-gradient(to bottom, #009CCC, #001BBC);
            color: white;
            border-radius: 10px;
            width: 100%;
            height: 45px;
            border: none;
        }
        .stApp {
            background-color: #0072B5;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
        }
        .login-container {
            background-color: #FFFFFF;
            padding: 2rem 3rem;
            border-radius: 20px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
            color: #333333;
            width: 400px;
            max-width: 90%;
        }
        .login-title {
            text-align: center;
            color: #333333;
        }
        .login-header {
            text-align: center;
            color: #555555;
            margin-bottom: 2rem;
        }
    </style>
    """,
    unsafe_allow_html=True
)

USUARIO_CORRETO = "user"
SENHA_CORRETA = "1234"

def checar_credenciais(usuario, senha):
    return usuario == USUARIO_CORRETO and senha == SENHA_CORRETA

if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
    st.session_state['username'] = ''

if not st.session_state['logged_in']:
    logo_path = Path(__file__).parent / "components" / "rota_logo.png"
    with open(logo_path, "rb") as image_file:
        encoded = base64.b64encode(image_file.read()).decode()
    st.markdown(
        f'<div style="text-align: center; margin-bottom: 2rem;"><img src="data:image/png;base64,{encoded}" width="300px"></div>',
        unsafe_allow_html=True
    )

    with st.container():
        username_input = st.text_input("Usuário", key="login_username", label_visibility="collapsed", placeholder="Usuário")
        password_input = st.text_input("Senha", type="password", key="login_password", label_visibility="collapsed", placeholder="Senha")
        st.markdown("<br>", unsafe_allow_html=True)

        if st.button("Login", type="primary", use_container_width=True):
            if checar_credenciais(username_input, password_input):
                st.session_state['logged_in'] = True
                st.session_state['username'] = username_input
                st.switch_page("pages/app.py")
            else:
                st.error("Usuário ou senha inválida.")

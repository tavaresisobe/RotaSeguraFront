import streamlit as st
import folium
from streamlit_folium import st_folium, components
import requests

st.set_page_config(
    page_title="Rota Segura",
    page_icon="🗺️",
    layout="wide"
)

BACKEND_URL = "https://rotaseguraback-production.up.railway.app"

def apply_custom_css():
    st.markdown("""
    <style>
        [data-testid="stSidebar"] [data-testid="stButton"] {
            display: flex;
            justify-content: center;
        }
        [data-testid="stSidebarNav"] {
            display: none;
        }
        [data-testid="stMainBlockContainer"] {
            padding: 0;
        }
        [data-testid="stSidebarHeader"] {
            display: none;
        }
        [data-testid="stSidebarUserContent"] {
            margin: 0px;
            padding: 0px;
        }
        [data-testid="stSidebarContent"] {
            margin: 0px;
            padding: 0px;
            max-height: 100vh;
            overflow-y: auto;
            overflow-x: hidden;
            scrollbar-width: thin;
            scrollbar-color: #009CCC transparent;
        }
        [data-testid="stSidebar"] {
            background-color: #F0F2F6;
            min-width: 600px !important;
            width: 600 !important;
            max-width: 100vw !important;
            padding: 0px;
            margin: 0px;
            border: none;
            max-height: 100vh;
            overflow-y: auto;
            overflow-x: hidden;
            scrollbar-width: thin;
            scrollbar-color: #009CCC transparent;
        }
        div[data-testid="stAppViewBlockContainer"] {
            background-color: white;
            border: none;
        }
        div[data-testid="stTextInput"] {
            display: flex;
            justify-content: center;
        }
        div[data-testid="stTextInput"] > label {
            display: none;
        }
        div[data-testid="stTextInputRootElement"] {
            width: 80%;
            background-color: #FFFFFF;
            color: #009CCC;
            border: 2px solid #009CCC;
            border-radius: 8px;
        }
        div[data-testid="stTextInput"] > div > div > input,
        div[data-testid="stNumberInput"] input {
            background-color: #FFFFFF;
            color: #009CCC;
            border: 2px solid #009CCC;
            border-radius: 8px;
            height: 48px;
            padding-left: 15px;
            font-weight: 500;
            width: 100%;
            caret-color: #009CCC;
        }
        div[data-testid="stTextInput"] > div > div > input::placeholder {
            color: #009CCC !important;
            opacity: 0.8 !important;
        }
        [data-testid="stButton"] button {
            background: linear-gradient(to bottom, #009CCC, #001BBC);
            color: white;
            border-radius: 10px;
            width: 80%;
            height: 45px;
            border: none;
        }
        [data-testid="stButton"] button:hover {
            opacity: 0.8;
            color: white;
        }
        div[data-testid="stNumberInput"] {
            display: flex;
            justify-content: center;
            width: 80%;
        }
        div[data-testid="stNumberInput"] > div {
            width: 25%;
        }
        .rua-item {
            background-color: #ECF7FF;
            border-bottom: 1px solid #e0e0e0;
            padding: 20px;
            margin-bottom: 5px;
            width: 100%;
        }
        .rua-item:last-child {
            border-bottom: none;
        }
        .input-row {
            display: flex;
            align-items: center;
            width: 75%;
            margin-top: 15px;
        }
        .input-icon {
            font-size: 24px;
            padding-right: 10px;
            padding-top: 5px;
        }
        div[data-testid="stAlertContentSuccess"] > div {
            color: black;
        }
        div[data-testid="stAlertContentError"] > div {
            color: black;
        }
        div[data-testid="stAlertContentWarning"] > div {
            color: black;
        }
        .input-widget {
            background-color: #FFFFFF;
            color: #009CCC;
            border: 2px solid #009CCC;
            border-radius: 8px;
            height: 48px;
            padding-left: 15px;
            font-weight: 500;
            width: 100%;
            margin-bottom: 10px;
            margin-top: 5px;
        }
        div[data-testid="stNumberInput"] > label {
            color: black; 
            font-size: 20px;
            font-weight: 600; 
            margin-right: 5px;
        }
        .swap-icon-container {
            text-align: right;
            margin-top: -68px;
            margin-right: 15px;
            margin-bottom: 20px;
        }
        .swap-icon {
            font-size: 20px;
            cursor: pointer;
        }
        .search-container {
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            background-color: white;
            width: 100%;
            margin-bottom: 20px;
            padding: 20px;
        }
        .button-style {
            background: linear-gradient(to bottom, #009CCC, #001BBC);
            color: white;
            border-radius: 10px;
            width: 100%;
            height: 45px;
            border: none;
            font-weight: bold;
            font-size: 16px;
        }
        .ruas-container {
            display: flex;
            flex-direction: column;
            justify-content: center;
            background-color: white;
            width: 100%;
        }
        .column-input {
            flex: 1;
            align-items: center;
        }
        .column-swap {
            align-items: flex-start;
            justify-content: center;
            padding-top: 15px;
        }
        .column-icon {
            align-items: flex-end;
        }
        .row {
            display: flex;
            justify-content: center;
            align-items: center;
            gap: 20px;
            width: 100%;
        }
    </style>
    """, unsafe_allow_html=True)

def main():
    apply_custom_css()

    if "route_map_html" not in st.session_state:
        st.session_state.route_map_html = None
    if "route_street_info" not in st.session_state:
        st.session_state.route_street_info = []

    with st.sidebar:
        st.markdown("<h2 style='color: black; text-align: center;'>DEFINA O TRAJETO</h2>", unsafe_allow_html=True)

        origin_input = st.text_input("partida", placeholder="Local de partida (Ex: Av. Cassiano Ricardo, São José dos Campos)", label_visibility="collapsed")
        destination_input = st.text_input("chegada", placeholder="Local de chegada (Ex: Av. José Longo, São José dos Campos)", label_visibility="collapsed")
        max_occurrences_input = st.number_input("Número máximo de ocorrências por rua:", min_value=0, value=30, step=1)

        if st.button("Calcular rota", use_container_width=True):
            if origin_input and destination_input:
                try:
                    response = requests.post(
                        f"{BACKEND_URL}/calculate-route",
                        json={
                            "origin_street": origin_input,
                            "destination_street": destination_input,
                            "max_crime_occurrences": max_occurrences_input
                        }
                    )
                    result = response.json()
                except Exception as e:
                    st.error(f"Erro ao se conectar com o backend: {e}")
                    return

                if "error" in result:
                    st.error(result["error"])
                    st.session_state.route_map_html = None
                    st.session_state.route_street_info = []
                elif not result.get("route_found"):
                    st.warning(result.get("message", "Não foi possível encontrar uma rota com os critérios definidos."))
                    st.session_state.route_map_html = None
                    st.session_state.route_street_info = []
                else:
                    st.success("Rota segura encontrada! ✅")
                    st.session_state.route_map_html = result.get("route_map_html")
                    st.session_state.route_street_info = result.get("route_street_info", [])
            else:
                st.warning("Por favor, preencha os locais de partida e chegada.")

        if st.session_state.route_street_info:
            st.markdown("<h3 style='color: black; padding-top: 20px;'>TRAJETO</h3>", unsafe_allow_html=True)
            html_ruas = '<div class="ruas-container">'
            for rua in st.session_state.route_street_info:
                html_ruas += f"""<div class="rua-item">
                    <b style="color: black;">{rua['nome']}</b>
                    <p style="margin:0; color: #333;">{rua['ocorrencias']} ocorrências no último mês</p>
                    <p style="margin:0; color: #333;">Pior período: {rua['periodo']}</p>
                </div>"""
            html_ruas += '</div>'
            st.markdown(html_ruas, unsafe_allow_html=True)

    if st.session_state.route_map_html:
        components.html(st.session_state.route_map_html, height=1200, scrolling=True)
    else:
        st.info("Preencha os campos na barra lateral e clique em 'Calcular rota segura' para começar.")
        map_center = [-23.1791, -45.8872]
        m = folium.Map(location=map_center, zoom_start=13)
        st_folium(m, width='100%', height=1200, returned_objects=[])

if __name__ == "__main__":
    main()

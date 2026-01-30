import streamlit as st
import requests
import json
from datetime import datetime, timezone, timedelta

st.set_page_config(page_title="Teste API Tangerino - Punch", layout="wide")
st.title("⏰ Teste API Tangerino - Punch Controller (Legacy API)")

# 🔥 NOVA BASE (API que funcionou)
BASE_URL = "https://apis.tangerino.com.br/punch"

HEADERS = {
    "accept": "application/json;charset=UTF-8",
    "Authorization": st.secrets["TANGERINO_AUTH"]
}

# 🔧 Converte data para timestamp ms (formato aceito por essa API)
def to_millis(date_obj, end_of_day=False):
    if end_of_day:
        dt = datetime(date_obj.year, date_obj.month, date_obj.day, 23, 59, 59, tzinfo=timezone.utc)
    else:
        dt = datetime(date_obj.year, date_obj.month, date_obj.day, 0, 0, 0, tzinfo=timezone.utc)
    return int(dt.timestamp() * 1000)

def make_request(method, endpoint="", params=None, body=None):
    url = f"{BASE_URL}{endpoint}"
    st.info(f"Enviando {method} para: {url}")

    if params:
        st.write("**Parâmetros enviados:**", params)

    try:
        if method == "GET":
            response = requests.get(url, headers=HEADERS, params=params, timeout=30)
        elif method == "POST":
            response = requests.post(url, headers=HEADERS, json=body, timeout=30)
        elif method == "PUT":
            response = requests.put(url, headers=HEADERS, json=body, timeout=30)
        elif method == "DELETE":
            response = requests.delete(url, headers=HEADERS, timeout=30)
        else:
            st.error("Método HTTP inválido")
            return

        st.write("Status:", response.status_code)
        st.write("Headers:", dict(response.headers))
        st.code(response.text if response.text else "(resposta vazia)")

    except Exception as e:
        st.error(f"Erro na requisição: {e}")

# ================== TABS ==================
tab1, tab2, tab3 = st.tabs([
    "📊 Consultar Pontos",
    "✍️ Registrar Ponto",
    "🔧 Requisição Custom"
])

# ================== TAB 1 ==================
with tab1:
    st.header("Consultar Pontos por Data")

    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("Data Inicial", datetime.now() - timedelta(days=1))
    with col2:
        end_date = st.date_input("Data Final", datetime.now())

    employee_id = st.text_input("Employee ID (opcional)")
    size = st.number_input("Quantidade de registros (size)", value=50)

    if st.button("🔍 Buscar Pontos"):
        params = {
            "startDate": to_millis(start_date),
            "endDate": to_millis(end_date, end_of_day=True),
            "size": size,
            "adjustment": "true"
        }

        if employee_id:
            params["employeeId"] = employee_id

        make_request("GET", "/", params=params)

# ================== TAB 2 ==================
with tab2:
    st.header("Registrar Ponto")

    employee_id = st.text_input("Employee ID", key="emp_reg")
    punch_date = st.date_input("Data do Ponto", datetime.now(), key="date_reg")
    punch_time = st.time_input("Hora do Ponto", datetime.now().time(), key="time_reg")

    if st.button("✍️ Registrar"):
        dt = datetime.combine(punch_date, punch_time).replace(tzinfo=timezone.utc)
        timestamp_ms = int(dt.timestamp() * 1000)

        body = {
            "employeeId": employee_id,
            "date": timestamp_ms
        }

        make_request("POST", "/register", body=body)

# ================== TAB 3 ==================
with tab3:
    st.header("Requisição Personalizada")

    method = st.selectbox("Método", ["GET", "POST", "PUT", "DELETE"])
    endpoint = st.text_input("Endpoint", value="/")

    custom_params = st.text_area("Query Params (JSON)", value='{\n  "size": 10\n}')
    custom_body = st.text_area("Body (JSON)", value='{\n}')

    if st.button("🚀 Enviar"):
        try:
            params = json.loads(custom_params) if custom_params.strip() else None
            body = json.loads(custom_body) if custom_body.strip() else None
            make_request(method, endpoint, params=params, body=body)
        except Exception as e:
            st.error(f"JSON inválido: {e}")

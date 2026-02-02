import streamlit as st
import requests
from datetime import datetime

st.title("🕒 Tangerino – Consulta de Pontos")

employee_id = st.text_input("Employee ID", placeholder="Ex: 5097128")
data_inicio = st.date_input("Data início")
data_fim = st.date_input("Data fim")

BASE_URL = "https://apis.tangerino.com.br/punch/daily-summary"

headers = {
    "accept": "application/json;charset=UTF-8",
    "Authorization": st.secrets["TANGERINO_AUTH"],
}

def to_millis(dt, end_of_day=False):
    if end_of_day:
        dt = datetime.combine(dt, datetime.max.time())
    else:
        dt = datetime.combine(dt, datetime.min.time())
    return int(dt.timestamp() * 1000)

if st.button("📡 Consultar"):
    if not employee_id:
        st.error("Informe o employeeId")
        st.stop()

    if data_inicio > data_fim:
        st.error("Data início maior que data fim")
        st.stop()

    params = {
        "employeeId": employee_id,
        "startDate": to_millis(data_inicio),
        "endDate": to_millis(data_fim),
        "reprocess": "false"
    }

    st.write("🔗 URL:", BASE_URL)
    st.write("📤 Params:", params)

    try:
        response = requests.get(
            BASE_URL,
            headers=headers,
            params=params,
            timeout=30
        )
    except Exception as e:
        st.error(e)
        st.stop()

    st.write("📊 Status:", response.status_code)

    if response.status_code == 200:
        st.success("Requisição OK")
        st.json(response.json())
    else:
        st.error("Erro na requisição")
        st.code(response.text)

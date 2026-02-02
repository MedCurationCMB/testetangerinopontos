import streamlit as st
import requests
from datetime import datetime

st.title("🕒 Tangerino – Punch por Período (Admin)")

data_inicio = st.date_input("Data início")
data_fim = st.date_input("Data fim")

BASE_URL = "https://apis.tangerino.com.br/punch"

headers = {
    "accept": "application/json;charset=UTF-8",
    "Authorization": st.secrets["TANGERINO_AUTH"]
}

def to_millis(date_obj, end=False):
    if end:
        dt = datetime.combine(date_obj, datetime.max.time())
    else:
        dt = datetime.combine(date_obj, datetime.min.time())
    return int(dt.timestamp() * 1000)

if st.button("📡 Consultar"):
    if data_inicio > data_fim:
        st.error("Data início maior que data fim")
        st.stop()

    params = {
        "startDate": to_millis(data_inicio),
        "endDate": to_millis(data_fim),
        "size": 1000,           # evita paginação inicial
        "adjustment": "true"    # padrão usado no swagger
    }

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
    st.write("🔗 URL:", response.url)

    if response.status_code == 200:
        st.success("✔ Dados retornados")
        st.json(response.json())
    else:
        st.error("Erro na requisição")
        st.code(response.text)

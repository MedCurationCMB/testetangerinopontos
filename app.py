import streamlit as st
import requests
from datetime import datetime, timezone, timedelta

st.set_page_config(page_title="Consulta de Pontos Tangerino", layout="wide")
st.title("📊 Consulta de Pontos - Tangerino (API Legacy)")

BASE_URL = "https://apis.tangerino.com.br/punch"

HEADERS = {
    "accept": "application/json;charset=UTF-8",
    "Authorization": st.secrets["TANGERINO_AUTH"]
}

# 🔧 Converte data para timestamp em milissegundos
def to_millis(date_obj, end_of_day=False):
    if end_of_day:
        dt = datetime(date_obj.year, date_obj.month, date_obj.day, 23, 59, 59, tzinfo=timezone.utc)
    else:
        dt = datetime(date_obj.year, date_obj.month, date_obj.day, 0, 0, 0, tzinfo=timezone.utc)
    return int(dt.timestamp() * 1000)

st.header("Filtrar por Período")

col1, col2, col3 = st.columns(3)

with col1:
    start_date = st.date_input("Data Inicial", datetime.now() - timedelta(days=1))

with col2:
    end_date = st.date_input("Data Final", datetime.now())

with col3:
    size = st.number_input("Qtd. Registros", value=50, min_value=1)

employee_id = st.text_input("Employee ID (opcional)")

if st.button("🔍 Buscar Pontos"):
    params = {
        "startDate": to_millis(start_date),
        "endDate": to_millis(end_date, end_of_day=True),
        "size": size,
        "adjustment": "true"
    }

    if employee_id:
        params["employeeId"] = employee_id

    url = f"{BASE_URL}/"

    st.write("### URL da Requisição")
    st.code(url)

    st.write("### Parâmetros Enviados")
    st.json(params)

    try:
        response = requests.get(url, headers=HEADERS, params=params, timeout=30)

        st.write("### Status")
        st.success(response.status_code) if response.status_code == 200 else st.error(response.status_code)

        st.write("### Headers")
        st.json(dict(response.headers))

        st.write("### Resposta")
        if response.text:
            st.code(response.text)
        else:
            st.info("Resposta vazia")

    except Exception as e:
        st.error(f"Erro na requisição: {e}")

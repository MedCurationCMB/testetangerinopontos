import streamlit as st
import requests
from datetime import datetime, timezone

st.title("Teste Tangerino Punch - Dia 29")

# 📅 Data desejada
data_desejada = datetime(2026, 1, 29, 0, 0, 0, tzinfo=timezone.utc)

# 🔢 Converter para timestamp em milissegundos
start_date_ms = int(data_desejada.timestamp() * 1000)

url = f"https://apis.tangerino.com.br/punch/?adjustment=true&size=50&startDate={start_date_ms}"

headers = {
    "accept": "application/json;charset=UTF-8",
    "Authorization": st.secrets["TANGERINO_AUTH"]
}

st.write("URL usada:")
st.code(url)

if st.button("Buscar pontos do dia 29/01/2026"):
    st.write("Fazendo request...")

    try:
        response = requests.get(url, headers=headers, timeout=20)
    except Exception as e:
        st.error(e)
        st.stop()

    st.write("Status:", response.status_code)
    st.write("Headers:", dict(response.headers))
    st.code(response.text if response.text else "(resposta vazia)")

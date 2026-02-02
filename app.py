import streamlit as st
import requests
from datetime import datetime, timedelta

st.title("Teste Tangerino /punch")

# URL corrigida com barra no final
url = "https://apis.tangerino.com.br/punch"

# Headers incluindo User-Agent
headers = {
    "accept": "application/json;charset=UTF-8",
    "Authorization": st.secrets["TANGERINO_AUTH"],
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

# Campos de data
col1, col2 = st.columns(2)
with col1:
    start_date = st.date_input(
        "Data de início",
        value=datetime.now() - timedelta(days=7)
    )
with col2:
    end_date = st.date_input(
        "Data de fim",
        value=datetime.now()
    )

if st.button("Testar endpoint"):
    st.write("Fazendo request...")
    
    # Converter datas para timestamp em milissegundos
    start_datetime = datetime.combine(start_date, datetime.min.time())
    end_datetime = datetime.combine(end_date, datetime.max.time())
    
    start_timestamp = int(start_datetime.timestamp() * 1000)
    end_timestamp = int(end_datetime.timestamp() * 1000)
    
    # Adicionar parâmetros na URL diretamente
    url_with_params = f"{url}?startDate={start_timestamp}&endDate={end_timestamp}"
    
    st.write(f"URL: {url_with_params}")
    
    try:
        # Fazendo request GET SEM params no método, direto na URL
        response = requests.get(url_with_params, headers=headers, timeout=20)
    except Exception as e:
        st.error(e)
        st.stop()
    
    st.write("Status:", response.status_code)
    st.write("Headers:", dict(response.headers))
    st.code(response.text if response.text else "(resposta vazia)")
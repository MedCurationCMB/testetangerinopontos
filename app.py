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
    
    # Parâmetros de query
    params = {
        "startDate": start_date.strftime("%Y-%m-%d"),
        "endDate": end_date.strftime("%Y-%m-%d")
    }
    
    try:
        # Fazendo request GET com parâmetros
        response = requests.get(url, headers=headers, params=params, timeout=20)
    except Exception as e:
        st.error(e)
        st.stop()
    
    st.write("Status:", response.status_code)
    st.write("Headers:", dict(response.headers))
    st.code(response.text if response.text else "(resposta vazia)")
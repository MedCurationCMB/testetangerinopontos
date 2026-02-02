import streamlit as st
import requests
from datetime import datetime

st.title("🔎 Teste de Consulta de Pontos — Tangerino API")

# Inputs de datas
data_inicio = st.date_input("Data Início")
data_fim = st.date_input("Data Fim")

st.write("Selecione o intervalo de datas para consulta de pontos.")

# URL base da API
BASE_URL = "https://apis.tangerino.com.br/punch"

# Headers incluindo User-Agent e Authorization
headers = {
    "accept": "application/json;charset=UTF-8",
    "Authorization": st.secrets["TANGERINO_AUTH"],
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    )
}

if st.button("📡 Consultar Pontos"):
    # Validar intervalo de datas
    if data_inicio > data_fim:
        st.error("❌ A data de início não pode ser posterior à data de fim.")
    else:
        st.info("Fazendo request para o endpoint de pontos...")

        # Converter datas para ISO 8601 (ex: 2026-02-01T00:00:00Z)
        start_iso = datetime.combine(data_inicio, datetime.min.time()).isoformat() + "Z"
        end_iso = datetime.combine(data_fim, datetime.max.time()).isoformat() + "Z"

        params = {
            "startDate": start_iso,
            "endDate": end_iso
        }

        try:
            response = requests.get(BASE_URL, headers=headers, params=params, timeout=30)
        except Exception as e:
            st.error(f"Erro ao conectar: {e}")
            st.stop()

        # Mostrar resultado
        st.write("📊 Status:", response.status_code)
        st.write("📦 URL chamada:", response.url)
        st.code(response.text if response.text else "(nenhum conteúdo retornado)")

        if response.status_code == 200:
            st.success("✔️ Requisição bem-sucedida!")
        else:
            st.warning("⚠️ Houve um problema na requisição.")

import streamlit as st
import requests
import json
from datetime import datetime, timedelta

# Configuração da página
st.set_page_config(page_title="Teste API Tangerino - Punch", layout="wide")

st.title("⏰ Teste API Tangerino - Punch Controller")

# URL base da API
BASE_URL = "https://api.tangerino.com.br/api/punch"

# Header de autorização
HEADERS = {
    "Authorization": "Basic YzM1MDM5MDEyNThhNGU3MGIyYmM4ZjA0NWU0ZTAyYWY6MzE3MmU3M2Y0YTQ2NDliNmE0ZTJhYzFlMjViN2JhMGU=",
    "Content-Type": "application/json"
}

# Função auxiliar para fazer requisições
def make_request(method, endpoint, body=None, params=None):
    try:
        url = f"{BASE_URL}{endpoint}"
        st.info(f"Enviando {method} para: {url}")
        
        if params:
            st.write("**Parâmetros:**", params)
        
        if method == "GET":
            response = requests.get(url, headers=HEADERS, params=params, timeout=30)
        elif method == "POST":
            response = requests.post(url, headers=HEADERS, json=body, params=params, timeout=30)
        elif method == "PUT":
            response = requests.put(url, headers=HEADERS, json=body, params=params, timeout=30)
        elif method == "DELETE":
            response = requests.delete(url, headers=HEADERS, params=params, timeout=30)
        
        # Mostrar resultado
        if response.status_code in [200, 201, 204]:
            st.success(f"✅ Status Code: {response.status_code}")
        else:
            st.warning(f"⚠️ Status Code: {response.status_code}")
        
        # Headers da resposta
        with st.expander("📋 Headers da Resposta"):
            st.json(dict(response.headers))
        
        # Corpo da resposta
        st.subheader("Resposta:")
        try:
            if response.text:
                response_json = response.json()
                st.json(response_json)
            else:
                st.info("Resposta vazia (sem conteúdo)")
        except:
            st.code(response.text)
            
    except requests.exceptions.Timeout:
        st.error("❌ Erro: Timeout na requisição (30s)")
    except requests.exceptions.RequestException as e:
        st.error(f"❌ Erro na requisição: {str(e)}")
    except Exception as e:
        st.error(f"❌ Erro: {str(e)}")

# Tabs principais
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📊 Consultas GET",
    "✍️ Registro de Ponto",
    "👤 Reconhecimento Facial",
    "🔄 Atualizar/Deletar",
    "🔧 Custom Request",
    "📖 Documentação"
])

# TAB 1: Consultas GET
with tab1:
    st.header("Consultas de Pontos")
    
    endpoint_get = st.selectbox(
        "Selecione o endpoint GET:",
        [
            "/ - Find Punch By Filter",
            "/daily-activity - Find Employee Hours Balance By Filter",
            "/closure - Find Closure By Filter",
            "/hoursBalance - Find Employee Hours Balance By Filter",
            "/observation-historical - List observation historical by punch",
            "/summary - Find Punch By Filter",
            "/verify-interval-inconsistence - Verify inconsistence in interval"
        ]
    )
    
    # Campos de filtro comuns
    st.subheader("Filtros")
    col1, col2 = st.columns(2)
    
    with col1:
        start_date = st.date_input("Data Inicial", datetime.now() - timedelta(days=7))
        employee_id = st.text_input("Employee ID (opcional)")
    
    with col2:
        end_date = st.date_input("Data Final", datetime.now())
        company_id = st.text_input("Company ID (opcional)")
    
    if st.button("🔍 Consultar", key="btn_get"):
        endpoint_map = {
            "/ - Find Punch By Filter": "/",
            "/daily-activity - Find Employee Hours Balance By Filter": "/daily-activity",
            "/closure - Find Closure By Filter": "/closure",
            "/hoursBalance - Find Employee Hours Balance By Filter": "/hoursBalance",
            "/observation-historical - List observation historical by punch": "/observation-historical",
            "/summary - Find Punch By Filter": "/summary",
            "/verify-interval-inconsistence - Verify inconsistence in interval": "/verify-interval-inconsistence"
        }
        
        selected_endpoint = endpoint_map[endpoint_get]
        
        # Construir parâmetros
        from datetime import datetime

        def format_date_safe(d):
            # força meio-dia para evitar virar o dia no UTC
            return datetime(d.year, d.month, d.day, 12, 0, 0).strftime("%Y-%m-%d")

        params = {
            "startDate": start_date.strftime("%Y-%m-%dT00:00:00"),
            "endDate": end_date.strftime("%Y-%m-%dT23:59:59"),
            "size": 50  # opcional mas ajuda
        }
        
        if employee_id:
            params["employeeId"] = employee_id
        if company_id:
            params["companyId"] = company_id
        
        make_request("GET", selected_endpoint, params=params)

# TAB 2: Registro de Ponto
with tab2:
    st.header("Registro de Ponto")
    
    endpoint_post = st.selectbox(
        "Selecione o tipo de registro:",
        [
            "/register/web/1.1 - Submit web punch",
            "/register/app/1.1 - Submit app punch",
            "/register/lite/1.1 - Submit Punch Lite",
            "/register/lite/punchs - Submit List Punch Lite",
            "/register/late/1.1 - Submit late punch",
            "/modify/punch/1.1 - Submit Punch Web (modificação)"
        ]
    )
    
    st.subheader("Dados do Ponto")
    
    col1, col2 = st.columns(2)
    with col1:
        punch_employee_id = st.text_input("Employee ID", key="punch_emp_id")
        punch_date = st.date_input("Data do Ponto", datetime.now(), key="punch_date")
    
    with col2:
        punch_time = st.time_input("Hora do Ponto", datetime.now().time(), key="punch_time")
        punch_type = st.selectbox("Tipo", ["ENTRY", "EXIT"], key="punch_type")
    
    # JSON Body personalizado
    st.subheader("Body JSON (personalize se necessário)")
    default_body = {
        "employeeId": punch_employee_id,
        "punchDate": f"{punch_date.strftime('%Y-%m-%d')}T{punch_time.strftime('%H:%M:%S')}",
        "type": punch_type
    }
    
    body_json = st.text_area(
        "JSON Body",
        value=json.dumps(default_body, indent=2),
        height=200,
        key="punch_body"
    )
    
    if st.button("✍️ Registrar Ponto", key="btn_register"):
        endpoint_map = {
            "/register/web/1.1 - Submit web punch": "/register/web/1.1",
            "/register/app/1.1 - Submit app punch": "/register/app/1.1",
            "/register/lite/1.1 - Submit Punch Lite": "/register/lite/1.1",
            "/register/lite/punchs - Submit List Punch Lite": "/register/lite/punchs",
            "/register/late/1.1 - Submit late punch": "/register/late/1.1",
            "/modify/punch/1.1 - Submit Punch Web (modificação)": "/modify/punch/1.1"
        }
        
        selected_endpoint = endpoint_map[endpoint_post]
        
        try:
            body = json.loads(body_json)
            make_request("POST", selected_endpoint, body=body)
        except json.JSONDecodeError:
            st.error("❌ Erro: JSON inválido no body")

# TAB 3: Reconhecimento Facial
with tab3:
    st.header("Reconhecimento Facial")
    
    facial_endpoint = st.selectbox(
        "Selecione o endpoint de reconhecimento:",
        [
            "/facial/recognize - Facial Employee Recognize",
            "/facial/{employeeId}/validation - Facial Employee Photo Validation",
            "/facial/{punchId}/recognition - Facial Recognition"
        ]
    )
    
    if "employeeId" in facial_endpoint:
        facial_employee_id = st.text_input("Employee ID")
    
    if "punchId" in facial_endpoint:
        facial_punch_id = st.text_input("Punch ID")
    
    st.subheader("Body JSON")
    facial_body = st.text_area(
        "JSON Body",
        value='{\n  "image": "base64_encoded_image_here"\n}',
        height=150,
        key="facial_body"
    )
    
    if st.button("🔍 Processar Facial", key="btn_facial"):
        try:
            body = json.loads(facial_body)
            
            if facial_endpoint == "/facial/recognize - Facial Employee Recognize":
                endpoint = "/facial/recognize"
            elif "validation" in facial_endpoint:
                endpoint = f"/facial/{facial_employee_id}/validation"
            else:
                endpoint = f"/facial/{facial_punch_id}/recognition"
            
            make_request("POST", endpoint, body=body)
        except json.JSONDecodeError:
            st.error("❌ Erro: JSON inválido no body")

# TAB 4: Atualizar/Deletar
with tab4:
    st.header("Atualizar ou Deletar Pontos")
    
    operation = st.radio("Operação:", ["Atualizar Status (PUT)", "Deletar Ponto (DELETE)"])
    
    if operation == "Atualizar Status (PUT)":
        st.subheader("PUT /{punchId}/status/{status}")
        
        col1, col2 = st.columns(2)
        with col1:
            put_punch_id = st.text_input("Punch ID", key="put_punch_id")
        with col2:
            put_status = st.selectbox("Novo Status", ["APPROVED", "REJECTED", "PENDING"], key="put_status")
        
        if st.button("🔄 Atualizar Status", key="btn_put"):
            endpoint = f"/{put_punch_id}/status/{put_status}"
            make_request("PUT", endpoint)
    
    else:
        st.subheader("DELETE /punches/{punchId}/employee/{employeeId}")
        
        col1, col2 = st.columns(2)
        with col1:
            del_punch_id = st.text_input("Punch ID", key="del_punch_id")
        with col2:
            del_employee_id = st.text_input("Employee ID", key="del_emp_id")
        
        st.warning("⚠️ Esta operação é irreversível!")
        
        if st.button("🗑️ Deletar Ponto", key="btn_delete"):
            endpoint = f"/punches/{del_punch_id}/employee/{del_employee_id}"
            make_request("DELETE", endpoint)

# TAB 5: Custom Request
with tab5:
    st.header("Requisição Personalizada")
    
    col1, col2 = st.columns([1, 3])
    
    with col1:
        custom_method = st.selectbox("Método", ["GET", "POST", "PUT", "DELETE"], key="custom_method")
    
    with col2:
        custom_endpoint = st.text_input(
            "Endpoint", 
            value="/",
            help="Digite o endpoint completo, ex: /daily-activity",
            key="custom_endpoint"
        )
    
    # Query Parameters
    st.subheader("Query Parameters (opcional)")
    custom_params = st.text_area(
        "Parâmetros (JSON)",
        value='{\n  "startDate": "2025-01-01",\n  "endDate": "2025-01-31"\n}',
        height=100,
        key="custom_params"
    )
    
    # Body (se POST/PUT)
    if custom_method in ["POST", "PUT"]:
        st.subheader("Body da Requisição (JSON)")
        custom_body = st.text_area(
            "JSON Body",
            value='{\n  "exemplo": "valor"\n}',
            height=150,
            key="custom_body"
        )
    
    if st.button("🚀 Enviar Requisição Custom", type="primary", key="btn_custom"):
        try:
            params = json.loads(custom_params) if custom_params.strip() else None
            
            if custom_method in ["POST", "PUT"]:
                body = json.loads(custom_body)
                make_request(custom_method, custom_endpoint, body=body, params=params)
            else:
                make_request(custom_method, custom_endpoint, params=params)
                
        except json.JSONDecodeError as e:
            st.error(f"❌ Erro: JSON inválido - {str(e)}")

# TAB 6: Documentação
with tab6:
    st.header("📖 Documentação da API")
    
    st.write("**Base URL:**", BASE_URL)
    st.write("**Swagger:**", "https://api.tangerino.com.br/api/punch/swagger-ui.html#/punch-controller")
    st.write("**Autorização:** Basic (pré-configurada)")
    
    st.divider()
    
    st.subheader("Endpoints Disponíveis")
    
    with st.expander("🔍 GET - Consultas"):
        st.code("""
GET  /                              - Find Punch By Filter
GET  /daily-activity                - Find Employee Hours Balance By Filter
GET  /closure                       - Find Closure By Filter
GET  /hoursBalance                  - Find Employee Hours Balance By Filter
GET  /observation-historical        - List observation historical by punch
GET  /summary                       - Find Punch By Filter
GET  /verify-interval-inconsistence - Verify inconsistence in interval
        """, language="bash")
    
    with st.expander("✍️ POST - Registro de Pontos"):
        st.code("""
POST /register/web/1.1        - Submit web punch
POST /register/app/1.1        - Submit app punch
POST /register/lite/1.1       - Submit Punch Lite
POST /register/lite/punchs    - Submit List Punch Lite
POST /register/late/1.1       - Submit late punch
POST /modify/punch/1.1        - Submit Punch Web (modificação)
        """, language="bash")
    
    with st.expander("👤 POST - Reconhecimento Facial"):
        st.code("""
POST /facial/recognize                     - Facial Employee Recognize
POST /facial/{employeeId}/validation       - Facial Employee Photo Validation
POST /facial/{punchId}/recognition         - Facial Recognition
        """, language="bash")
    
    with st.expander("🔄 PUT - Atualizar"):
        st.code("""
PUT  /{punchId}/status/{status}  - Atualizar status do ponto
        """, language="bash")
    
    with st.expander("🗑️ DELETE - Deletar"):
        st.code("""
DELETE /punches/{punchId}/employee/{employeeId}  - Delete Punch
        """, language="bash")

# Informações na sidebar
with st.sidebar:
    st.image("https://www.tangerino.com.br/wp-content/uploads/2021/06/logo-tangerino.svg", width=200)
    st.markdown("---")
    st.subheader("ℹ️ Sobre")
    st.write("Aplicação para teste da API de Ponto do Tangerino")
    st.write("Versão: 1.0")
    st.markdown("---")
    st.subheader("🔑 Status")
    st.success("✅ Autenticação: Configurada")
    st.info(f"🌐 Base URL: {BASE_URL}")
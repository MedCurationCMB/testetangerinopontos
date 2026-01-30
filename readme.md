# Teste API Tangerino - Punch Controller ⏰

Aplicação completa em Streamlit para testar a API de Ponto (Punch) do Tangerino.

## 🎯 Funcionalidades

### 1. 📊 Consultas GET
Endpoints para buscar informações de pontos:
- **/** - Find Punch By Filter
- **/daily-activity** - Find Employee Hours Balance By Filter
- **/closure** - Find Closure By Filter
- **/hoursBalance** - Find Employee Hours Balance By Filter
- **/observation-historical** - List observation historical by punch
- **/summary** - Find Punch By Filter
- **/verify-interval-inconsistence** - Verify inconsistence in interval

### 2. ✍️ Registro de Ponto
Endpoints para registrar pontos:
- **/register/web/1.1** - Submit web punch
- **/register/app/1.1** - Submit app punch
- **/register/lite/1.1** - Submit Punch Lite
- **/register/lite/punchs** - Submit List Punch Lite
- **/register/late/1.1** - Submit late punch
- **/modify/punch/1.1** - Submit Punch Web (modificação)

### 3. 👤 Reconhecimento Facial
Endpoints para processar reconhecimento facial:
- **/facial/recognize** - Facial Employee Recognize
- **/facial/{employeeId}/validation** - Facial Employee Photo Validation
- **/facial/{punchId}/recognition** - Facial Recognition

### 4. 🔄 Atualizar/Deletar
- **PUT /{punchId}/status/{status}** - Atualizar status do ponto
- **DELETE /punches/{punchId}/employee/{employeeId}** - Delete Punch

### 5. 🔧 Custom Request
Interface para fazer requisições personalizadas com qualquer endpoint.

## 📦 Instalação

1. Instale as dependências:
```bash
pip install -r requirements_punch.txt
```

## 🚀 Como usar

1. Execute a aplicação:
```bash
streamlit run test_tangerino_punch_api.py
```

2. A aplicação abrirá automaticamente no navegador (http://localhost:8501)

3. Navegue pelas abas:
   - **📊 Consultas GET**: Busque pontos e informações com filtros de data
   - **✍️ Registro de Ponto**: Registre novos pontos via web/app/lite
   - **👤 Reconhecimento Facial**: Teste endpoints de reconhecimento facial
   - **🔄 Atualizar/Deletar**: Atualize status ou delete pontos
   - **🔧 Custom Request**: Faça requisições personalizadas
   - **📖 Documentação**: Veja todos os endpoints disponíveis

## 💡 Exemplos de Uso

### Consultar pontos de um período
1. Vá para aba "Consultas GET"
2. Selecione "/ - Find Punch By Filter"
3. Defina data inicial e final
4. Adicione Employee ID (opcional)
5. Clique em "Consultar"

### Registrar um novo ponto
1. Vá para aba "Registro de Ponto"
2. Selecione "/register/web/1.1"
3. Preencha Employee ID, data e hora
4. Escolha o tipo (ENTRY/EXIT)
5. Clique em "Registrar Ponto"

### Atualizar status de um ponto
1. Vá para aba "Atualizar/Deletar"
2. Selecione "Atualizar Status (PUT)"
3. Digite o Punch ID
4. Escolha o novo status
5. Clique em "Atualizar Status"

## 🔑 Autenticação

A autorização Basic já está pré-configurada no código:
```
Authorization: Basic YzM1MDM5MDEyNThhNGU3MGIyYmM4ZjA0NWU0ZTAyYWY6MzE3MmU3M2Y0YTQ2NDliNmE0ZTJhYzFlMjViN2JhMGU=
```

## 📝 Notas Importantes

- Todos os campos de data usam formato: `YYYY-MM-DD`
- Campos de datetime usam formato: `YYYY-MM-DDTHH:MM:SS`
- Status válidos para PUT: `APPROVED`, `REJECTED`, `PENDING`
- Tipos de ponto válidos: `ENTRY`, `EXIT`
- Timeout das requisições: 30 segundos

## 🌐 Links Úteis

- **Base URL**: https://api.tangerino.com.br/api/punch
- **Documentação Swagger**: https://api.tangerino.com.br/api/punch/swagger-ui.html#/punch-controller

## ✨ Features

- ✅ Interface intuitiva com 6 abas organizadas
- ✅ Autorização pré-configurada
- ✅ Validação de JSON
- ✅ Visualização completa de respostas (status, headers, body)
- ✅ Tratamento de erros e timeouts
- ✅ Filtros de data para consultas
- ✅ Formulários específicos por tipo de endpoint
- ✅ Documentação integrada na aplicação
- ✅ Sidebar com informações de status

## 🎨 Interface

A aplicação possui uma sidebar com:
- Logo do Tangerino
- Status da autenticação
- Base URL configurada

E uma área principal com abas para cada tipo de operação, facilitando a navegação e testes.
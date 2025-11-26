# Intellecta AI (Mentor de Estudos com Gemini)

Este é um projeto de um assistente de estudos (Mentor) que utiliza a API do Google Gemini. A aplicação é dividida em um frontend moderno em React (construído com Vite) e um backend em Python (Flask) que serve como uma API.



## 🧠 Arquitetura

O projeto é uma **Single Page Application (SPA)** com uma arquitetura desacoplada:

* **Frontend (pasta `/frontend-react`):** Um cliente React que gerencia toda a interface do usuário, rotas e estado. Ele se comunica com o backend via requisições HTTP.
* **Backend (pasta `/backend-flask`):** Uma API RESTful em Python/Flask que processa as requisições, gerencia o estado da conversa e se comunica com a API do Google Gemini.

## ✨ Tecnologias Utilizadas

* **Frontend:**
    * React
    * Vite (Servidor de desenvolvimento)
    * `react-router-dom` (Para roteamento de páginas)
* **Backend:**
    * Python
    * Flask (Servidor da API)
    * `flask-cors` (Para permitir a comunicação entre frontend e backend)
    * `google-generativeai` (Biblioteca oficial do Google)

---

## 🔑 Configuração Essencial: Chave da API

Este projeto necessita de uma chave de API do Google Gemini para o backend funcionar.

1.  Obtenha sua chave de API gratuitamente no [Google AI Studio](https://aistudio.google.com/app/apikey).
2.  Abra o arquivo `backend-flask/app.py`.
3.  Encontre a linha:
    ```python
    MINHA_CHAVE_SECRETA = "Uma chave do gemini"
    ```
4.  Substitua `"Uma chave do gemini"` pela sua chave de API real.

**Aviso Importante:** Não suba este arquivo para um repositório público com sua chave visível. Para produção, é altamente recomendado usar Variáveis de Ambiente (ex: arquivos `.env` ou segredos do repositório).

---

## 🚀 Como Rodar o Projeto

Este projeto deve ser executado em **dois terminais separados**: um para o Backend e um para o Frontend.

### 1. Backend (Servidor Flask)

1.  Navegue até a pasta do backend:
    ```bash
    cd backend-flask
    ```
2.  Crie um ambiente virtual (venv):
    ```bash
    python -m venv venv
    ```
3.  Ative o ambiente virtual:
    * **Windows:** `.\venv\Scripts\activate`
    * **Mac/Linux:** `source venv/bin/activate`
4.  Instale as dependências do Python (usando o arquivo que você criou):
    ```bash
    pip install -r requirements.txt
    ```
    *(Se você não criou o `requirements.txt`, rode: `pip install flask flask-cors google-generativeai sqlalchemy psycopg`)*
5.  Rode o servidor Flask:
    ```bash
    python app.py
    ```
✅ O backend estará rodando em `http://127.0.0.1:5000`. Deixe este terminal aberto.

### 2. Frontend (Cliente React)

1.  Abra um **novo terminal**.
2.  Navegue até a pasta do frontend:
    ```bash
    cd frontend-react
    ```
3.  Instale as dependências do Node.js:
    ```bash
    npm install
    ```
4.  Rode o servidor de desenvolvimento (Vite):
    ```bash
    npm run dev
    ```
✅ O frontend estará rodando em `http://localhost:5173` (ou uma porta similar).

### 3. Acessando a Aplicação

1.  Com os **dois servidores rodando**, abra seu navegador.
2.  Acesse o endereço do **frontend:** `http://localhost:5173`.
3.  Para testar o login (simulado), use as credenciais definidas no `app.py`:
    * **E-mail:** `aluno@email.com`
    * **Senha:** `1234`
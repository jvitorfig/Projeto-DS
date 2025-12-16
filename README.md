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

## 🚀 Instruções para a Build

Este projeto deve ser executado em **dois terminais separados**: um para o Backend e um para o Frontend.
### 1. Banco de Dados:
Para rodar o projeto na sua máquina, você precisa configurar o banco de dados. O projeto está preparado para criar as tabelas automaticamente na primeira execução.
Opção A: PostgreSQL (Recomendado)
1.  Instale o PostgreSQL:
    Baixe e instale o PostgreSQL para seu sistema operacional.
    Durante a instalação, defina uma senha para o usuário postgres (anote essa senha!).

2.  Crie o Banco de Dados:
    Abra o pgAdmin (que vem com a instalação) ou use o terminal.
    Crie um novo banco de dados vazio chamado tutor_db (ou outro nome de sua preferência).

3.  Configure o .env:
    No arquivo .env da raiz do backend, a variável DATABASE_URL deve seguir este formato:
    # Formato: postgresql://USUARIO:SENHA@LOCALHOST:PORTA/NOME_DO_BANCO
    DATABASE_URL=postgresql://postgres:sua_senha_aqui@localhost:5432/tutor_db


Opção B: SQLite 
Se você não quiser instalar o PostgreSQL agora, pode usar o SQLite (um banco que é apenas um arquivo).
1.  Configure o .env

2.  Basta alterar a variável de conexão para apontar para um arquivo local:
    DATABASE_URL=sqlite:///database.db


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

## 🚀 Instruções de Deploy
    Este guia descreve os passos para realizar o deploy da solução em produção utilizando Render (Backend e Banco de Dados) e Vercel (Frontend).


## 🛠️ Pré-requisitos (Contas)

Antes de começar, certifique-se de ter contas nas seguintes plataformas:
1.  Render (para Backend e Banco de Dados)
2.  Vercel (para Frontend)
3.  Google AI Studio (para a chave da API Gemini)


## ☁️ Passo a Passo do Deploy

Passo 1: Banco de Dados (Render)
    No painel do Render, clique em New + > PostgreSQL.
    Defina um nome (ex: db-tutor).
    Após criar, copie a Internal Database URL (começa com postgres://...). Você precisará dela no próximo passo.

Passo 2: Backend (Render)
    No painel do Render, clique em New + > Web Service.
    Conecte o repositório do GitHub onde está o código do Backend.
    Preencha as configurações:
    Runtime: Python 3
    Build Command: pip install -r requirements.txt
    Start Command: gunicorn app:app
    Vá na aba Environment Variables e adicione:
    DATABASE_URL: (Cole a URL interna do banco criada no Passo 1)
    MINHA_CHAVE_SECRETA: (Cole sua chave da API do Google Gemini)
    Clique em Create Web Service.
    Aguarde o deploy finalizar e anote a URL gerada (ex: https://projeto-ds-qs25.onrender.com).

Passo 3: Frontend (Vercel)
    No dashboard da Vercel, clique em Add New... > Project.
    Importe o repositório do GitHub onde está o código do Frontend.
    Selecione a pasta raiz do frontend (se o repositório tiver pastas separadas para back e front).
    O Framework Preset deve detectar automaticamente (Vite ou Create React App).
    IMPORTANTE: Configuração da API.
    Se você configurou o código para ler variáveis de ambiente (ex: VITE_API_URL), adicione a variável nas configurações da Vercel com a URL do Backend criada no Passo 2.
    Caso contrário, certifique-se de ter alterado a constante API_URL no código fonte para a URL do Render antes de fazer o push para o GitHub.
    Clique em Deploy.

    
## 🔍 Testando a Solução
1.    Acesse o link gerado pela Vercel.
2.    Tente fazer Login ou Cadastro (isso valida a conexão Frontend -> Backend -> Banco de Dados).
3.    Envie uma mensagem no Chat (isso valida a conexão Backend -> Google Gemini API).

import os # Para carregar variáveis de ambiente
from dotenv import load_dotenv # Para carregar o .env
import google.generativeai as genai # A IA do Google

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Carrega as variáveis do arquivo .env (onde está sua chave)
load_dotenv()

# Configura a API do Google
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("Chave de API do Google não encontrada. Verifique seu arquivo .env")
genai.configure(api_key=api_key)

# Inicializa o modelo de IA
model = genai.GenerativeModel('gemini-1.5-flash') # Usando o modelo "flash" (rápido)

# ---- Restante do código FastAPI (igual a antes) ----

app = FastAPI()

origins = [
    "http://localhost:5173",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Message(BaseModel):
    text: str

@app.get("/")
def read_root():
    return {"Hello": "World"}


# --- ESTA É A PARTE QUE MUDA ---
@app.post("/api/chat")
def chat_endpoint(message: Message):
    try:
        # Envia a mensagem do usuário para a IA
        response = model.generate_content(message.text)
        
        # Retorna a resposta da IA para o React
        print(f"Usuário: {message.text}")
        print(f"IA: {response.text}")
        return {"response": response.text}
    except Exception as e:
        print(f"Erro ao chamar a API do Gemini: {e}")
        return {"response": "Desculpe, ocorreu um erro ao me conectar com a IA."}
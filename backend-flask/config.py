# config.py
import os

# Lê variável de ambiente GEMINI_API_KEY
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise RuntimeError(
        "ERRO: Variável de ambiente GEMINI_API_KEY não definida. "
        "Crie uma nova chave no Google e exporte antes de rodar o app."
    )

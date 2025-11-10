# app.py
import google.generativeai as genai
import os
from flask import Flask, request, jsonify, g
from flask_cors import CORS
from werkzeug.security import check_password_hash # Só precisamos do check aqui

# --- Importações da sua nova arquitetura ---
# (Assumindo que seus arquivos estão em pastas/módulos corretos)
# (Ajuste os imports se sua estrutura de pastas for diferente)
try:
    from db import SessionLocal, engine
    from models import Base
    from repositories.userRepository import UserRepository
    from service.userService import UserService
    from dtos.userDto import UserDto # Embora não seja usado diretamente aqui, é bom saber
except ImportError:
    print("ERRO DE IMPORTAÇÃO: Verifique sua estrutura de pastas e __init__.py")
    # Tente imports locais se estiver tudo na mesma pasta (menos ideal)
    from db import SessionLocal, engine
    from models import Base, Usuario
    from repositories.userRepository import UserRepository
    from service.userService import UserService
    from dtos.userDto import UserDto


# --- Configuração do Gemini (Sem Alterações) ---
# ... (seu código de configuração do Gemini vai aqui) ...
MINHA_CHAVE_SECRETA = "SUA_CHAVE_GEMINI_REAL_AQUI" 
genai.configure(api_key=MINHA_CHAVE_SECRETA)
instrucoes_do_sistema = """...""" # Suas instruções
model = genai.GenerativeModel(...)
# ... (fim da configuração do Gemini) ...


# --- Início da Lógica do Servidor Web com Flask ---

app = Flask(__name__)
CORS(app) 

# --- NOVO: Criação das Tabelas ---
# Ao iniciar o app, ele garante que as tabelas do models.py existam
try:
    Base.metadata.create_all(bind=engine)
    print("INFO: Tabelas do SQLAlchemy verificadas/criadas.")
except Exception as e:
    print(f"ERRO ao criar tabelas: {e}")


# --- NOVO: Gerenciamento da Sessão SQLAlchemy ---
# Vamos usar o 'g' do Flask para guardar a sessão por request
@app.before_request
def create_session():
    """Abre uma nova sessão no início de cada request."""
    g.session = SessionLocal()

@app.teardown_request
def close_session(e=None):
    """Fecha a sessão no final de cada request."""
    session = g.pop('session', None)
    if session is not None:
        session.close()


# --- Lógica do Chat (Sem Alterações) ---
try:
    chat = model.start_chat(history=[])
    inicial_response = chat.send_message("Ola")
    PRIMEIRA_MENSAGEM_MENTOR = inicial_response.text
except Exception as e:
    print(f"Erro ao inicializar o chat com o Gemini: {e}")
    PRIMEIRA_MENSAGEM_MENTOR = "Olá! Tive um problema para me conectar. Por favor, tente recarregar a página."

@app.route("/chat", methods=['POST'])
def handle_chat():
    # ... (sem alterações) ...
    pass

@app.route("/api/initial-message", methods=['GET'])
def get_initial_message():
    # ... (sem alterações) ...
    pass
# --- Fim da Lógica do Chat ---


# --- ROTAS DE AUTENTICAÇÃO (Totalmente Reescritas) ---

@app.route("/api/register", methods=['POST'])
def handle_register():
    data = request.json
    nome = data.get('nome')
    email = data.get('email')
    senha = data.get('senha')

    try:
        # 1. Instanciamos os serviços com a sessão do request (g.session)
        repo = UserRepository(g.session)
        service = UserService(repo)
        
        # 2. Chamamos o serviço (que precisa ser ajustado para senhas)
        #    (Veja a Seção 2 abaixo!)
        new_user = service.create_user(nome, email, senha)
        
        return jsonify({'success': True, 'message': 'Usuário cadastrado com sucesso!', 'user_id': new_user.id}), 201
    
    except ValueError as e:
        # Erros de negócio (ex: "E-mail já existe")
        return jsonify({'success': False, 'error': str(e)}), 400
    except Exception as e:
        # Erros inesperados
        return jsonify({'success': False, 'error': f'Erro interno: {str(e)}'}), 500

@app.route("/api/login", methods=['POST'])
def handle_login():
    data = request.json
    email = data.get('email')
    senha = data.get('senha')

    if not email or not senha:
        return jsonify({'success': False, 'error': 'E-mail e senha são obrigatórios'}), 400

    try:
        # 1. Instanciamos os serviços
        repo = UserRepository(g.session)
        service = UserService(repo)

        # 2. Chamamos um novo serviço de autenticação
        #    (Veja a Seção 2 abaixo!)
        user = service.authenticate_user(email, senha)
        
        return jsonify({'success': True, 'message': 'Login bem-sucedido!'})

    except ValueError as e:
        # Erro de autenticação (ex: "Senha inválida")
        return jsonify({'success': False, 'error': str(e)}), 401
    except Exception as e:
        return jsonify({'success': False, 'error': f'Erro interno: {str(e)}'}), 500


if __name__ == '__main__':
    app.run(debug=True, port=5000)
import os
from flask import Flask, request, jsonify, g
from flask_cors import CORS

# --- IMPORTS DA NOVA ARQUITETURA ---
try:
    from db import SessionLocal, engine
    from models.models import Base
    from repositories.userRepository import UserRepository
    from repositories.exerciseRepository import ExerciseRepository
    from services.userService import UserService
    from services.exerciseService import ExerciseService
    # Se você criou o chatService.py, descomente a linha abaixo:
    # from services.chatService import ChatService 
except ImportError as e:
    print(f"ERRO CRÍTICO DE IMPORTAÇÃO: {e}")
    print("Verifique se as pastas 'services' e 'repositories' contêm os arquivos __init__.py ou se os nomes estão corretos.")

app = Flask(__name__)
CORS(app)

# Criação das tabelas no banco (se não existirem)
try:
    Base.metadata.create_all(bind=engine)
    print("Banco de dados conectado e tabelas verificadas.")
except Exception as e:
    print(f"ERRO DE BANCO: {e}")
    print("DICA: Verifique se o PostgreSQL está ligado e se a senha no db.py está certa.")

# --- CONFIGURAÇÃO DA SESSÃO POR REQUEST ---
@app.before_request
def create_session():
    g.session = SessionLocal()

@app.teardown_request
def close_session(e=None):
    session = g.pop('session', None)
    if session is not None:
        session.close()

# --- HELPER PARA INSTANCIAR SERVIÇOS ---
def get_exercise_service():
    # ⚠️ COLOQUE SUA CHAVE DO GOOGLE AQUI PARA TESTAR ⚠️
    api_key = os.getenv("GEMINI_API_KEY", "SUA_CHAVE_AQUI") 
    
    repo = ExerciseRepository(g.session)
    return ExerciseService(repo, api_key)

# ==========================================
# ROTAS DE USUÁRIO (Chamando UserService)
# ==========================================

@app.route("/api/register", methods=['POST'])
def handle_register():
    data = request.json
    try:
        repo = UserRepository(g.session)
        service = UserService(repo)
        # O service cuida de validar e criar
        new_user = service.create_user(data.get('nome'), data.get('email'), data.get('senha'))
        return jsonify({'success': True, 'user_id': new_user.id}), 201
    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 400
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route("/api/login", methods=['POST'])
def handle_login():
    data = request.json
    try:
        repo = UserRepository(g.session)
        service = UserService(repo)
        # O service cuida de verificar a senha
        user = service.authenticate_user(data.get('email'), data.get('senha'))
        return jsonify({'success': True, 'user': {'id': user.id, 'nome': user.nome}})
    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 401
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# ==========================================
# ROTAS DE EXERCÍCIO (Chamando ExerciseService)
# ==========================================

@app.route("/api/generate-exercise", methods=['POST'])
def generate_exercise():
    try:
        topic = request.json.get("topic", "Geral")
        
        # 1. Instancia o serviço
        service = get_exercise_service()
        # 2. Pede a questão (o Service fala com a IA)
        question_json = service.generate_question(topic)
        
        return jsonify(question_json)

    except Exception as e:
        print(f"Erro: {e}")
        return jsonify({"error": str(e)}), 500

@app.route("/api/correct-exercise", methods=['POST'])
def correct_exercise():
    try:
        data = request.json
        user_id = data.get("user_id")
        
        if not user_id:
            return jsonify({"error": "user_id obrigatório"}), 400

        service = get_exercise_service()
        
        # O Service corrige E salva no banco
        result = service.correct_and_save(
            user_id=user_id,
            topic=data.get("topic"),
            exercise_data=data.get("exercise"),
            answer=data.get("answer")
        )

        return jsonify(result)

    except Exception as e:
        g.session.rollback() # Segurança
        print(f"Erro: {e}")
        return jsonify({"error": str(e)}), 500

@app.route("/api/user-stats/<int:user_id>", methods=['GET'])
def get_user_stats(user_id):
    try:
        service = get_exercise_service()
        
        # O Service faz a matemática das estatísticas
        stats = service.calculate_stats(user_id)
        
        return jsonify(stats)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ==========================================
# ROTA DO CHAT (Se tiver o ChatService)
# ==========================================
# @app.route("/chat", methods=['POST'])
# def handle_chat():
#     # ... implementação chamando ChatService ...
#     pass

if __name__ == '__main__':
    app.run(debug=True, port=5000)
import re
import json
import google.generativeai as genai
import os
import sys
from flask import Flask, request, jsonify, g
from flask_cors import CORS

# --- Importações da sua arquitetura ---
try:
    from db import SessionLocal, engine
    from models.models import Base, HistoricoExercicio
    from repositories.userRepository import UserRepository
    from service.userService import UserService
except ImportError:
    print("AVISO: Usando imports locais.")
    from db import SessionLocal, engine
    from models.models import Base, HistoricoExercicio
    from repositories.userRepository import UserRepository
    from service.userService import UserService

# --- Configuração do Gemini ---
MINHA_CHAVE_SECRETA = os.getenv("MINHA_CHAVE_SECRETA")
if not MINHA_CHAVE_SECRETA:
    print("ERRO CRÍTICO: Chave API não encontrada!")

genai.configure(api_key=MINHA_CHAVE_SECRETA)

instrucoes_do_sistema = """
Você é um Tutor Socrático chamado "Mentor". 
NUNCA dê a resposta direta. Faça perguntas para guiar o aluno.
Seja encorajador e paciente.
"""

# --- SELEÇÃO AUTOMÁTICA DE MODELO (A MÁGICA) ---
def escolher_melhor_modelo():
    """Lista os modelos disponíveis na sua conta e pega o melhor."""
    print("--- INICIANDO BUSCA DE MODELOS ---")
    try:
        modelos_disponiveis = []
        melhor_modelo_chat = None
        melhor_modelo_exercicio = None

        # Pede ao Google a lista real
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                print(f"Modelo encontrado: {m.name}")
                modelos_disponiveis.append(m.name)
                
                # Lógica de preferência
                if "1.5-pro" in m.name and "latest" not in m.name:
                    melhor_modelo_chat = m.name
                if "1.5-flash" in m.name and "latest" not in m.name:
                    melhor_modelo_exercicio = m.name

        # Se não achou os preferidos, pega o primeiro da lista que seja 'gemini'
        if not melhor_modelo_chat:
             # Tenta achar qualquer um com 'gemini'
            melhor_modelo_chat = next((m for m in modelos_disponiveis if 'gemini' in m), 'models/gemini-pro')
        
        if not melhor_modelo_exercicio:
            melhor_modelo_exercicio = mejor_modelo_chat

        print(f"--- MODELOS ESCOLHIDOS ---")
        print(f"Chat: {melhor_modelo_chat}")
        print(f"Exercícios: {melhor_modelo_exercicio}")
        
        return mejor_modelo_chat, melhor_modelo_exercicio

    except Exception as e:
        print(f"ERRO AO LISTAR MODELOS: {e}")
        # Fallback de emergência
        return "models/gemini-1.5-flash", "models/gemini-1.5-flash"

# Executa a escolha agora
NOME_MODELO_CHAT, NOME_MODELO_EXERCICIO = escolher_melhor_modelo()

# Configura os objetos com os nomes descobertos
model = genai.GenerativeModel(    
    model_name=NOME_MODELO_CHAT,
    system_instruction=instrucoes_do_sistema
)

model_exercicios = genai.GenerativeModel(
    model_name=NOME_MODELO_EXERCICIO, 
    generation_config={"response_mime_type": "application/json"}
)

# --- Início da Aplicação Flask ---
app = Flask(__name__)
# ... O resto do código continua igual ...
CORS(app) 

# --- Criação das Tabelas ---
try:
    Base.metadata.create_all(bind=engine)
    print("INFO: Tabelas do SQLAlchemy verificadas/criadas.")
except Exception as e:
    print(f"ERRO ao criar tabelas: {e}")

# --- Gerenciamento da Sessão SQLAlchemy ---
@app.before_request
def create_session():
    g.session = SessionLocal()

@app.teardown_request
def close_session(e=None):
    session = g.pop('session', None)
    if session is not None:
        session.close()

# --- NOVA ROTA: Health Check (Corrige o erro 404) ---
@app.route("/", methods=['GET'])
def home():
    return jsonify({
        "status": "online",
        "message": "API do Mentor de Estudos está rodando corretamente! 🚀",
        "endpoints": ["/chat", "/api/login", "/api/register", "/api/generate-exercise"]
    })

# --- Lógica do Chat (CORRIGIDA) ---
# Removemos a chamada global que travava o servidor.
# Definimos uma mensagem padrão rápida para não depender da IA no boot.
PRIMEIRA_MENSAGEM_PADRAO = "Olá! Eu sou o Mentor, seu tutor de estudos. Meu objetivo é te ajudar a entender de verdade a raiz das suas dificuldades. Para começarmos, me conte: em qual matéria ou tópico você está encontrando mais desafios no momento?"

@app.route("/api/initial-message", methods=['GET'])
def get_initial_message():
    # Retorna a mensagem fixa instantaneamente
    return jsonify({'message': PRIMEIRA_MENSAGEM_PADRAO})

@app.route("/chat", methods=['POST'])
def handle_chat():
    try:
        data = request.json
        user_message = data.get('message')
        
        # IMPORTANTE: Para manter o contexto, o Frontend idealmente deveria enviar
        # o histórico da conversa. Aqui estamos criando um chat "fresco" a cada request
        # ou tentando usar o histórico se o front enviar (history).
        history = data.get('history', []) 
        
        # Inicia uma sessão de chat isolada para este request
        chat_session = model.start_chat(history=history)
        
        response = chat_session.send_message(user_message)
        return jsonify({'response': response.text})
    
    except Exception as e:
        print(f"Erro no endpoint /chat: {e}")
        return jsonify({'error': str(e)}), 500


# --- ROTAS DE AUTENTICAÇÃO ---

@app.route("/api/register", methods=['POST'])
def handle_register():
    data = request.json
    nome = data.get('nome')
    email = data.get('email')
    senha = data.get('senha')

    try:
        repo = UserRepository(g.session)
        service = UserService(repo)
        new_user = service.create_user(nome, email, senha)
        
        return jsonify({'success': True, 'message': 'Usuário cadastrado!', 'user_id': new_user.id}), 201
    
    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 400
    except Exception as e:
        return jsonify({'success': False, 'error': f'Erro interno: {str(e)}'}), 500

@app.route("/api/login", methods=['POST'])
def handle_login():
    data = request.json
    email = data.get('email')
    senha = data.get('senha')

    if not email or not senha:
        return jsonify({'success': False, 'error': 'E-mail e senha são obrigatórios'}), 400

    try:
        repo = UserRepository(g.session)
        service = UserService(repo)
        user = service.authenticate_user(email, senha)
        
        return jsonify({
            'success': True, 
            'message': 'Login bem-sucedido!',
            'user': {'id': user.id, 'nome': user.nome}
        })

    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 401
    except Exception as e:
        return jsonify({'success': False, 'error': f'Erro interno: {str(e)}'}), 500
        
# --- GERAÇÃO DE EXERCÍCIOS ---
@app.route("/api/generate-exercise", methods=['POST'])
def generate_exercise():
    try:
        topic = request.json.get("topic", "Geral")

        prompt = f"""
        Você é um professor elaborando uma prova.
        Crie uma questão de MÚLTIPLA ESCOLHA sobre o tópico: "{topic}".
        
        Regras:
        1. Nível: Iniciante/Intermediário.
        2. Deve ter exatamente 5 alternativas.
        3. Indique qual o INDICE (0 a 4) da alternativa correta.
        4. Forneça uma explicação detalhada (feedback).
        
        Sua saída deve ser EXCLUSIVAMENTE um JSON neste formato:
        {{
            "enunciado": "Texto da pergunta...",
            "alternativas": ["A) ...", "B) ...", "C) ...", "D) ...", "E) ..."],
            "indice_correta": 2,
            "explicacao": "A resposta C é correta porque..."
        }}
        """

        response = model_exercicios.generate_content(prompt)
        
        texto_bruto = response.text
        match = re.search(r"\{[\s\S]*\}", texto_bruto)

        if match:
            return jsonify(json.loads(match.group(0)))
        else:
            return jsonify({"error": "Formato inválido da IA"}), 500

    except Exception as e:
        print("Erro em generate-exercise:", e)
        return jsonify({"error": str(e)}), 500

@app.route("/api/correct-exercise", methods=['POST'])
def correct_exercise():
    try:
        data = request.json
        user_id = int(data.get("user_id"))
        topic = data.get("topic")
        exercise_data = data.get("exercise")
        answer_text = data.get("answer_text")
        answer_index = data.get("answer_index")

        indice_gabarito = exercise_data.get("indice_correta")
        acertou = (answer_index == indice_gabarito)
        nota = 10 if acertou else 0
        feedback = exercise_data.get("explicacao", "Sem feedback disponível.")

        try:
            enunciado_str = json.dumps(exercise_data, ensure_ascii=False)
            novo_historico = HistoricoExercicio(
                id_usuario=user_id,
                topico=topic,
                enunciado_exercicio=enunciado_str,
                resposta_aluno=answer_text,
                feedback_ia=feedback,
                nota=nota,
                acertou=acertou
            )
            g.session.add(novo_historico)
            g.session.commit()
        except Exception as db_e:
            g.session.rollback()
            print(f"Erro ao salvar no banco: {db_e}")

        return jsonify({
            "correction": feedback,
            "nota": nota,
            "acertou": acertou,
            "saved": True
        })

    except Exception as e:
        print("Erro CRÍTICO:", e)
        return jsonify({"error": str(e)}), 500

@app.route("/api/user-stats/<int:user_id>", methods=['GET'])
def get_user_stats(user_id):
    try:
        historico = g.session.query(HistoricoExercicio).filter(
            HistoricoExercicio.id_usuario == user_id
        ).all()

        if not historico:
            return jsonify({"stats": [], "global_average": 0, "total_questions": 0})

        stats_by_topic = {}
        for h in historico:
            raw_topic = h.topico if h.topico else "Geral"
            topic_key = raw_topic.strip().title()

            if topic_key not in stats_by_topic:
                stats_by_topic[topic_key] = {"total": 0, "acertos": 0}
            
            stats_by_topic[topic_key]["total"] += 1
            if h.acertou:
                stats_by_topic[topic_key]["acertos"] += 1

        final_stats = []
        total_questions = 0
        total_correct = 0

        for topic, data in stats_by_topic.items():
            percent = round((data["acertos"] / data["total"]) * 100, 1)
            final_stats.append({
                "topic": topic,
                "total": data["total"],
                "acertos": data["acertos"],
                "percent": percent
            })
            total_questions += data["total"]
            total_correct += data["acertos"]

        global_avg = round((total_correct / total_questions) * 100, 1) if total_questions > 0 else 0
        final_stats.sort(key=lambda x: x['percent'])

        return jsonify({
            "stats": final_stats,
            "global_average": global_avg,
            "total_questions": total_questions
        })

    except Exception as e:
        print(f"Erro em /api/user-stats: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
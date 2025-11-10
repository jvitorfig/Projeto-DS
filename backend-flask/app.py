# app.py
import google.generativeai as genai
import os
from flask import Flask, request, jsonify, g
from flask_cors import CORS

# --- Importações da sua nova arquitetura ---
# (Assumindo que seus arquivos estão em pastas/módulos corretos)
# (Ajuste os imports se sua estrutura de pastas for diferente)
try:
    from db import SessionLocal, engine
    from models.models import Base
    from repositories.userRepository import UserRepository
    from service.userService import UserService
    from dtos.userDto import UserDto # Embora não seja usado diretamente aqui, é bom saber
except ImportError:
    print("ERRO DE IMPORTAÇÃO: Verifique sua estrutura de pastas e __init__.py")
    # Tente imports locais se estiver tudo na mesma pasta (menos ideal)
    from db import SessionLocal, engine
    from models.models import Base, Usuario
    from repositories.userRepository import UserRepository
    from service.userService import UserService
    from dtos.userDto import UserDto


# --- Configuração do Gemini (Sem Alterações) ---
# ... (seu código de configuração do Gemini vai aqui) ...
MINHA_CHAVE_SECRETA = "AIzaSyAoLsdHr2CTXZVevr39qSjnY9PIm_9X7Xk" 
genai.configure(api_key=MINHA_CHAVE_SECRETA)
instrucoes_do_sistema = """
# PERSONA
Você é um Tutor Socrático, um especialista em aprendizado e um mentor de estudos. Seu nome é "Mentor". Seu objetivo principal não é dar respostas, mas sim guiar o estudante a construir o próprio conhecimento, garantindo que a base seja sólida. Você é paciente, encorajador e extremamente curioso sobre o processo de pensamento do estudante.


# DIRETRIZ PRINCIPAL (A REGRA DE OURO)
NUNCA ensine o conteúdo ou dê a resposta diretamente. Sua primeira e mais importante missão é investigar a CAUSA RAIZ do problema através de perguntas direcionadas. Apenas após diagnosticar a lacuna no conhecimento, você pode começar a ensinar, focando especificamente no ponto fraco identificado.

#CARACTERÍSTICAS
Você não deve falar sobre assuntos não relacionados ao estudo, caso o aluno fale sobre um tema paralelo, você deverá dizer que não pode responder essa pergunta


# PROCESSO DE ATENDIMENTO (PASSO A PASSO)

**PASSO 1: ACOLHIMENTO E DIAGNÓSTICO INICIAL**
1. Apresente-se cordialmente como "Mentor" e explique que seu objetivo é entender a raiz da dificuldade.
2. A sua PRIMEIRA FALA na conversa deve ser sempre uma pergunta aberta para que o aluno descreva suas dificuldades gerais.
3. Exemplo de primeira fala: "Olá! Eu sou o Mentor, seu tutor de estudos. Meu objetivo é te ajudar a entender de verdade a raiz das suas dificuldades. Para começarmos, me conte: em qual matéria ou tópico você está encontrando mais desafios no momento?"

**PASSO 2: INVESTIGAÇÃO DA CAUSA RAIZ (FASE DE DIAGNÓSTICO)**
Após o aluno indicar o tópico, inicie a investigação aprofundada. Esta é a fase mais crítica. Não avance para o Passo 3 até ter uma hipótese clara da dificuldade. Use as seguintes técnicas:

* **Verificar Pré-requisitos:** Pergunte sobre conceitos fundamentais necessários para entender o tópico principal.
    * *Exemplo (se a dificuldade for em "Derivadas"):* "Claro, vamos chegar em derivadas. Mas antes, para eu entender melhor onde estamos, você poderia me explicar o que você entende por 'limite de uma função'?"
    * *Exemplo (se a dificuldade for em "Ponteiros em C"):* "Entendido. Ponteiros são um ótimo assunto. Antes de mergulharmos nisso, me diga com suas palavras: o que é uma variável e como você imagina que ela é guardada na memória do computador?"

* **Testar a Compreensão Conceitual:** Peça ao estudante para explicar o que ele *já sabe* sobre o tópico com as próprias palavras, mesmo que ache que está errado.
    * *Exemplo:* "Não se preocupe em acertar. Apenas me diga o que vem à sua mente quando você ouve o termo 'recursividade'."

* **Simplificar e Quebrar o Problema:** Se a pergunta for um exercício, peça para ele explicar qual foi a primeira parte que o deixou confuso.
    * *Exemplo:* "Ok, vamos olhar para este problema. Não precisa resolver tudo. Qual é o primeiro passo que você tentou dar? O que você pensou em fazer primeiro?"

**PASSO 3: CONFIRMAÇÃO DO DIAGNÓSTICO**
1. Após a investigação, formule uma hipótese sobre a dificuldade real.
2. Apresente essa hipótese ao estudante de forma colaborativa.
    * *Exemplo:* "Obrigado por explicar. Pelo que você me disse, parece que a principal dificuldade não é com as derivadas em si, mas em como simplificar as expressões algébricas antes de aplicar as regras. Faz sentido para você?"

**PASSO 4: ENSINO DIRECIONADO (FASE DE TRATAMENTO)**
1.  **Somente agora**, depois do diagnóstico confirmado, você pode ensinar.
2.  Concentre sua explicação **especificamente na causa raiz** que você identificou (ex: na simplificação algébrica, no conceito de memória, etc.).
3.  Use analogias e exemplos simples para explicar o conceito fundamental.
4.  Após a explicação, verifique a compreensão pedindo para o estudante explicar de volta ou resolver um problema bem mais simples.
    * *Exemplo:* "Isso ajudou a clarear as coisas? Com base nisso, como você resolveria este pequeno problema [problema simples]?"
""" # Suas instruções
model = genai.GenerativeModel(    
    model_name='gemini-pro-latest',
    system_instruction=instrucoes_do_sistema)


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
    try:
        user_message = request.json['message']
        response = chat.send_message(user_message)
        return jsonify({'response': response.text})
    
    except Exception as e:
        print(f"Erro no endpoint /chat: {e}")
        return jsonify({'error': str(e)}), 500


@app.route("/api/initial-message", methods=['GET'])
def get_initial_message():
    return jsonify({'message': PRIMEIRA_MENSAGEM_MENTOR})
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
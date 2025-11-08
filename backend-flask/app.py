import google.generativeai as genai
import os
from flask import Flask, request, jsonify
from flask_cors import CORS # Importar o CORS

# --- Configuração do Gemini (Exatamente como o seu) ---
# ... (seu código de configuração do Gemini vai aqui) ...
# ... (instrucoes_do_sistema, model = genai.GenerativeModel...) ...

try:
    # COLOQUE SUA CHAVE DE API REAL AQUI DENTRO DAS ASPAS
    MINHA_CHAVE_SECRETA = "Uma chave do gemini" 

    genai.configure(api_key=MINHA_CHAVE_SECRETA)
    print("INFO: Chave da API carregada diretamente do código (Modo de Teste).")

except Exception as e:
    print(f"Erro ao configurar a API (mesmo com a chave no código): {e}")
    exit()

instrucoes_do_sistema =  """
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
"""

model = genai.GenerativeModel(
    model_name='gemini-pro-latest',
    system_instruction=instrucoes_do_sistema
)
# --- Fim da Configuração do Gemini ---


# --- Início da Lógica do Servidor Web com Flask ---

# Cria a aplicação Flask
app = Flask(__name__)
# Habilita o CORS para permitir requisições do seu app React
CORS(app) 

# !! AVISO: Este chat global é compartilhado por TODOS os usuários. !!
# (Para um projeto real, você precisaria gerenciar o histórico por sessão)
try:
    chat = model.start_chat(history=[])
    inicial_response = chat.send_message("Ola")
    PRIMEIRA_MENSAGEM_MENTOR = inicial_response.text
except Exception as e:
    print(f"Erro ao inicializar o chat com o Gemini: {e}")
    PRIMEIRA_MENSAGEM_MENTOR = "Olá! Tive um problema para me conectar. Por favor, tente recarregar a página."


# Rota 1: O endpoint da API para conversar (SEU CÓDIGO ORIGINAL, PERFEITO)
@app.route("/chat", methods=['POST'])
def handle_chat():
    try:
        user_message = request.json['message']
        response = chat.send_message(user_message)
        return jsonify({'response': response.text})
    
    except Exception as e:
        print(f"Erro no endpoint /chat: {e}")
        return jsonify({'error': str(e)}), 500

# Rota 2: NOVA API para "logar" o usuário
@app.route("/api/login", methods=['POST'])
def handle_login():
    data = request.json
    email = data.get('email')
    senha = data.get('senha')
    
    # --- Lógica de Validação (Simulada) ---
    # Aqui você checaria no banco de dados
    if email == "aluno@email.com" and senha == "1234":
        # Em um app real, você retornaria um token (JWT)
        return jsonify({'success': True, 'message': 'Login bem-sucedido!'})
    else:
        return jsonify({'success': False, 'error': 'E-mail ou senha inválidos'}), 401

# Rota 3: NOVA API para buscar a primeira mensagem do bot
@app.route("/api/initial-message", methods=['GET'])
def get_initial_message():
    return jsonify({'message': PRIMEIRA_MENSAGEM_MENTOR})



if __name__ == '__main__':
    # 'debug=True' ajuda a ver erros e atualiza automaticamente
    app.run(debug=True, port=5000)
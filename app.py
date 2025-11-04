import google.generativeai as genai
import os
from flask import Flask, render_template, request, jsonify # Importações do Flask

##from dotenv import load_dotenv 

##oad_dotenv()

# --- Configuração do Gemini (Igual ao seu código) ---
# --- Configuração do Gemini (MODO DE TESTE) ---
# AVISO: Esta é uma solução de teste. Não compartilhe este arquivo.
try:
    # COLOQUE SUA CHAVE DE API REAL AQUI DENTRO DAS ASPAS
    MINHA_CHAVE_SECRETA = "Uma chave do gemini" 

    genai.configure(api_key=MINHA_CHAVE_SECRETA)
    print("INFO: Chave da API carregada diretamente do código (Modo de Teste).")

except Exception as e:
    print(f"Erro ao configurar a API (mesmo com a chave no código): {e}")
    exit()
# --- Fim do Modo de Teste ---

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
"""

model = genai.GenerativeModel(
    model_name='gemini-pro-latest',
    system_instruction=instrucoes_do_sistema
)

# --- Início da Lógica do Servidor Web com Flask ---

# Cria a aplicação Flask
app = Flask(__name__)

# NOTA IMPORTANTE SOBRE O HISTÓRICO:
# No seu script original, 'chat = model.start_chat(history=[])' criava UM chat.
# Em um app web, múltiplos usuários podem acessar. 
# Para este exemplo simples, vamos criar UM chat global.
# !! AVISO: Isso significa que todos os usuários estarão na MESMA conversa. !!
# (Para um projeto real, você precisaria gerenciar o histórico por sessão de usuário)

try:
    chat = model.start_chat(history=[])
    # Envia a mensagem inicial para "aquecer" o chat com a persona
    # Vamos capturar a primeira resposta do mentor
    inicial_response = chat.send_message("Ola")
    PRIMEIRA_MENSAGEM_MENTOR = inicial_response.text
except Exception as e:
    print(f"Erro ao inicializar o chat com o Gemini: {e}")
    PRIMEIRA_MENSAGEM_MENTOR = "Olá! Tive um problema para me conectar. Por favor, tente recarregar a página."

# Rota 1: Servir a página de chat
@app.route("/")
def home():
    # 'render_template' procura por arquivos na pasta 'templates'
    # Vamos passar a primeira mensagem do mentor para a página
    return render_template('chat.html', primeira_mensagem=PRIMEIRA_MENSAGEM_MENTOR)

# Rota 2: O endpoint da API para conversar
@app.route("/chat", methods=['POST'])
def handle_chat():
    try:
        user_message = request.json['message'] # Pega a mensagem do JSON enviado pelo front-end
        
        # Envia a mensagem para o Gemini (usando o chat global)
        response = chat.send_message(user_message)
        
        # Retorna a resposta do bot como JSON
        return jsonify({'response': response.text})
    
    except Exception as e:
        print(f"Erro no endpoint /chat: {e}")
        return jsonify({'error': str(e)}), 500

# Rota 3: Servir o CSS (para o navegador encontrar)
@app.route('/static/<path:filename>')
def serve_static(filename):
    return app.send_static_file(filename)


# --- Executar o aplicativo ---
if __name__ == '__main__':
    app.run(debug=True) # 'debug=True' ajuda a ver erros e atualiza automaticamente
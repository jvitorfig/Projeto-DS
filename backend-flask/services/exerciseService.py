import google.generativeai as genai
import re
import json
from repositories.exerciseRepository import ExerciseRepository

class ExerciseService:
    def __init__(self, repo: ExerciseRepository, api_key: str):
        self.repo = repo
        # Configura a IA com a chave fornecida
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel("gemini-pro-latest")

    def _extract_json(self, text: str):
        """
        Helper para limpar a resposta da IA.
        Muitas vezes a IA responde com ```json ... ```, e isso quebra o json.loads.
        Este método extrai apenas o conteúdo entre chaves {}.
        """
        match = re.search(r"\{[\s\S]*\}", text)
        if match:
            json_str = match.group(0)
            try:
                return json.loads(json_str)
            except json.JSONDecodeError:
                pass 
        
        # Se falhar, lançamos erro para o Controller tratar
        raise ValueError("A IA não retornou um JSON válido. Tente novamente.")

    def generate_question(self, topic: str):
        # 👇 SEU PROMPT DETALHADO DE GERAÇÃO
        prompt = f"""
        Você é um professor elaborando uma prova.
        Crie uma questão de MÚLTIPLA ESCOLHA sobre o tópico: "{topic}".
        
        Regras:
        1. Nível: Iniciante/Intermediário.
        2. Deve ter exatamente 5 alternativas (A, B, C, D, E).
        3. Apenas UMA alternativa correta.
        4. NÃO diga qual é a resposta correta na saída.
        
        Sua saída deve ser EXCLUSIVAMENTE um JSON válido neste formato:
        {{
            "enunciado": "O texto da pergunta aqui...",
            "alternativas": [
                "A) Opção 1", "B) Opção 2", "C) Opção 3", "D) Opção 4", "E) Opção 5"
            ]
        }}
        """
        
        response = self.model.generate_content(prompt)
        return self._extract_json(response.text)

    def correct_and_save(self, user_id: int, topic: str, exercise_data: dict, answer: str):
        # 👇 PROMPT DE CORREÇÃO (O professor corretor)
        prompt = f"""
        Você é um corretor de provas rigoroso mas didático.
        
        Questão Original:
        {str(exercise_data)}

        Alternativa escolhida pelo aluno:
        "{answer}"

        Tarefa:
        1. Identifique qual era a alternativa correta.
        2. Verifique se o aluno acertou.
        3. Explique o porquê de forma educativa.

        Sua saída deve ser EXCLUSIVAMENTE um JSON neste formato:
        {{
            "correcao_detalhada": "A resposta certa é X porque... (Explicação aqui)",
            "nota": 10,
            "acertou": true
        }}
        (Nota deve ser 10 para acerto ou 0 para erro. 'acertou' deve ser um booleano true/false).
        """
        
        response = self.model.generate_content(prompt)
        correction_data = self._extract_json(response.text)
        
        # O Service é quem manda Salvar no Banco (chamando o Repositório)
        # Convertemos o exercise_data para JSON string para caber no banco de texto
        self.repo.add_attempt(
            user_id=user_id, 
            topic=topic, 
            enunciado=json.dumps(exercise_data), 
            resposta=answer,
            feedback=correction_data['correcao_detalhada'], 
            nota=correction_data['nota'], 
            acertou=correction_data['acertou']
        )
        
        return correction_data

    def calculate_stats(self, user_id: int):
        # 1. Busca todo o histórico bruto no banco
        history = self.repo.get_history_by_user(user_id)
        
        if not history:
            return {"stats": [], "global_average": 0, "total_questions": 0}

        # 2. Processa os dados (Agrupa por Tópico)
        stats_by_topic = {}
        
        for h in history:
            # Normaliza nomes (Ex: "matematica" e "Matemática" viram "Matemática")
            topic = (h.topico or "Geral").strip().title()
            
            if topic not in stats_by_topic:
                stats_by_topic[topic] = {"total": 0, "acertos": 0}
            
            stats_by_topic[topic]["total"] += 1
            if h.acertou:
                stats_by_topic[topic]["acertos"] += 1
        
        # 3. Calcula as porcentagens finais
        final_stats = []
        total_questions = 0
        total_correct = 0
        
        for t, d in stats_by_topic.items():
            percent = round((d["acertos"]/d["total"])*100, 1)
            final_stats.append({
                "topic": t, 
                "percent": percent,
                "total": d["total"],
                "acertos": d["acertos"]
            })
            total_questions += d["total"]
            total_correct += d["acertos"]
            
        # Ordena do melhor para o pior desempenho
        final_stats.sort(key=lambda x: x['percent'], reverse=True)

        global_avg = round((total_correct / total_questions) * 100, 1) if total_questions > 0 else 0

        return {
            "stats": final_stats,
            "global_average": global_avg,
            "total_questions": total_questions
        }
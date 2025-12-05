from sqlalchemy.orm import Session
from sqlalchemy import func
from models.models import HistoricoExercicio

class ExerciseRepository:
    def __init__(self, session: Session):
        self.session = session

    def add_attempt(self, user_id: int, topic: str, enunciado: str, resposta: str, feedback: str, nota: int, acertou: bool):
        novo = HistoricoExercicio(
            id_usuario=user_id,
            topico=topic,
            enunciado_exercicio=enunciado,
            resposta_aluno=resposta,
            feedback_ia=feedback,
            nota=nota,
            acertou=acertou
        )
        self.session.add(novo)
        self.session.commit()
        return novo

    def get_history_by_user(self, user_id: int):
        return self.session.query(HistoricoExercicio).filter(
            HistoricoExercicio.id_usuario == user_id
        ).all()
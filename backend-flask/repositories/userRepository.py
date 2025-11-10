from sqlalchemy.orm import Session
from models.models import Usuario

class UserRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_all(self):
        return self.session.query(Usuario).all()

    def get_by_id(self, user_id: int):
        return self.session.query(Usuario).filter(Usuario.id == user_id).first()

    def add(self, nome: str, email: str, senha : str):
        user = Usuario(nome=nome, email=email, senha=senha)
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        return user

    def delete(self, user_id: int):
        user = self.get_by_id(user_id)
        if user:
            self.session.delete(user)
            self.session.commit()

    def get_by_email(self, email: str):
        return self.session.query(Usuario).filter(Usuario.email == email).first()

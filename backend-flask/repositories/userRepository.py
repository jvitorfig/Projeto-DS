from sqlalchemy.orm import Session
from ..models import User

class UserRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_all(self):
        return self.session.query(User).all()

    def get_by_id(self, user_id: int):
        return self.session.query(User).filter(User.id == user_id).first()

    def add(self, name: str, email: str):
        user = User(name=name, email=email)
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
        return self.session.query(User).filter(User.email == email).first()

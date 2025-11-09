from ..repositories import UserRepository
from ..dtos import userDto
class UserService:
    def __init__(self, repo: UserRepository):
        self.repo = repo

    def create_user(self, user: userDto):
        # 👇 Aqui você colocaria validações e regras de negócio
        if not user.name or not user.email:
            raise ValueError("Nome e e-mail são obrigatórios.")
        
        if self.repo.get_by_email(user.email):
            raise ValueError("E-mail já cadastrado.")
        
        return self.repo.add(user.name, user.email)

    def list_users(self):
        return self.repo.get_all()

    def find_user(self, user_id: int):
        user = self.repo.get_by_id(user_id)
        if not user:
            raise ValueError(f"Usuário {user_id} não encontrado.")
        return user

    def delete_user(self, user_id: int):
        user = self.repo.get_by_id(user_id)
        if not user:
            raise ValueError(f"Usuário {user_id} não encontrado.")
        self.repo.delete(user_id)
        return True
    
    
from repositories.userRepository import UserRepository
from dtos.userDto import UserDto

class UserService:
    def __init__(self, repo: UserRepository):
        self.repo = repo

    def create_user(self, name: str, email: str, senha_plain: str):
        # 👇 Validações
        if not name or not email or not senha_plain:
            raise ValueError("Nome, e-mail e senha são obrigatórios.")
        
        if self.repo.get_by_email(email):
            raise ValueError("E-mail já cadastrado.")
        
        # Armazena senha em texto plano (sem hash)
        return self.repo.add(name, email, senha_plain)

    def authenticate_user(self, email: str, senha_plain: str):
        user = self.repo.get_by_email(email)
        
        # Compara senha em texto plano
        if not user or user.senha != senha_plain:
            raise ValueError("E-mail ou senha inválidos.")
            
        return user # Retorna o usuário se for sucesso
    
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

from werkzeug.security import generate_password_hash, check_password_hash
from repositories.userRepository import UserRepository
from dtos.userDto import UserDto


class UserService:
    def __init__(self, repo: UserRepository):
        self.repo = repo

    def create_user(self, nome: str, email: str, senha_plain: str):
        if not nome or not email or not senha_plain:
            raise ValueError("Nome, e-mail e senha são obrigatórios.")

        if self.repo.get_by_email(email):
            raise ValueError("E-mail já cadastrado.")

        #Agora armazena **hash** da senha
        senha_hash = generate_password_hash(senha_plain)

        user = self.repo.add(nome, email, senha_hash)

        return user

    def authenticate_user(self, email: str, senha_plain: str):
        if not email or not senha_plain:
            raise ValueError("E-mail e senha são obrigatórios.")

        user = self.repo.get_by_email(email)

        #Compara usando o hash
        if not user or not check_password_hash(user.senha, senha_plain):
            raise ValueError("E-mail ou senha inválidos.")

        return user

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

import pytest
from service.userService import UserService

class DummyUser:
    def __init__(self, id, nome, email, senha):
        self.id = id
        self.nome = nome
        self.email = email
        self.senha = senha

def test_create_user_ok(fake_user_repo):
    fake_user_repo.get_by_email.return_value = None
    fake_user_repo.add.return_value = DummyUser(1, "Felipe", "felipe@email.com", "123")

    service = UserService(fake_user_repo)
    user = service.create_user("Felipe", "felipe@email.com", "123")

    assert user.id == 1
    fake_user_repo.add.assert_called_once_with("Felipe", "felipe@email.com", "123")

def test_create_user_missing_fields(fake_user_repo):
    service = UserService(fake_user_repo)
    with pytest.raises(ValueError):
        service.create_user("", "email", "123")
    with pytest.raises(ValueError):
        service.create_user("Nome", "", "123")
    with pytest.raises(ValueError):
        service.create_user("Nome", "email", "")

def test_create_user_existing_email(fake_user_repo):
    fake_user_repo.get_by_email.return_value = DummyUser(1, "Existente", "a@a.com", "123")
    service = UserService(fake_user_repo)
    with pytest.raises(ValueError, match="E-mail já cadastrado"):
        service.create_user("Novo", "a@a.com", "123")

def test_authenticate_user_ok(fake_user_repo):
    fake_user_repo.get_by_email.return_value = DummyUser(1, "User", "a@a.com", "123")
    service = UserService(fake_user_repo)
    user = service.authenticate_user("a@a.com", "123")
    assert user.email == "a@a.com"

def test_authenticate_user_wrong_password(fake_user_repo):
    fake_user_repo.get_by_email.return_value = DummyUser(1, "User", "a@a.com", "123")
    service = UserService(fake_user_repo)
    with pytest.raises(ValueError, match="E-mail ou senha inválidos"):
        service.authenticate_user("a@a.com", "errada")

def test_find_user_not_found(fake_user_repo):
    fake_user_repo.get_by_id.return_value = None
    service = UserService(fake_user_repo)
    with pytest.raises(ValueError, match="Usuário 99 não encontrado"):
        service.find_user(99)

def test_find_user_ok(fake_user_repo):
    user = DummyUser(1, "User", "user@email.com", "123")
    fake_user_repo.get_by_id.return_value = user

    service = UserService(fake_user_repo)

    result = service.find_user(1)

    assert result is user
    fake_user_repo.get_by_id.assert_called_once_with(1)


def test_list_users_returns_all(fake_user_repo):
    users = [
        DummyUser(1, "User1", "u1@email.com", "123"),
        DummyUser(2, "User2", "u2@email.com", "123"),
    ]
    fake_user_repo.get_all.return_value = users

    service = UserService(fake_user_repo)

    result = service.list_users()

    assert result == users
    fake_user_repo.get_all.assert_called_once()


def test_delete_user_ok(fake_user_repo):
    user = DummyUser(1, "User", "user@email.com", "123")
    fake_user_repo.get_by_id.return_value = user

    service = UserService(fake_user_repo)

    result = service.delete_user(1)

    assert result is True
    fake_user_repo.get_by_id.assert_called_once_with(1)
    fake_user_repo.delete.assert_called_once_with(1)


def test_delete_user_not_found(fake_user_repo):
    fake_user_repo.get_by_id.return_value = None
    service = UserService(fake_user_repo)

    with pytest.raises(ValueError, match="Usuário 99 não encontrado"):
        service.delete_user(99)


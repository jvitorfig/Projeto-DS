from unittest.mock import patch

def test_register_success(client):
    mock_user = type("User", (), {"id": 1})
    with patch("app.UserService.create_user", return_value=mock_user):
        resp = client.post("/api/register", json={
            "nome": "Leo",
            "email": "leo@email.com",
            "senha": "123"
        })
    assert resp.status_code in (200, 201)
    data = resp.get_json()
    assert data["success"] is True

def test_register_existing_email(client):
    with patch("app.UserService.create_user", side_effect=ValueError("E-mail já cadastrado.")):
        resp = client.post("/api/register", json={
            "nome": "Leo",
            "email": "existe@email.com",
            "senha": "123"
        })
    assert resp.status_code == 400
    assert resp.get_json()["success"] is False

def test_login_success(client):
    with patch("app.UserService.authenticate_user", return_value={"email": "a@a.com"}):
        resp = client.post("/api/login", json={
            "email": "a@a.com",
            "senha": "123"
        })
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["success"] is True

def test_login_invalid(client):
    with patch("app.UserService.authenticate_user", side_effect=ValueError("E-mail ou senha inválidos.")):
        resp = client.post("/api/login", json={
            "email": "a@a.com",
            "senha": "errada"
        })
    assert resp.status_code == 401
    data = resp.get_json()
    assert data["success"] is False

def test_login_missing_email_returns_400(client):
    resp = client.post("/api/login", json={
        "senha": "123"
    })
    assert resp.status_code == 400
    data = resp.get_json()
    assert data["success"] is False
    assert "E-mail e senha são obrigatórios" in data["error"]


def test_login_missing_password_returns_400(client):
    resp = client.post("/api/login", json={
        "email": "a@a.com"
    })
    assert resp.status_code == 400
    data = resp.get_json()
    assert data["success"] is False
    assert "E-mail e senha são obrigatórios" in data["error"]


def test_login_internal_error_returns_500(client):
    with patch("app.UserService.authenticate_user", side_effect=Exception("Erro inesperado")):
        resp = client.post("/api/login", json={
            "email": "a@a.com",
            "senha": "123"
        })
    assert resp.status_code == 500
    data = resp.get_json()
    assert data["success"] is False
    assert "Erro interno:" in data["error"]


def test_register_internal_error_returns_500(client):
    with patch("app.UserService.create_user", side_effect=Exception("Erro inesperado")):
        resp = client.post("/api/register", json={
            "nome": "Leo",
            "email": "leo@email.com",
            "senha": "123"
        })
    assert resp.status_code == 500
    data = resp.get_json()
    assert data["success"] is False
    assert "Erro interno:" in data["error"]

def test_chat_success(client):
    class FakeResponse:
        text = "Resposta do modelo"

    with patch("app.chat.send_message", return_value=FakeResponse()):
        resp = client.post("/chat", json={"message": "Olá"})
    
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["response"] == "Resposta do modelo"

def test_chat_error(client):
    with patch("app.chat.send_message", side_effect=Exception("Erro no modelo")):
        resp = client.post("/chat", json={"message": "Olá"})
    
    assert resp.status_code == 500
    data = resp.get_json()
    assert "Erro no modelo" in data["error"]

def test_initial_message(client):
    resp = client.get("/api/initial-message")
    assert resp.status_code == 200
    
    data = resp.get_json()
    assert "message" in data
    assert isinstance(data["message"], str)
def test_generate_exercise_success(client):
    class FakeResponse:
        text = "Exercício gerado"

    with patch("app.model_exercicios.generate_content", return_value=FakeResponse()):
        resp = client.post("/api/generate-exercise", json={"topic": "frações"})

    assert resp.status_code == 200
    data = resp.get_json()
    assert data["exercise"] == "Exercício gerado"

def test_generate_exercise_error(client):
    with patch("app.model_exercicios.generate_content", side_effect=Exception("Falha IA")):
        resp = client.post("/api/generate-exercise", json={"topic": "frações"})

    assert resp.status_code == 500
    data = resp.get_json()
    assert "Falha IA" in data["error"]

def test_correct_exercise_success(client):
    class FakeResponse:
        text = "Correção feita"

    with patch("app.model_exercicios.generate_content", return_value=FakeResponse()):
        resp = client.post("/api/correct-exercise", json={"question": "2+2", "answer": "4"})

    assert resp.status_code == 200
    data = resp.get_json()
    assert data["correction"] == "Correção feita"

def test_correct_exercise_error(client):
    with patch("app.model_exercicios.generate_content", side_effect=Exception("Erro de IA")):
        resp = client.post("/api/correct-exercise", json={"question": "2+2", "answer": "4"})

    assert resp.status_code == 500
    data = resp.get_json()
    assert "Erro de IA" in data["error"]


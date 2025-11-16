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

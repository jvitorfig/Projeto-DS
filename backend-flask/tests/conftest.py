import os, sys
import os.path as op
import os, sys
import os.path as op

sys.path.append(op.abspath(op.join(op.dirname(__file__), '..')))
os.environ.setdefault("APP_ENV", "TEST")

import pytest
from flask import Flask
from app import app as flask_app
from repositories.userRepository import UserRepository
from service.userService import UserService
from models.models import Usuario
sys.path.append(op.abspath(op.join(op.dirname(__file__), '..')))
os.environ.setdefault("APP_ENV", "TEST")

import pytest
from flask import Flask
from app import app as flask_app
from repositories.userRepository import UserRepository
from service.userService import UserService
from models.models import Usuario

@pytest.fixture
def app():
    flask_app.config.update({
        "TESTING": True
    })
    return flask_app

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def fake_user_repo(mocker):
    """Mocka o UserRepository para testar UserService isoladamente."""
    repo = mocker.Mock(spec=UserRepository)
    return repo

import pytest
from unittest.mock import patch
from flask import Flask
from werkzeug.wrappers import response

from src.routes.User_blueprint import User_blueprint

@patch('routes.User_blueprint.db.session')
def test_register_user(mock_db):
    app = Flask(__name__)
    app.config['TESTING'] = True
    client = app.test_client()

    with app.app_context():
        mock_db.commit.return_value = None
        response = client.post('/creat-user', json={
            'username': 'testuser',
            'senha': 'testpassword',
            'email': 'testuser@example.com',
            'is_admin': False
        })

    assert response.status_code == 201
    assert response.get_json() == {'message': 'User created successfully'}
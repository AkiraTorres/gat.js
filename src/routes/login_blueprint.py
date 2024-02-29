from flask import Blueprint, request, jsonify, make_response
from models.usuarios import (usuarios)
from datetime import timedelta
from flask_jwt_extended import create_access_token, create_refresh_token
from sqlalchemy.exc import SQLAlchemyError

login_blueprint = Blueprint('login', __name__)


@login_blueprint.route('/login', methods=['POST'])
def login_usuarios():

    data = request.get_json()

    username = data.get('username')
    senha = data.get('senha')

    user = usuarios.query.filter(usuarios.username == username).first()

    if user and user.check_password(senha):
        access_token = create_access_token(identity=username, expires_delta=timedelta(days=1))
        refresh_token = create_refresh_token(identity=username)

        return jsonify({
            'message': 'Login realizado com sucesso',
            'access_token': access_token,
            'refresh_token': refresh_token
        }), 200

    return jsonify({'message': 'Usuário ou senha incorretos'}), 401

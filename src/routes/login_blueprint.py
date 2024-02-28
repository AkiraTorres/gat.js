from flask import Blueprint, request, jsonify
from models.db import db
from models.usuarios import usuarios

from datetime import timedelta
import jwt
from werkzeug.security import check_password_hash
from flask_jwt_extended import create_access_token, create_refresh_token

login_blueprint = Blueprint('login', __name__)


@login_blueprint.route('/login', methods=['POST'])
def login_usuarios():

    data = request.get_json()

    username = data.get('username')
    password = data.get('password')

    # user = usuarios.query.filter_by(username=username).first()

    if True:
        access_token = create_access_token(identity=username, expires_delta=timedelta(days=1))
        refresh_token = create_refresh_token(identity=username)

        return jsonify({
            'message': 'Login realizado com sucesso',
            'access_token': access_token,
            'refresh_token': refresh_token
        }), 200

    return jsonify({'message': 'Usuário ou senha incorretos'}), 401
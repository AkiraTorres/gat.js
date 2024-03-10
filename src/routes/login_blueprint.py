from flask import Blueprint, request, jsonify, make_response
from flask_cors import cross_origin
from models.usuarios import (usuarios)
from datetime import timedelta
from flask_jwt_extended import create_access_token, create_refresh_token

login_blueprint = Blueprint('login', __name__)


@login_blueprint.route('/login', methods=['POST'])
@cross_origin()
def login_usuarios():
    data = request.get_json()

    email = data.get('email')
    senha = data.get('senha')
    
    if email == "" or senha == "":
        response = make_response({"message": "Por favor informe seu email e senha"}, 400)
        return response

    user = usuarios.query.filter(usuarios.email == email).first()

    if not (user and user.check_password(senha)):
        response = make_response({'message': 'Email ou senha incorretos'}, 401)
        # response.headers.add('Access-Control-Allow-Origin', '*')

        return response

    access_token = create_access_token(identity=email, expires_delta=timedelta(days=1))
    refresh_token = create_refresh_token(identity=email)

    response = make_response({
        'message': 'Login realizado com sucesso',
        'access_token': access_token,
        'refresh_token': refresh_token
    }, 200)

    return response


# Retorno com cookie de sessão
@login_blueprint.route('/login-cookie', methods=['POST'])
def login_usuarios_cookie():
    data = request.get_json()

    username = data.get('username')
    senha = data.get('senha')

    user = usuarios.query.filter(usuarios.username == username).first()

    if user and user.check_password(senha):
        session_id = create_access_token(identity=username, expires_delta=timedelta(days=1))

        response = make_response(jsonify({
            'message': 'Login realizado com sucesso'
        }), 200)
        response.set_cookie('session_id', session_id, httponly=True)

        return response

    return jsonify({'message': 'Usuário ou senha incorretos'}), 401


@login_blueprint.route('/logout', methods=['POST'])
def logout_usuarios():
    response = make_response(jsonify({'message': 'Logout realizado com sucesso'}), 200)
    response.set_cookie('session_id', '', expires=0)

    return response

from flask import Blueprint, request, jsonify
from models.usuarios import usuarios
from datetime import timedelta
import jwt
from werkzeug.security import check_password_hash
from flask_jwt_extended import create_access_token, create_refresh_token

login_blueprint = Blueprint('login', __name__)


@login_blueprint.route('/login', methods=['POST'])
def login():
    # data = request.get_json()
    # username = data.get('username')
    # password = data.get('password')
    #
    # user = usuarios.query.filter_by(username=username).first()
    #
    # if not user or not check_password_hash(user.password, password):
    #     return jsonify({'message': 'Invalid username or password'}), 401
    #
    # token = jwt.encode({'username': user.id}, 'SECRET_KEY', algorithm='HS256')  #Aqui é onde a mágica acontece, o token é gerado
    #
    # # return jsonify({'token': token.decode('UTF-8')})
    # return jsonify({'token': token}), 200



    data = request.get_json()

    id= data.get('id')
    username = data.get('username')
    password = data.get('password')

    user = usuarios.query.filter_by(id=id).first()

    if not user or not user.check_password(password):
        return jsonify({'message': 'Invalid username or password'}), 401

    access_token = create_access_token(
        identity=id,
        expires_delta=timedelta(minutes=30)

    )
    refresh_token = create_refresh_token(identity=id)

    return jsonify(
        {
            'access_token': access_token,
            'refresh_token': refresh_token,
            'message': 'Logged in as {}'.format(user.username),
        }
    ), 200


from flask import Blueprint, request, make_response, current_app
from models.db import db
from werkzeug.security import generate_password_hash
from models.usuarios import usuarios

User_blueprint = Blueprint('User', __name__)


@User_blueprint.route('/creat-user', methods=['POST'])
def register_user():
    try:
        data = request.get_json()

        new_user = usuarios(
            id=data.get('id'),
            username=data.get('username'),
            password=data.get('password'),
            email=data['email'],
            is_admin=data.get('is_admin', False),
        )

        new_user.gen_hash(data.get('password'))

        db.session.add(new_user)
        db.session.commit()

        return {'message': 'User created successfully'}, 201

    except Exception as e:
        return {'message': 'An error occurred while creating the user', 'error': str(e)}, 500


# 2. Listar todos os usuários
@User_blueprint.route('/list-user', methods=['GET'])
def list_user_details():
    try:
        user_details = usuarios.query.with_entities(usuarios.username, usuarios.id, usuarios.is_admin, usuarios.email, usuarios.is_active).all()

        user_details = [{
            'username': detail[0],
            'id': detail[1],
            'is_admin': detail[2],
            'email': detail[3],
            'is_active': detail[4]
        } for detail in user_details]

        return make_response({'user_details': user_details}, 200)

    except Exception as e:
        return {'message': 'An error occurred while listing user details', 'error': str(e)}, 500

    except Exception as e:
        return {'message': 'An error occurred while listing usernames', 'error': str(e)}, 500

from flask import Blueprint, request, make_response, current_app
from models.db import db
from werkzeug.security import generate_password_hash
from models.usuarios import usuarios
from flask_jwt_extended import jwt_required

User_blueprint = Blueprint('User', __name__)


@User_blueprint.route('/creat-user', methods=['POST'])
@jwt_required()
def register_user():
    try:
        data = request.get_json()

        new_user = usuarios(
            id=data.get('id'),
            username=data.get('username'),
            senha=data.get('senha'),
            email=data['email'],
            is_admin=data.get('is_admin', False),
        )

        new_user.gen_hash(data.get('senha'))

        db.session.add(new_user)
        db.session.commit()

        return {'message': 'User created successfully'}, 201

    except Exception as e:
        return {'message': 'An error occurred while creating the user', 'error': str(e)}, 500


# 2. Listar todos os usuários
@User_blueprint.route('/list-user', methods=['GET'])
@jwt_required()
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


# @User_blueprint.route('/update-user/<str:email>', methods=['PUT'])
# @jwt_required()
# def update_user(email):
#     try:
#         data = request.get_json()
#
#         user = usuarios.query.filter(usuarios.id == email).first()
#
#         user.username = data.get('username', user.username)
#         user.senha = generate_password_hash(data.get('senha', user.senha))
#         user.email = data.get('email', user.email)
#         user.is_admin = data.get('is_admin', user.is_admin)
#         user.is_active = data.get('is_active', user.is_active)
#
#         db.session.commit()
#
#         return {'message': 'User updated successfully'}, 200
#
#     except Exception as e:
#         return {'message': 'An error occurred while updating the user', 'error': str(e)}, 500
#

#
# @User_blueprint.route('/listar-emails', methods=['GET'])
# @jwt_required()
# def listar_emails():
#     try:
#         emails = usuarios.query.with_entities(usuarios.email).all()
#         emails = [email[0] for email in emails]
#         return make_response({'emails': emails}, 200)
#
#     except Exception as e:
#         return {'message': 'An error occurred while listing emails', 'error': str(e)}, 500


# @User_blueprint.route('/delete-user/<str:email>', methods=['DELETE'])
# @jwt_required()
# def delete_user(email):
#     try:
#         user = usuarios.query.filter(usuarios.email == email).first()
#         db.session.delete(user)
#         db.session.commit()
#
#         return {'message': 'User deleted successfully'}, 200
#
#     except Exception as e:
#         return {'message': 'An error occurred while deleting the user', 'error': str(e)}, 500
from flask import Blueprint, request, make_response
from src.models.db import db
from werkzeug.security import generate_password_hash
from src.models.User import User

User_blueprint = Blueprint('User', __name__)


@User_blueprint.route('/creat-user', methods=['POST'])
def register_user():
    try:
        data = request.get_json()

        hashed_password = generate_password_hash(data['password'], method='sha256')

        new_user = User(
            username=data['username'],
            password=hashed_password,
            email=data['email'],
            is_admin=data.get('is_admin', False)
        )

        db.session.add(new_user)
        db.session.commit()

        return {'message': 'User created successfully'}, 201

    except Exception as e:
        return {'message': 'An error occurred while creating the user', 'error': str(e)}, 500
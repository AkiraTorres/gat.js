from flask import Blueprint, request, make_response, jsonify
from models.db import db
from werkzeug.security import generate_password_hash
from models.usuarios import usuarios
from flask_jwt_extended import jwt_required, get_jwt_identity
from functools import wraps

User_blueprint = Blueprint("User", __name__)


def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        current_user = get_jwt_identity()
        user = usuarios.query.filter(usuarios.username == current_user).first()

        if not user.is_admin:
            return jsonify({"message": "Admins only!"}), 403

        return fn(*args, **kwargs)

    return wrapper


@User_blueprint.route("/user", methods=["GET", "POST"])
# @jwt_required()
def user():
    if request.method == "GET":
        try:
            user_details = usuarios.query.with_entities(
                usuarios.username,
                usuarios.is_admin,
                usuarios.email,
                usuarios.is_active,
                usuarios.photo,
            ).all()

            user_details = [
                {
                    "username": detail[0],
                    # 'id': detail[1],
                    "is_admin": detail[1],
                    "email": detail[2],
                    "is_active": detail[3],
                    "photo": detail[4],
                }
                for detail in user_details
            ]

            response = make_response({"user_details": user_details}, 200)

        except Exception as e:
            status = e.args[1] if e.args[1] else 500
            return make_response(
                {
                    "message": "An error occurred while updating the user",
                    "error": str(e.args[0]),
                },
                status,
            )

        return response

    elif request.method == "POST":
        try:
            data = request.get_json()

            new_user = usuarios(
                id=data.get("id"),
                username=data.get("username"),
                senha=data.get("senha"),
                photo=data.get("photo"),
                email=data["email"],
                is_admin=data.get("is_admin", False),
            )

            new_user.gen_hash(data.get("senha"))

            db.session.add(new_user)
            db.session.commit()

            return make_response({"message": "User created successfully"}, 201)

        except Exception as e:
            status = e.args[1] if e.args[1] else 500
            return make_response(
                {
                    "message": "An error occurred while updating the user",
                    "error": str(e.args[0]),
                },
                status,
            )


@User_blueprint.route("/user/<string:email>", methods=["GET", "PUT", "DELETE"])
@jwt_required()
def user_parameter(email=None):
    if request.method == "GET":
        try:
            user_details = usuarios.query.with_entities(
                usuarios.username,
                usuarios.is_admin,
                usuarios.email,
                usuarios.is_active,
                usuarios.photo,
            ).filter(usuarios.email == email)

            user_details = [
                {
                    "username": detail[0],
                    # 'id': detail[1],
                    "is_admin": detail[1],
                    "email": detail[2],
                    "is_active": detail[3],
                    "photo": detail[4],
                }
                for detail in user_details
            ]

            response = make_response(user_details[0], 200)

        except Exception as e:
            status = e.args[1] if e.args[1] else 500
            return make_response(
                {
                    "message": "An error occurred while updating the user",
                    "error": str(e.args[0]),
                },
                status,
            )

        return response

    elif request.method == "PUT":
        try:
            data = request.get_json()
            if data is None or data == {}:
                raise Exception("Missing data", 400)

            user = usuarios.query.filter(usuarios.email == email).first()
            if user is None:
                raise Exception("User does not exist", 404)

            user.username = data.get("username", user.username)
            user.senha = generate_password_hash(data.get("senha", user.senha))
            user.email = data.get("email", user.email)
            user.is_admin = data.get("is_admin", user.is_admin)
            user.is_active = data.get("is_active", user.is_active)

            db.session.commit()

            return make_response({"message": "User updated successfully"}, 200)

        except Exception as e:
            status = e.args[1] if e.args[1] else 500
            return make_response(
                {
                    "message": "An error occurred while updating the user",
                    "error": str(e.args[0]),
                },
                status,
            )

    elif request.method == "DELETE":
        try:
            if email is None:
                raise Exception("Missing data", 400)

            user = usuarios.query.filter(usuarios.email == email).first()
            if user is None:
                raise Exception("User does not exist", 404)

            db.session.delete(user)
            db.session.commit()

            return make_response({"message": "User deleted successfully"}, 200)

        except Exception as e:
            status = e.args[1] if e.args[1] else 500
            return make_response(
                {
                    "message": "An error occurred while updating the user",
                    "error": str(e.args[0]),
                },
                status,
            )


@User_blueprint.route("/listar-emails", methods=["GET"])
@jwt_required()
@admin_required
def listar_emails():
    try:
        emails = usuarios.query.with_entities(usuarios.email).all()
        emails = [email[0] for email in emails]
        return make_response({"emails": emails}, 200)

    except Exception as e:
        return {
            "message": "An error occurred while listing emails",
            "error": str(e),
        }, 500


@User_blueprint.route("/delete-user/<string:email>", methods=["DELETE"])
@jwt_required()
@admin_required
def delete_usuaurio(email):
    try:
        user = usuarios.query.filter(usuarios.email == email).first()
        db.session.delete(user)
        db.session.commit()

        return {"message": "User deleted successfully"}, 200

    except Exception as e:
        return {
            "message": "An error occurred while deleting the user",
            "error": str(e),
        }, 500

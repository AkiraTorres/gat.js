import os
from flask import Flask, request, make_response, jsonify
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager

from models.db import db

# imports das rotas
from routes.student_blueprint import student_blueprint
from routes.historic_blueprint import historic_blueprint
from routes.subject_blueprint import subject_blueprint
from routes.professor_blueprint import professor_blueprint
from routes.User_blueprint import User_blueprint
from routes.login_blueprint import login_blueprint


app = Flask(__name__)


env_config = os.getenv("APP_SETTINGS", "configs.config.DevelopmentConfig")
app.config.from_object(env_config)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

migrate = Migrate(app, db, command="migrate")

aluno = db.relationship('Aluno', backref='historico_aluno')
disciplina = db.relationship('Disciplina', backref='historico_disciplina')
historico = db.relationship('Historico', backref='aluno', cascade='all, delete-orphan')
User = db.relationship('User', backref='usuario', cascade='all, delete-orphan')
login = db.relationship('Login', backref='usuario', cascade='all, delete-orphan')

app.config['JWT_SECRET_KEY'] = 'super-secret'

JWTManager(app)

app.register_blueprint(student_blueprint)
app.register_blueprint(historic_blueprint)
app.register_blueprint(subject_blueprint)
app.register_blueprint(professor_blueprint)
app.register_blueprint(User_blueprint)
app.register_blueprint(login_blueprint)

if __name__ == "__main__":
    app.run()

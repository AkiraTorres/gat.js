import os
from flask import Flask, request, make_response, jsonify
from flask_migrate import Migrate

# from models.User import User, db
from models.db import db
from models.Aluno import Aluno
from models.Disciplina import Disciplina
from models.Historico import Historico


# imports das rotas
from routes.student_blueprint import student_blueprint
from routes.historic_blueprint import historic_blueprint

app = Flask(__name__)
env_config = os.getenv("APP_SETTINGS", "configs.config.DevelopmentConfig")
app.config.from_object(env_config)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)
migrate = Migrate(app, db, command="migrate")
aluno = db.relationship('Aluno', backref='historico_aluno')
disciplina = db.relationship('Disciplina', backref='historico_disciplina')
historico = db.relationship('Historico', backref='aluno', cascade='all, delete-orphan')


app.register_blueprint(student_blueprint)
app.register_blueprint(historic_blueprint)

if __name__ == "__main__":
    app.run()

import os
from flask import Flask, request, make_response, jsonify
from flask_migrate import Migrate

# from models.User import User, db
from models.db import db
from models.Aluno import Aluno
from models.Disciplina import Disciplina
from models.Historico import Historico

app = Flask(__name__)
env_config = os.getenv("APP_SETTINGS", "configs.config.DevelopmentConfig")
app.config.from_object(env_config)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)
migrate = Migrate(app, db, command="migrate")
aluno = db.relationship('Aluno', backref='historico_aluno')
disciplina = db.relationship('Disciplina', backref='historico_disciplina')
historico = db.relationship('Historico', backref='aluno', cascade='all, delete-orphan')


# criar aluno
@app.route('/alunos', methods=['POST'])
def create_aluno():
    dados_aluno = request.json

    novo_aluno = Aluno(dados_aluno)

    db.session.add(novo_aluno)
    db.session.commit()

    response = make_response({'message': 'Aluno criado com sucesso', 'id': novo_aluno.id})
    response.status_code = 201

    return response


# listar todos os alunos
@app.route("/alunos", methods=["GET"])
def list_alunos():
    alunos_list = Aluno.query.all()
    return jsonify([aluno.to_json() for aluno in alunos_list])


# encontrar aluno por id
@app.route("/alunos/<id>", methods=["GET"])
def get_aluno_by_id(user_id):
    aluno = Aluno.query.get(user_id)
    if not aluno:
        response = make_response({'message': 'Aluno não encontrado'})
        response.status_code = 404
    else:
        response = make_response(aluno.to_json())
        response.status_code = 200
    return response


# Atualizar aluno por id
@app.route('/alunos/<int:aluno_id>', methods=['PUT'])
def update_aluno(aluno_id):
    aluno = Aluno.query.get(aluno_id)

    if not aluno:
        response = make_response({'message': 'Aluno não encontrado'})
        response.status_code = 404
        return response

    dados_atualizados = request.json

    aluno.nome = dados_atualizados.get('nome', aluno.nome)
    aluno.cpf = dados_atualizados.get('cpf', aluno.cpf)
    aluno.arg_class = dados_atualizados.get('arg_class', aluno.arg_class)
    aluno.ano_entrada = dados_atualizados.get('ano_entrada', aluno.ano_entrada)

    db.session.commit()

    response = make_response({'message': 'Aluno atualizado com sucesso'})
    return response


# Deletar aluno por id
@app.route('/alunos/<int:aluno_id>', methods=['DELETE'])
def delete_aluno(aluno_id):
    aluno = Aluno.query.get(aluno_id)

    if not aluno:
        response = make_response({'message': 'Aluno não encontrado'})
        response.status_code = 404
        return response

    db.session.delete(aluno)
    db.session.commit()

    response = make_response({'message': 'Aluno excluído com sucesso'})
    return response


@app.route("/disciplinas", methods=["GET"])
def list_disciplinas():
    disciplinas_list = Disciplina.query.all()
    response = make_response([disc.to_json() for disc in disciplinas_list])
    return response


@app.route('/historico', methods=['GET'])
def encontrar_todos_historicos():
    historicos = Historico.query.all()
    response = make_response([historico.to_json() for historico in historicos])
    return response


if __name__ == "__main__":
    app.run()

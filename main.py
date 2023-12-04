import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from models import User, db

app = Flask(__name__)
env_config = os.getenv("APP_SETTINGS", "config.DevelopmentConfig")
app.config.from_object(env_config)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)
migrate = Migrate(app, db, command="migrate")


class Aluno(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(60), nullable=False)
    cpf = db.Column(db.String(14), nullable=False, unique=True)
    arg_class = db.Column(db.DECIMAL(5, 2), nullable=False)
    ano_entrada = db.Column(db.Integer, nullable=True)


class Disciplina(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    codigo = db.Column(db.String(8), nullable=False, unique=True)
    nome = db.Column(db.String(100), nullable=False)
    carga_horaria = db.Column(db.Integer, nullable=True)
    credito = db.Column(db.Integer, nullable=True)
    tipo = db.Column(db.Integer, nullable=False)


class Historico(db.Model):
    id_aluno = db.Column(db.Integer, db.ForeignKey('aluno.id'), primary_key=True)
    id_disciplina = db.Column(db.Integer, db.ForeignKey('disciplina.id'), primary_key=True)
    status = db.Column(db.Integer, nullable=False)
    ano = db.Column(db.Integer, nullable=False)
    semestre = db.Column(db.Integer, nullable=False)
    nota = db.Column(db.DECIMAL(5, 2), nullable=True)


aluno = db.relationship('Aluno', backref='historico_aluno')
disciplina = db.relationship('Disciplina', backref='historico_disciplina')
historico = db.relationship('Historico', backref='aluno', cascade='all, delete-orphan')


# Criar Aluno
@app.route('/alunos', methods=['POST'])
def criar_aluno():
    dados_aluno = request.json

    novo_aluno = Aluno(**dados_aluno)

    db.session.add(novo_aluno)
    db.session.commit()

    return jsonify({'message': 'Aluno criado com sucesso', 'id': novo_aluno.id}), 201


# Listar todos os alunos
@app.route('/alunos', methods=['GET'])
def encontrar_todos_alunos():
    alunos = Aluno.query.all()
    alunos_dict = [{'id': aluno.id, 'nome': aluno.nome, 'cpf': aluno.cpf, 'arg_class': aluno.arg_class, 'ano_entrada': aluno.ano_entrada} for aluno in alunos]
    return jsonify({'alunos': alunos_dict})


# Encotrar aluno por id
@app.route('/alunos/<int:aluno_id>', methods=['GET'])
def encontrar_aluno_por_id(aluno_id):
    aluno = Aluno.query.get(aluno_id)

    if aluno:
        aluno_dict = {'id': aluno.id, 'nome': aluno.nome, 'cpf': aluno.cpf, 'arg_class': aluno.arg_class, 'ano_entrada': aluno.ano_entrada}
        return jsonify(aluno_dict)
    else:
        return jsonify({'message': 'Aluno não encontrado'}), 404


# Atualizar aluno por id
@app.route('/alunos/<int:aluno_id>', methods=['PUT'])
def atualizar_aluno(aluno_id):
    aluno = Aluno.query.get(aluno_id)

    if not aluno:
        return jsonify({'message': 'Aluno não encontrado'}), 404

    dados_atualizados = request.json

    aluno.nome = dados_atualizados.get('nome', aluno.nome)
    aluno.cpf = dados_atualizados.get('cpf', aluno.cpf)
    aluno.arg_class = dados_atualizados.get('arg_class', aluno.arg_class)
    aluno.ano_entrada = dados_atualizados.get('ano_entrada', aluno.ano_entrada)

    db.session.commit()

    return jsonify({'message': 'Aluno atualizado com sucesso'})


# Deletar aluno por id
@app.route('/alunos/<int:aluno_id>', methods=['DELETE'])
def excluir_aluno(aluno_id):
    aluno = Aluno.query.get(aluno_id)

    if not aluno:
        return jsonify({'message': 'Aluno não encontrado'}), 404

    db.session.delete(aluno)
    db.session.commit()

    return jsonify({'message': 'Aluno excluído com sucesso'})

@app.route('/disciplinas', methods=['GET'])
def encontrar_todas_disciplinas():
    disciplinas = Disciplina.query.all()
    disciplinas_dict = [{'id': disciplina.id, 'codigo': disciplina.codigo, 'nome': disciplina.nome, 'carga_horaria': disciplina.carga_horaria, 'credito': disciplina.credito, 'tipo': disciplina.tipo} for disciplina in disciplinas]
    return jsonify({'disciplinas': disciplinas_dict})


@app.route('/historico', methods=['GET'])
def encontrar_todos_historicos():
    historicos = Historico.query.all()
    historicos_dict = [{'id_aluno': historico.id_aluno, 'id_disciplina': historico.id_disciplina, 'status': historico.status, 'ano': historico.ano, 'semestre': historico.semestre, 'nota': historico.nota} for historico in historicos]
    return jsonify({'historicos': historicos_dict})


if __name__ == "_main_":
    app.run()
from flask import Blueprint, jsonify, request, make_response
from models.db import db
from models.Aluno import Aluno

# cria o blueprint do aluno
student_blueprint = Blueprint('alunos', __name__)

# rota para criar um aluno 
@student_blueprint.route('/alunos', methods=['POST'])
def create_aluno():
    dados_aluno = request.json

    # novo_aluno = Aluno(nome, cpf, arg_class, ano_entrada)
    novo_aluno = Aluno(dados_aluno)
    db.session.add(novo_aluno)
    db.session.commit()

    response = make_response({'message': 'Aluno criado com sucesso', 'id': novo_aluno.id})
    response.status_code = 201

    return response


#rota para listar todos os alunos 
@student_blueprint.route("/alunos", methods=["GET"])
def list_alunos():
    alunos_list = Aluno.query.all()
    return jsonify([aluno.to_json() for aluno in alunos_list])


# encontrar aluno por id
@student_blueprint.route("/alunos/<cpf>", methods=["GET"])
def get_aluno_by_cpf(cpf):

    aluno = Aluno.query.get(cpf)

    if not aluno:
        response = make_response({'message': 'Aluno não encontrado'})
        response.status_code = 404
    else:
        response = make_response(aluno.to_json())
        response.status_code = 200
    return response


# Atualizar aluno por id
@student_blueprint.route('/alunos/<cpf>', methods=['PUT'])
def update_aluno(cpf):
    aluno = Aluno.query.get(cpf)

    if not aluno:
        response = make_response({'message': 'Aluno não encontrado'})
        response.status_code = 404
        return response

    dados_atualizados = request.json

    aluno.nome = dados_atualizados.get('nome', aluno.nome)
    # aluno.cpf = dados_atualizados.get('cpf', aluno.cpf)  # não atualizar o cpf, pois é a chave primária
    aluno.arg_class = dados_atualizados.get('arg_class', aluno.arg_class)
    aluno.ano_entrada = dados_atualizados.get('ano_entrada', aluno.ano_entrada)

    db.session.commit()

    response = make_response({'message': 'Aluno atualizado com sucesso'})
    return response


# Deletar aluno por id
@student_blueprint.route('/alunos/<cpf>', methods=['DELETE'])
def delete_aluno_por_cpf(cpf):
    aluno = Aluno.query.get(cpf)

    if not aluno:
        response = make_response({'message': 'Aluno não encontrado'})
        response.status_code = 404
        return response

    db.session.delete(aluno)
    db.session.commit()

    response = make_response({'message': 'Aluno excluído com sucesso'})
    return response
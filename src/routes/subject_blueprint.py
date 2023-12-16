from flask import Blueprint, request, make_response
from models.db import db
from models.Disciplina import Disciplina
from models.Historico import Historico

subject_blueprint = Blueprint('disciplinas', __name__)

@subject_blueprint.route("/disciplinas", methods=["GET"])
def list_disciplinas():
    disciplinas_list = Disciplina.query.all()
    return make_response([disc.to_json() for disc in disciplinas_list])


@subject_blueprint.route("/disciplinas/<int:id_disciplina>", methods=["PUT"])
def update_disciplina(id_disciplina):
    # retornar a disciplina do banco de dados 
    disciplina = Disciplina.query.get(id_disciplina)

    if not disciplina:
        response = make_response({'message': 'disciplina não encontrada'})
        response.status_code = 404
        return response

    
    # coletar as informações da requisição
    dados_atualizados = request.json
    disciplina.carga_horaria = dados_atualizados.get('carga_horaria', disciplina.carga_horaria)
    disciplina.codigo = dados_atualizados.get('codigo', disciplina.codigo)
    disciplina.credito = dados_atualizados.get('credito', disciplina.credito)
    disciplina.nome = dados_atualizados.get('nome', disciplina.nome)
    disciplina.tipo = dados_atualizados.get('tipo', disciplina.tipo)

    # subir pro banco de dados 
    db.session.commit()

    return make_response({'message': 'Disciplina atualizada com sucesso'})


@subject_blueprint.route("/disciplinas", methods=["POST"])
def create_subject():
    # coletar os dados
    dados_disciplina = request.json

    # criar um objeto disciplina
    nova_disciplina = Disciplina(dados_disciplina)

    # adicionar no banco de dados 
    db.session.add(nova_disciplina)
    db.session.commit()

    # retornar resposta 

    response = make_response({'message': 'Disciplina criada com sucesso', 'id': nova_disciplina.id})
    response.status_code = 201
    return response

@subject_blueprint.route("/disciplinas/<int:id_disciplina>", methods=["GET"])
def find_subject_by_id(id_disciplina):
    # procurar disciplina pelo no banco de dados 
    disciplina = Disciplina.query.get(id_disciplina)

    # verificar se a disciplina existe 

    if not disciplina:
        response = make_response({'message': 'disciplina não encontrada'})
        response.status_code = 404
        return response
    
    # se existe: mostar a disciplina 
    return  make_response(disciplina.to_json())








{
    "carga_horaria": 60,
    "codigo": "BXLX6924",
    "credito": 4,
    "id": 1,
    "nome": "Branding",
    "tipo": 1
},
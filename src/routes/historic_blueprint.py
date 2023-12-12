from flask import Blueprint, request, make_response
from models.db import db
from models.Historico import Historico

historic_blueprint = Blueprint('historico', __name__)


# listar historico escolar 
@historic_blueprint.route('/historico', methods=['GET'])
def find_():
    historicos = Historico.query.all()
    response = make_response([historico.to_json() for historico in historicos])
    return response

# listar historico escolar pelo id do aluno
@historic_blueprint.route('/historico/<int:user_id>', methods=['GET'])
def get_historic_by_id(user_id):
    historicos = Historico.query.get(user_id)
    if not historicos:
        response = make_response({'message': 'Historico não encontrado'})
        response.status_code = 404
    else:
        response = make_response([historico.to_json() for historico in historicos])
        response.status_code = 200
    return response

@historic_blueprint.route('/historico/<int:id_aluno>/<int:id_disciplina>', methods=['GET'])
def get_historic_by_ids(id_aluno, id_disciplina):
    historicos = Historico.query.filter_by(id_aluno=id_aluno, id_disciplina=id_disciplina).all()

    if not historicos:
        response = make_response({'message': 'Histórico não encontrado'})
        response.status_code = 404
    else:
        response = make_response([historico.to_json() for historico in historicos])
        response.status_code = 200

    return response
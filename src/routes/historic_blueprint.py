from flask import Blueprint, request, make_response
from models.db import db
from models.Historico import Historico
from models.Disciplina import Disciplina

historic_blueprint = Blueprint('historico', __name__)


# listar historico escolar 
@historic_blueprint.route('/historico', methods=['GET'])
def find_():
    historicos = Historico.query.all()
    response = make_response([historico.to_json() for historico in historicos])
    return response


# listar historico escolar pelo id do aluno
@historic_blueprint.route('/historico/<string:cpf_aluno>', methods=['GET'])
def get_historic_by_cpf(cpf_aluno):
    try:
        resultados = []

        historicos = Historico.query.filter(Historico.cpf_aluno == cpf_aluno).all()

        for historico in historicos:
            resultado = {
                "id": historico.id,
                "cpf_aluno": historico.cpf_aluno,
                "id_disciplina": historico.id_disciplina,
                "status": historico.status,
                "ano": historico.ano,
                "semestre": historico.semestre,
                "nota": historico.nota,
                "nome_disciplina": Disciplina.query.get(historico.id_disciplina).nome,
            }

            resultados.append(resultado)

        response_data = {"historicos": resultados}
        response = make_response(response_data)
        response.status_code = 200

    except Exception as e:
        response_data = {"error": str(e)}
        response = make_response(response_data)
        response.status_code = 500  # Internal Server Error

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
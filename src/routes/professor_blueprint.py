from flask import Blueprint, request, make_response
from models.Professor import Professor
from models.db import db
from models.Disciplina import Disciplina

professor_blueprint = Blueprint("professor", __name__)


@professor_blueprint.route("/professor", methods=['GET'])
def lista_professores() -> object:
    try:
        resultados = []

        professores = Professor.query.all()

        for professor in professores:
            resultado = {
                "matricula": professor.matricula,
                "nome": professor.nome,
                "cpf": professor.cpf
            }

            resultados.append(resultado)

        response_data = {"professores": resultados}
        response = make_response(response_data)
        response.status_code = 200

    except Exception as e:
        response_data = {"error": str(e)}
        response = make_response(response_data)
        response.status_code = 500

    return response


@professor_blueprint.route("/professor/<string:cpf>", methods=["GET"])
def buscar_professor_por_cpf(cpf) -> object:
    try:
        professor = Professor.query.filter(Professor.cpf == cpf).first()

        if professor:
            resultado = {
                "matricula": professor.matricula,
                "nome": professor.nome,
                "cpf": professor.cpf
            }
            response_data = {"professor": resultado}
            response_status = 200
        else:
            response_data = {"message": "Professor não encontrado"}
            response_status = 404

        response = make_response(response_data)
        response.status_code = response_status

    except Exception as e:
        response_data = {"error": str(e)}
        response = make_response(response_data)
        response.status_code = 500

    return response


@professor_blueprint.route("/professor/<string:cpf>", methods=["PUT"])
def atualizar_professor(cpf) -> object:
    try:
        professor = Professor.query.filter(Professor.cpf == cpf).first()

        if professor:
            dados_atualizados = request.json
            professor.nome = dados_atualizados.get("nome", professor.nome)

            db.session.commit()

            resultado = {
                "matricula": professor.matricula,
                "nome": professor.nome,
                "cpf": professor.cpf
            }
            response_data = {"professor_atualizado": resultado}
            response_status = 200
        else:
            response_data = {"message": "Professor não encontrado"}
            response_status = 404

        response = make_response(response_data)
        response.status_code = response_status

    except Exception as e:
        response_data = {"error": str(e)}
        response = make_response(response_data)
        response.status_code = 500

    return response


@professor_blueprint.route("/professor/<string:cpf>", methods=["DELETE"])
def excluir_professor(cpf) -> object:
    try:
        # Verificar se o professor existe
        professor = Professor.query.filter(Professor.cpf == cpf).first()

        if professor:
            # Excluir o professor do banco de dados
            db.session.delete(professor)
            db.session.commit()

            resultado = {
                "matricula": professor.matricula,
                "nome": professor.nome,
                "cpf": professor.cpf
            }
            response_data = {"professor_excluido": resultado}
            response_status = 200
        else:
            response_data = {"message": "Professor não encontrado"}
            response_status = 404

        response = make_response(response_data)
        response.status_code = response_status

    except Exception as e:
        response_data = {"error": str(e)}
        response = make_response(response_data)
        response.status_code = 500  # Internal Server Error

    return response


@professor_blueprint.route("/professor", methods=["POST"])
def criar_professor() -> object:
    try:
        dados_novo_professor = request.json

        novo_professor = Professor(
            cpf=dados_novo_professor["cpf"],
            matricula=dados_novo_professor.get("matricula"),
            nome=dados_novo_professor.get("nome")
        )

        db.session.add(novo_professor)
        db.session.commit()

        resultado = {
            "cpf": novo_professor.cpf,
            "matricula": novo_professor.matricula,
            "nome": novo_professor.nome
        }

        response_data = {"professor_criado": resultado}
        response_status = 201

        response = make_response(response_data)
        response.status_code = response_status

    except Exception as e:
        response_data = {"error": str(e)}
        response = make_response(response_data)
        response.status_code = 500

    return response


@professor_blueprint.route("/carga_horaria_total/<int:id_matricula>", methods=["GET"])
def carga_horaria_total_professor(id_matricula):
    try:
        carga_horaria_total = db.session.query(db.func.sum(Disciplina.carga_horaria)).\
            join(Professor, Disciplina.matricula_professor == Professor.matricula).\
            filter(Professor.matricula == id_matricula).scalar()

        carga_horaria_total = carga_horaria_total or 0  # Isso serve para evitar que o valor seja None

        response_data = {
            "id_matricula": id_matricula,
            "carga_horaria_total": carga_horaria_total
        }

        response = make_response(response_data)
        response.status_code = 200

    except Exception as e:
        response_data = {"error": str(e)}
        response = make_response(response_data)
        response.status_code = 500  # Internal Server Error

    return response
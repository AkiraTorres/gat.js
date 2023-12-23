from flask import Blueprint, request, make_response
from exceptions.Professor.ProfessorNotFoundException import ProfessorNotFoundException
from models.Professor import Professor
from models.db import db
from models.Disciplina import Disciplina
from models.Historico import Historico

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

# Taxa de desempenho por professor
@professor_blueprint.route("/taxa_professor/<string:cpf>", methods=["GET"])
def taxa_professor(cpf):
    try:
        professor = Professor.query.filter(Professor.cpf == cpf).first()

        if professor:
            subjects_by_professor = Disciplina.query.filter(Disciplina.matricula_professor == professor.matricula).all()

            resultado = {
                "matricula": professor.matricula,
                "nome": professor.nome,
                "cpf": professor.cpf,
                "disciplinas": [],
            }

            for subject in subjects_by_professor:
                count_total_approved = Historico.query.filter(
                    (Historico.id_disciplina == subject.id) &
                    ((Historico.status == 1) | (Historico.status == 2))
                ).count()

                count_total_reproved = Historico.query.filter(
                    (Historico.id_disciplina == subject.id) &
                    ((Historico.status == 3) | (Historico.status == 4))
                ).count()

                total_students = count_total_approved + count_total_reproved

                performance_rate = count_total_approved / total_students if total_students > 0 else 0

                subject_info = {
                    "id_disciplina": subject.id,
                    "nome_disciplina": subject.nome,
                    "Total de estudantes aprovados": count_total_approved,
                    "Total de estudantes reprovados": count_total_reproved,
                    "Taxa de desempenho": performance_rate,
                }

                resultado["disciplinas"].append(subject_info)

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

# Avaliação média do professor
@professor_blueprint.route("/avaliacao_professor/<string:cpf>", methods=["GET"])
def avaliacao_professor(cpf):
    try:
        professor = Professor.query.filter(Professor.cpf == cpf).first()

        if professor:
            subjects_by_professor = Disciplina.query.filter(Disciplina.matricula_professor == professor.matricula).all()


            total_rate = 0
            total_discipline = 0
            for subject in subjects_by_professor:
                count_total_approved = Historico.query.filter(
                    (Historico.id_disciplina == subject.id) &
                    ((Historico.status == 1) | (Historico.status == 2))
                ).count()

                count_total_reproved = Historico.query.filter(
                    (Historico.id_disciplina == subject.id) &
                    ((Historico.status == 3) | (Historico.status == 4))
                ).count()

                total_students = count_total_approved + count_total_reproved

                performance_rate = count_total_approved / total_students if total_students > 0 else 0

                total_rate += performance_rate
                total_discipline += 1


            avaliation_rate = total_rate/total_discipline
            avaliation = round(avaliation_rate * 10)
            resultado = {
                "matricula": professor.matricula,
                "nome": professor.nome,
                "cpf": professor.cpf,
                "avaliação": avaliation
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


@professor_blueprint.route("/professor/media/disciplinas", methods=["GET"])
def get_average_subjects_by_professor():
    try:
        result = 0
        professors = db.session.query(
            Professor.matricula,
            Professor.cpf,
            Professor.nome,
            db.func.count().label('total_disciplinas')
        ).join(
            Disciplina, Professor.matricula == Disciplina.matricula_professor,
        ).group_by(Professor.matricula).all()

        for professor in professors:
            result += professor.total_disciplinas

        result = result / len(professors)

        response_data = {"average_subjects_by_professor": eval(f"{result:.2f}")}
        response = make_response(response_data)

    except Exception as e:
        response = make_response({"error": e})
        response.status_code = 500

    return response

@professor_blueprint.route("/professor/disciplinas/<identifier>", methods=["GET"])
def get_professor_subjects(identifier):
    try:
        professor = Professor.query.filter(
            (Professor.matricula == identifier) |
            (Professor.cpf == identifier)
        )

        if professor.count() < 1:
            raise ProfessorNotFoundException(identifier)
        
        professor = professor[0]
        professor_subjects = Disciplina.query.filter(Disciplina.matricula_professor == professor.matricula).all()
        professor_subjects = [subject.to_json() for subject in professor_subjects]

        response_data = {
            "professor_registration": professor.matricula,
            "professor_name": professor.nome,
            "subjects": professor_subjects
        }
        response = make_response(response_data)

    except ProfessorNotFoundException as e:
        response = make_response({"error": str(e)}) 
        response.status_code = 404

    except Exception as e:
        response = make_response({"error": e})
        response.status_code = 500

    return response

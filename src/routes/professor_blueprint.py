from flask import Blueprint, request, make_response
from exceptions.Professor.ProfessorNotFoundException import ProfessorNotFoundException
from exceptions.Professor.ProfessorAlreadyExistsException import ProfessorAlreadyExistsException
from models.Professor import Professor
from models.db import db
from models.Disciplina import Disciplina
from models.Historico import Historico

professor_blueprint = Blueprint("professor", __name__)

@professor_blueprint.route("/professors", methods=['GET'])
def list_professors() -> object:
    try:
        results = []

        professors = Professor.query.all()

        for professor in professors:
            result = {
                "registration": professor.matricula,
                "name": professor.nome,
                "cpf": professor.cpf
            }

            results.append(result)

        response = make_response({"professors": results})

    except Exception as e:
        response = make_response({"error": str(e)})
        response.status_code = 500

    return response


@professor_blueprint.route("/professors/<string:cpf>", methods=["GET"])
def find_professor_by_cpf(cpf: str) -> object:
    try:
        professor = Professor.query.filter(Professor.cpf == cpf).first()

        if not professor:
            raise ProfessorNotFoundException(cpf)
            
        result = {
            "registration": professor.matricula,
            "name": professor.nome,
            "cpf": professor.cpf
        }
        response_data = {"professor": result}

        response = make_response(response_data)

    except ProfessorNotFoundException as e:
        response = make_response({"error": str(e)})
        response.status_code = 404

    except Exception as e:
        response = make_response({"error": str(e)})
        response.status_code = 500

    return response


@professor_blueprint.route("/professors/<string:cpf>", methods=["PUT"])
def update_professor_by_cpf(cpf: str) -> object:
    try:
        professor = Professor.query.filter(Professor.cpf == cpf).first()

        if not professor:
            raise ProfessorNotFoundException(cpf)

        updated_data = request.json
        professor.nome = updated_data.get("name", professor.nome)

        db.session.commit()

        result = {
            "registration": professor.matricula,
            "name": professor.nome,
            "cpf": professor.cpf
        }
        response_data = {"updated_professor": result}

        response = make_response(response_data)

    except ProfessorNotFoundException as e:
        response = make_response({"error": str(e)})
        response.status_code = 404

    except Exception as e:
        response = make_response({"error": str(e)})
        response.status_code = 500

    return response


@professor_blueprint.route("/professors/<string:cpf>", methods=["DELETE"])
def delete_professor_by_cpf(cpf: str) -> object:
    try:
        professor = Professor.query.filter(Professor.cpf == cpf).first()

        if not professor:
            raise ProfessorNotFoundException(cpf)

        # Delete the professor from the database
        db.session.delete(professor)
        db.session.commit()

        result = {
            "registration": professor.matricula,
            "name": professor.nome,
            "cpf": professor.cpf
        }
        response_data = {"deleted_professor": result}

        response = make_response(response_data)
        
    except ProfessorNotFoundException as e:
        response = make_response({"error": str(e)})
        response.status_code = 404

    except Exception as e:
        response = make_response({"error": str(e)})
        response.status_code = 500

    return response


@professor_blueprint.route("/professors", methods=["POST"])
def create_professor() -> object:
    try:
        new_professor_data = request.json

        if Professor.query.filter(Professor.cpf == new_professor_data["cpf"]).first():
            raise ProfessorAlreadyExistsException(new_professor_data["cpf"])

        new_professor = Professor(new_professor_data)

        db.session.add(new_professor)
        db.session.commit()

        result = {
            "registration": new_professor.matricula,
            "cpf": new_professor.cpf,
            "name": new_professor.nome
        }

        response = make_response({"created_professor": result})
        response.status_code = 201

    except ProfessorAlreadyExistsException as e:
        response = make_response({"error": str(e)})
        response.status_code = 403

    except Exception as e:
        response = make_response({"error": str(e)})
        response.status_code = 500

    return response


@professor_blueprint.route("/professors/<int:id_matricula>/total_workload", methods=["GET"])
def total_workload_professor(id_matricula: int) -> object:
    try:
        total_workload = db.session.query(db.func.sum(Disciplina.carga_horaria)).\
            join(Professor, Disciplina.matricula_professor == Professor.matricula).\
            filter(Professor.matricula == id_matricula).scalar()

        total_workload = total_workload or 0  # This is to prevent the value from being None

        response_data = {
            "professor_id": id_matricula,
            "total_workload": total_workload
        }

        response = make_response(response_data)

    except Exception as e:
        response = make_response({"error": str(e)})
        response.status_code = 500  # Internal Server Error

    return response


# Taxa de desempenho por professor
@professor_blueprint.route("/professors/<string:cpf>/performance_rate", methods=["GET"])
def professor_performance_rate(cpf: str) -> object:
    try:
        professor = Professor.query.filter(Professor.cpf == cpf).first()

        if not professor:
            raise ProfessorNotFoundException(cpf)

        subjects_by_professor = Disciplina.query.filter(Disciplina.matricula_professor == professor.matricula).all()

        result = {
            "registration": professor.matricula,
            "name": professor.nome,
            "cpf": professor.cpf,
            "subjects": [],
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
                "discipline_id": subject.id,
                "discipline_name": subject.nome,
                "Total students approved": count_total_approved,
                "Total students reproved": count_total_reproved,
                "Performance rate": performance_rate,
            }

            result["subjects"].append(subject_info)

        response = make_response({"professor": result})

    except ProfessorNotFoundException as e:
        response = make_response({"error": str(e)})
        response.status_code = 404

    except Exception as e:
        response = make_response({"error": str(e)})
        response.status_code = 500

    return response


# Avaliação média do professor
@professor_blueprint.route("/professors/<string:cpf>/evaluation", methods=["GET"])
def professor_evaluation(cpf: str) -> object:
    try:
        professor = Professor.query.filter(Professor.cpf == cpf).first()

        if not professor:
            raise ProfessorNotFoundException(cpf)

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

        evaluation_rate = total_rate / total_discipline
        evaluation = round(evaluation_rate * 10)
        result = {
            "registration": professor.matricula,
            "name": professor.nome,
            "cpf": professor.cpf,
            "evaluation": evaluation
        }

        response = make_response({"professor": result})

    except ProfessorNotFoundException as e:
        response = make_response({"error": str(e)})
        response.status_code = 404

    except Exception as e:
        response = make_response({"error": str(e)})
        response.status_code = 500

    return response


@professor_blueprint.route("/professors/average_subjects", methods=["GET"])
def get_average_subjects_by_professor() -> object:
    try:
        total_subjects = 0
        professors = db.session.query(
            Professor.matricula,
            Professor.cpf,
            Professor.nome,
            db.func.count().label('total_subjects')
        ).join(
            Disciplina, Professor.matricula == Disciplina.matricula_professor,
        ).group_by(Professor.matricula).all()

        for professor in professors:
            total_subjects += professor.total_subjects

        average_subjects = total_subjects / len(professors) if len(professors) > 0 else 0

        response_data = {"average_subjects_by_professor": round(average_subjects, 2)}
        response = make_response(response_data)

    except Exception as e:
        response = make_response({"error": str(e)})
        response.status_code = 500

    return response


@professor_blueprint.route("/professors/<string:cpf>/subjects", methods=["GET"])
def get_professor_subjects(cpf: str) -> object:
    try:
        professor = Professor.query.filter(Professor.cpf == cpf).first()

        if not professor:
            raise ProfessorNotFoundException(cpf)

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
        response = make_response({"error": str(e)})
        response.status_code = 500

    return response

from flask import Blueprint, request, make_response
from exceptions.Historic.HistoricNotFoundException import HistoricNotFoundException
from exceptions.Student.StudentNotFoundException import StudentNotFoundException
from models.db import db
from models.Historico import Historico
from models.Disciplina import Disciplina
from models.Aluno import Aluno
from exceptions.Subject.SubjectNotFoundException import SubjectNotFoundException
from flask_jwt_extended import jwt_required


historic_blueprint = Blueprint('historic', __name__)


@historic_blueprint.route('/historic', methods=['GET'])
@jwt_required()
def list_all_historic() -> object:
    try:
        # historicos = Historico.query.all()
        historicos = db.session.query(Historico).all()
        response = make_response([historico.to_json() for historico in historicos])

    except Exception as e:
        response = make_response({"error": str(e)})
        response.status_code = 500

    return response


@historic_blueprint.route('/historic/get_historic_by_cpf/<string:student_cpf>', methods=['GET'])
@jwt_required()
def get_history_by_cpf(student_cpf: str) -> object:
    try:
        results = []

        histories = Historico.query.filter(Historico.cpf_aluno == student_cpf).all()

        for history in histories:
            result = {
                "id": history.id,
                "student_cpf": history.cpf_aluno,
                "discipline_id": history.id_disciplina,
                "status": history.status,
                "year": history.ano,
                "semester": history.semestre,
                "grade": history.nota,
                "discipline_name": Disciplina.query.get(history.id_disciplina).nome,
            }

            results.append(result)

        response = make_response({"histories": results})

    except Exception as e:
        response = make_response({"error": str(e)})
        response.status_code = 500

    return response


@historic_blueprint.route('/historic/get_historic_by_ids/<string:student_cpf>/<int:subjects_id>', methods=['GET'])
@jwt_required()
def get_historic_by_ids(student_cpf: str, subjects_id: int) -> object:
    try:
        if not Aluno.query.get(student_cpf):
            raise StudentNotFoundException(student_cpf)
        if not Disciplina.query.get(subjects_id):
            raise SubjectNotFoundException(subjects_id)

        historicos = Historico.query.filter(Historico.cpf_aluno==student_cpf, Historico.id_disciplina==subjects_id).all()

        if not historicos:
            raise HistoricNotFoundException()

        response = make_response([historico.to_json() for historico in historicos])

    except (StudentNotFoundException, SubjectNotFoundException, HistoricNotFoundException) as e:
        response = make_response({"error": str(e)})
        response.status_code = 404

    except Exception as e:
        response = make_response({"error": str(e)})
        response.status_code = 500

    return response


@historic_blueprint.route("/historic/enrolled_students", methods=["GET"])
@jwt_required()
def enrolled_students() -> object:
    try:
        enrolled_students = Aluno.query.join(
            Historico, Aluno.cpf == Historico.cpf_aluno
        ).filter(
            Historico.status == 1
        ).all()

        results = []
        for student in enrolled_students:
            result = {
                "cpf": student.cpf,
                "nome": student.nome,
                "arg_class": student.arg_class,
                "ano_entrada": student.ano_entrada,
            }
            results.append(result)

        response = make_response({"results": results})

    except Exception as e:
        response = make_response({"error": str(e)})
        response.status_code = 500  # Internal Server Error

    return response


@historic_blueprint.route("/historic/get_retention_rate/<int:year>", methods=["GET"])
@jwt_required()
def get_retention_rate(year: int):
    try:
        retained_query = Historico.query.filter(
            Historico.ano == year,
            (Historico.status == 3) | (Historico.status == 4)
        ).count()

        total_students_query = Historico.query.filter(
            Historico.ano == year
        ).count()

        if total_students_query > 0:
            retention_rate = (retained_query / total_students_query) * 100
        else:
            retention_rate = 0

        response_data = {
            "year": year,
            "total_students": total_students_query,
            "retained": retained_query,
            "retention_rate": retention_rate
        }

        response = make_response(response_data)

    except Exception as e:
        response = make_response({"error": str(e)})
        response.status_code = 500  # Internal Server Error

    return response


@historic_blueprint.route("/historic/get_global_approval_rate", methods=["GET"])
@jwt_required()
def get_global_approval_rate() -> object:
    try:
        approved_query = Historico.query.filter(
            (Historico.status == 1) | (Historico.status == 2)
        ).count()

        total_students_query = Historico.query.count()

        if total_students_query > 0:
            global_approval_rate = (approved_query / total_students_query) * 100
        else:
            global_approval_rate = 0

        response_data = {
            "total_students": total_students_query,
            "approved": approved_query,
            "global_approval_rate": global_approval_rate
        }

        response = make_response(response_data)

    except Exception as e:
        response = make_response({"error": str(e)})
        response.status_code = 500

    return response


@historic_blueprint.route("/historic/get_success_rate_year/<int:year>", methods=["GET"])
@jwt_required()
def get_success_rate_year(year: int) -> object:
    try:
        success_rate = 0

        approved_query = Historico.query.filter(
            Historico.ano == year,
            (Historico.status == 1) | (Historico.status == 2)
        ).count()

        total_students_query = Historico.query.filter(
            Historico.ano == year
        ).count()

        if total_students_query > 0:
            success_rate = (approved_query / total_students_query) * 100
        else:
            success_rate = 0

        response_data = {
            "year": year,
            "total_students": total_students_query,
            "approved": approved_query,
            "success_rate": success_rate
        }

        response = make_response(response_data)

    except Exception as e:
        response = make_response({"error": str(e)})
        response.status_code = 500  # Internal Server Error

    return response


@historic_blueprint.route("/historic/get_abandonment_by_subject/<int:subject_id>", methods=["GET"])
@jwt_required()
def get_abandonment_by_subject(subject_id: int) -> object:
    try:
        subject = Disciplina.query.filter(Disciplina.id == subject_id)

        if not subject:
            raise SubjectNotFoundException(subject_id)
        
        total_abandonment = Historico.query.filter(
            Historico.id_disciplina == subject_id,
            Historico.status == 4
        ).count()

        total = Historico.query.filter(
            Historico.id_disciplina == subject_id
        ).count()

        abandonment_rate = (total_abandonment / total) * 100

        response_data = {
            "total_abandonment": total_abandonment,
            "total": total,
            "abandonment_rate": float(f"{abandonment_rate:.2f}")
        }

        response = make_response(response_data)

    except SubjectNotFoundException as e:
        response = make_response({"error": str(e)})
        response.status_code = 404  # Internal Server Error


    except Exception as e:
        response = make_response({"error": str(e)})
        response.status_code = 500  # Internal Server Error

    return response


@historic_blueprint.route('/historic/subjects_by_student', methods=["GET"])
@jwt_required()
def subjects_by_student() -> object:
    try:
        result = 0

        total_subjects = Disciplina.query.count()

        students = db.session.query(
            Aluno.cpf,
            Aluno.nome,
            Aluno.ano_entrada,
            db.func.count().label('total_cursadas')
        ).join(
            Historico, Aluno.cpf == Historico.cpf_aluno
        ).filter(
            (Historico.status == 1) |
            (Historico.status == 2) | 
            (Historico.status == 7)
        ).group_by(Aluno.cpf).all()

        for student in students:
            result += student.total_cursadas

        result = (result / len(students))
        response = make_response({
            "average": eval(f"{result:.2f}"),
            "average_percentage": f"{result/total_subjects*100:.2f}%"
        })

    except Exception as e:
        response = make_response({"error": str(e)})
        response.status_code = 500  # Internal Server Error

    return response


@historic_blueprint.route('/historic', methods=['POST'])
@jwt_required()
def create_historic() -> object:
    try:
        new_historic = Historico(request.json)

        db.session.add(new_historic)
        db.session.commit()

        response = make_response({"created_historic": new_historic.to_json()})
        response.status_code = 201

    except Exception as e:
        response = make_response({"error": str(e)})
        response.status_code = 500  # Internal Server Error
    
    return response


@historic_blueprint.route('/historic/<int:id>', methods=['PUT'])
@jwt_required()
def update_historic(id) -> object:
    try:
        historic = Historico.query.get(id)
        if not historic:
            raise HistoricNotFoundException(id)

        historic.cpf_aluno = request.json.get("cpf_aluno")
        historic.id_disciplina = request.json.get("id_disciplina")
        historic.status = request.json.get("status")
        historic.ano = request.json.get("ano")
        historic.semestre = request.json.get("semestre")
        historic.nota = request.json.get("nota")

        db.session.commit()

        response = make_response({"updated_historic": historic.to_json()})
        
    except HistoricNotFoundException as e:
        response = make_response({"error": str(e)})
        response.status_code = 404  # Not Found

    except Exception as e:
        response = make_response({"error": str(e)})
        response.status_code = 500

    return response


@historic_blueprint.route('/historic/<int:id>', methods=["DELETE"])
@jwt_required()
def delete_historic(id) -> object:
    try:
        historic = Historico.query.get(id)

        if not historic:
            raise HistoricNotFoundException(id)

        db.session.delete(historic)
        db.session.commit()

        response = make_response({"deleted_historic": historic.to_json()})
        
    except HistoricNotFoundException as e:
        response = make_response({"error": str(e)})
        response.status_code = 404  # Not Found

    except Exception as e:
        response = make_response({"error": str(e)})
        response.status_code = 500  # Internal Server Error

    return response

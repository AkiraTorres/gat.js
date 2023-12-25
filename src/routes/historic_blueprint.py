from flask import Blueprint, request, make_response
from exceptions.Historic.HistoricNotFoundException import HistoricNotFoundException
from exceptions.Student.StudentNotFoundException import StudentNotFoundException
from models.db import db
from models.Historico import Historico
from models.Disciplina import Disciplina
from models.Aluno import Aluno
from exceptions.Subject.SubjectNotFoundException import SubjectNotFoundException

historic_blueprint = Blueprint('historico', __name__)


@historic_blueprint.route('/historic', methods=['GET'])
def list_all_historic():
    try:
        historicos = Historico.query.all()
        response = make_response([historico.to_json() for historico in historicos])

    except Exception as e:
        response = make_response({"error": str(e)})
        response.status_code = 500

    return response


@historic_blueprint.route('/historic/get_historic_by_cpf/<string:student_cpf>', methods=['GET'])
def get_history_by_cpf(student_cpf):
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



@historic_blueprint.route('/historic/get_historic_by_ids/<int:id_aluno>/<int:id_disciplina>', methods=['GET'])
def get_historic_by_ids(id_aluno, id_disciplina):
    try:
        if not Aluno.query.get(id_aluno):
            raise StudentNotFoundException(id_aluno)
        if not Disciplina.query.get(id_disciplina):
            raise SubjectNotFoundException(id_disciplina)

        historicos = Historico.query.filter_by(id_aluno=id_aluno, id_disciplina=id_disciplina).all()

        if not historicos:
            raise HistoricNotFoundException()

        response = make_response([historico.to_json() for historico in historicos])

    except StudentNotFoundException as e:
        response = make_response({"error": str(e)})
        response.status_code = 404

    except SubjectNotFoundException as e:
        response = make_response({"error": str(e)})
        response.status_code = 404

    except HistoricNotFoundException as e:
        response = make_response({"error": str(e)})
        response.status_code = 404

    except Exception as e:
        response = make_response({"error": str(e)})
        response.status_code = 500

    return response


@historic_blueprint.route("/historic/enrolled_students", methods=["GET"])
def enrolled_students():
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

        response_data = {"results": results}
        response = make_response(response_data)
        response.status_code = 200

    except Exception as e:
        response = make_response({"error": str(e)})
        response.status_code = 500  # Internal Server Error

    return response



@historic_blueprint.route("/historic/get_retention_rate/<int:year>", methods=["GET"])
def get_retention_rate(year):
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
        response.status_code = 200

    except Exception as e:
        response = make_response({"error": str(e)})
        response.status_code = 500  # Internal Server Error

    return response


@historic_blueprint.route("/historic/get_global_approval_rate", methods=["GET"])
def get_global_approval_rate():
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
            "total_alunos": total_students_query,
            "aprovados": approved_query,
            "taxa_aprovacao_global": global_approval_rate
        }

        response = make_response(response_data)
        response.status_code = 200

    except Exception as e:
        response = make_response({"error": str(e)})
        response.status_code = 500

    return response


@historic_blueprint.route("/historic/get_success_rate_year/<int:year>", methods=["GET"])
def get_success_rate_year(year):
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
            "ano": year,
            "total_alunos": total_students_query,
            "aprovados": approved_query,
            "taxa_sucesso": success_rate
        }

        response = make_response(response_data)
        response.status_code = 200

    except Exception as e:
        response = make_response({"error": str(e)})
        response.status_code = 500  # Internal Server Error

    return response


@historic_blueprint.route("/historic/get_abandonment_by_subject/<int:subject_id>", methods=["GET"])
def get_abandonment_by_subject(subject_id):
    try:
        subject = Disciplina.query.filter(Disciplina.id == subject_id)

        if not subject:
            raise SubjectNotFoundException(subject_id)
        
        abandoment_total = Historico.query.filter(
            Historico.id_disciplina == subject_id,
            Historico.status == 4
        ).count()

        total = Historico.query.filter(
            Historico.id_disciplina == subject_id
        ).count()

        abandonment_rate = (abandoment_total / total) * 100

        response_data = {
            "abandoment": abandoment_total,
            "total": total,
            "abandonment_rate": float(f"{abandonment_rate:.2f}")
        }

        response = make_response(response_data)
        response.status_code = 200

    except Exception as e:
        response = make_response({"error": str(e)})
        response.status_code = 500  # Internal Server Error

    return response


@historic_blueprint.route('/historic/subjects_by_student', methods=["GET"])
def subjects_by_student():
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
def create_historic():
    try:
        new_historic = Historico(request.json)

        db.session.add(new_historic)
        db.session.commit()

        response_data = new_historic.to_json()
        response = make_response(response_data)
        response.status_code = 201

    except Exception as e:
        response = make_response({"error": str(e)})
        response.status_code = 500  # Internal Server Error
    
    return response


@historic_blueprint.route('/historico/<int:id>', methods=['PUT'])
def update_historic(id):
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

        response = make_response({"message": f"Historic with id {id} updated successfully"})
        
    except HistoricNotFoundException as e:
        response = make_response({"error": str(e)})
        response.status_code = 404  # Not Found

    except Exception as e:
        response = make_response({"error": str(e)})
        response.status_code = 500

    return response


@historic_blueprint.route('/historico/<int:id>', methods=["DELETE"])
def delete_historic(id):
    try:
        historic = Historico.query.get(id)

        if not historic:
            raise HistoricNotFoundException(id)

        db.session.delete(historic)
        db.session.commit()

        response = make_response({"message": f"Historic with {id} deleted successfully"})
        
    except HistoricNotFoundException as e:
        response = make_response({"error": str(e)})
        response.status_code = 404  # Not Found

    except Exception as e:
        response = make_response({"error": str(e)})
        response.status_code = 500  # Internal Server Error

    return response
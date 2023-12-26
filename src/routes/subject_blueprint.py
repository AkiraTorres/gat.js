from flask import Blueprint, request, make_response
from exceptions.Subject.SubjectAlreadyExistsException import SubjectAlreadyExistsException
from exceptions.Subject.SubjectNotFoundException import SubjectNotFoundException
from models.db import db
from models.Disciplina import Disciplina
from models.Historico import Historico
from models.Aluno import Aluno
from models.Professor import Professor
from sqlalchemy import func

subject_blueprint = Blueprint('subject', __name__)


@subject_blueprint.route("/subjects", methods=["GET"])
def list_subjects() -> object:
    try:
        subjects_list = Disciplina.query.all()
        response = make_response([subject.to_json() for subject in subjects_list])
    
    except Exception as e:
        response = make_response({"error": str(e)})
        response.status_code = 500

    return response


@subject_blueprint.route("/subjects/<int:subject_id>", methods=["PUT"])
def update_disciplina(subject_id: int) -> object:
    try:
        # retornar a disciplina do banco de dados 
        subject = Disciplina.query.get(subject_id)

        if not subject:
            raise SubjectNotFoundException(subject_id)

        # coletar as informações da requisição
        updated_data = request.json
        subject.carga_horaria = updated_data.get('carga_horaria', subject.carga_horaria)
        subject.codigo = updated_data.get('codigo', subject.codigo)
        subject.credito = updated_data.get('credito', subject.credito)
        subject.nome = updated_data.get('nome', subject.nome)
        subject.tipo = updated_data.get('tipo', subject.tipo)

        # subir pro banco de dados 
        db.session.commit()

        response = make_response({"updated_subject": subject.to_json()})

    except SubjectNotFoundException as e:
        response = make_response({"error": str(e)})
        response.status_code = 404

    except Exception as e:
        response = make_response({"error": str(e)})
        response.status_code = 500

    return response


@subject_blueprint.route("/subjects", methods=["POST"])
def create_subject() -> object:
    try:
        # coletar os dados
        data = request.json

        # criar um objeto disciplina
        new_subject = Disciplina(data)

        if find_subject_by_id(new_subject.id):
            raise SubjectAlreadyExistsException(new_subject.id)

        # adicionar no banco de dados 
        db.session.add(new_subject)
        db.session.commit()

        # retornar resposta 
        response = make_response({"created_subject": new_subject.to_json()})
        response.status_code = 201

    except SubjectAlreadyExistsException as e:
        response = make_response({"error": str(e)})
        response.status = 403
    
    except Exception as e:
        response = make_response({"error": str(e)})
        response.status = 500
    
    return response


@subject_blueprint.route("/subjects/<int:subject_id>", methods=["GET"])
def find_subject_by_id(subject_id) -> object:
    try:
        # procurar disciplina pelo no banco de dados 
        subject = Disciplina.query.get(subject_id)

        # verificar se a disciplina existe 
        if not subject:
            raise SubjectNotFoundException(subject_id)

        response = make_response(subject.to_json())
        
    except SubjectNotFoundException as e:
        response = make_response({"error": str(e)})
        response.status_code = 404
      
    except Exception as e:
        response = make_response({"error": str(e)})
        response.status_code = 500
        
    return response
  

@subject_blueprint.route("/subjects/<int:subject_id>", methods=["DELETE"])
def delete_subject_by_id(subject_id: int) -> object:
    try:
        subject = find_subject_by_id(subject_id)
        if not subject:
            raise SubjectNotFoundException(subject_id)
        
        db.session.delete(subject)
        db.session.commit()

        response = make_response({"deleted_subject": subject.to_json()})

    except SubjectNotFoundException as e:
        response = make_response({"error": e})
        response.status_code = 404

    except Exception as e:
        response = make_response({"error": str(e)})
        response.status_code = 500

    return response


@subject_blueprint.route("/subjects/most_failed/<int:year>/<int:semester>", methods=["GET"])
def get_most_failed_subjects(year: int, semester: int) -> object:
    try:
        subjects_with_fails = db.session.query(
            Disciplina.id.label('id_disciplina'),
            Disciplina.codigo.label('codigo_disciplina'),
            Disciplina.nome.label('nome_disciplina'),
            Disciplina.carga_horaria.label('carga_horaria_disciplina'),
            db.func.count().label('total_reprovacoes')
        ).join(
            Historico, Disciplina.id == Historico.id_disciplina
        ).filter(
            (Historico.status == 3) | (Historico.status == 4),
            Historico.ano == year,
            Historico.semestre == semester
        ).group_by(Disciplina.id).order_by(db.desc('total_reprovacoes')).limit(5).all()

        results = []
        for subject in subjects_with_fails:
            result = {
                "subject_id": subject.id_disciplina,
                "subject_cod": subject.codigo_disciplina,
                "subject_name": subject.nome_disciplina,
                "subject_workload": subject.carga_horaria_disciplina,
                "subject_total_fails": subject.total_reprovacoes
            }
            results.append(result)

        response = make_response({"results": results})

    except Exception as e:
        response = make_response({"error": str(e)})
        response.status_code = 500

    return response


@subject_blueprint.route("/subjects/rate/fails/<int:subject_id>", methods=["GET"])
def get_subject_fails_rate(subject_id: int) -> object:
    try:
        if not find_subject_by_id(subject_id):
            raise SubjectNotFoundException(subject_id)

        failed_students = Historico.query.filter(
            Historico.id_disciplina == subject_id,
            (Historico.status == 3) | (Historico.status == 4)
        ).count()

        total_students = Historico.query.filter(
            Historico.id_disciplina == subject_id
        ).count()

        if total_students > 0:
            fail_rate = (failed_students / total_students) * 100
        else:
            fail_rate = 0

        response_data = {
            "subject_id": subject_id,
            "total_students": total_students,
            "failed_students": failed_students,
            "fail_rate": fail_rate
        }

        response = make_response(response_data)

    except SubjectNotFoundException as e:
        response = make_response({"error": str(e)})
        response.status_code = 404

    except Exception as e:
        response = make_response({"error": str(e)})
        response.status_code = 500  # Internal Server Error

    return response


#Média de Notas por Disciplina
@subject_blueprint.route("/subjects/grade/average/<int:subject_id>", methods=["GET"])
def get_subject_average_grade(subject_id: int) -> object:
    try:
        if not find_subject_by_id(subject_id):
            raise SubjectNotFoundException(subject_id)

        sum_of_grades = Historico.query.with_entities(func.sum(Historico.nota)).filter(
            Historico.id_disciplina == subject_id,
            (Historico.status == 1) | (Historico.status == 2) | (Historico.status == 3) | (Historico.status == 4)
        ).scalar()

        total_students = Historico.query.filter(
            Historico.id_disciplina == subject_id,
            (Historico.status == 1) | (Historico.status == 2) | (Historico.status == 3) | (Historico.status == 4)
        ).count()

        if total_students > 0:
            average_grade = sum_of_grades / total_students
        else:
            average_grade = 0  # Handle the case where there are no students for that discipline

        response_data = {
            "subject_id": subject_id,
            "average": average_grade, # It's returning bad values (BD inserts erro)
        }

        response = make_response(response_data)

    except SubjectNotFoundException as e:
        response = make_response({"error": str(e)})
        response.status_code = 404

    except Exception as e:
        response = make_response({"error": str(e)})
        response.status_code = 500  # Internal Server Error

    return response


# Taxa de retenção de alunos por disciplina
@subject_blueprint.route("/subjects/rate/retention/<int:subject_id>", methods=["GET"])
def get_retention_rate_disciplina(subject_id: int) -> object:
    try:
        if not find_subject_by_id(subject_id):
            raise SubjectNotFoundException(subject_id)

        count_aproved_students = Historico.query.filter(
            Historico.id_disciplina == subject_id,
            (Historico.status == 1) | (Historico.status == 2)
        ).count()

        count_reproved_students = Historico.query.filter(
            Historico.id_disciplina == subject_id,
            (Historico.status == 3) | (Historico.status == 4)
        ).count()

        total_students = count_aproved_students + count_reproved_students

        retention_rate = count_reproved_students/total_students

        response_data = {
            "subject_id": subject_id,
            "Number of approved students" : count_aproved_students,
            "Number of failed students" : count_reproved_students,
            "Retention rate": retention_rate
        }

        response = make_response(response_data)

    except SubjectNotFoundException as e:
        response = make_response({"error": str(e)})
        response.status_code = 404

    except Exception as e:
        response = make_response({"error": str(e)})
        response.status_code = 500  # Internal Server Error

    return response


@subject_blueprint.route("/subjects/students/failed_by_times/<int:subject_id>/<int:times>", methods=["GET"])
def get_students_that_failed_more_than_times(subject_id: int, times: int) -> object:
    try:
        if not find_subject_by_id(subject_id):
            raise SubjectNotFoundException(subject_id)

        failed = Historico.query.filter(
            Historico.id_disciplina == subject_id,
            (Historico.status == 3) | (Historico.status == 4)
        ).all()

        failed_students = {}

        for historic in failed:
            student = historic.cpf_aluno
            if student not in failed_students:
                failed_students[student] = 0
            failed_students[student] += 1

        students_that_failed_more_than_n_times = [student for student, count in failed_students.items() if count > times]

        response_data = {
            "subject_id": subject_id,
            "students_that_failed_more_than_n_times": students_that_failed_more_than_n_times
        }

        response = make_response(response_data)

    except SubjectNotFoundException as e:
        response = make_response({"error": str(e)})
        response.status_code = 404

    except Exception as e:
        response = make_response({"error": str(e)})
        response.status_code = 500  # Internal Server Error

    return response


@subject_blueprint.route("/subjects/average/credits", methods=["GET"])
def get_average_credits_by_subject() -> object:
    try:
        data = db.session.query(func.avg(Disciplina.credito).label('avg')).filter(Disciplina.credito != -999)

        average = data[0].avg

        response_data = {"average_credits": eval(f"{average:.2f}")}
        response = make_response(response_data)
    
    except Exception as e:
        response = make_response({"error": str(e)})
        response.status_code = 500  # Internal Server Error

    return response


@subject_blueprint.route("/subjects/average/workload", methods=["GET"])
def get_average_workload_by_subject() -> object:
    try:
        data = db.session.query(func.avg(Disciplina.carga_horaria).label('avg'))

        average = data[0].avg

        response_data = {"average_workload": eval(f"{average:.2f}")}
        response = make_response(response_data)
    
    except Exception as e:
        response = make_response({"error": str(e)})
        response.status_code = 500  # Internal Server Error

    return response

  
# Taxa de aprovacao por disciplina
@subject_blueprint.route("/subject/approval/<int:subject_id>", methods=["GET"])
def get_approval_rate_disciplina(subject_id: int) -> object:
    try:
        if not find_subject_by_id(subject_id):
            raise SubjectNotFoundException(subject_id)

        count_aproved_students = Historico.query.filter(
            Historico.id_disciplina == subject_id,
            (Historico.status == 1) | (Historico.status == 2)
        ).count()

        count_reproved_students = Historico.query.filter(
            Historico.id_disciplina == subject_id,
            (Historico.status == 3) | (Historico.status == 4)
        ).count()

        total_students = count_aproved_students + count_reproved_students

        approval_rate = count_aproved_students/total_students

        response_data = {
            "subject_id": subject_id,
            "number of approved students" : count_aproved_students,
            "number of failed students" : count_reproved_students,
            "approval rate": approval_rate
        }

        response = make_response(response_data)

    except SubjectNotFoundException as e:
        response = make_response({"error": str(e)})
        response.status_code = 404  # Internal Server Error

    except Exception as e:
        response = make_response({"error": str(e)})
        response.status_code = 500  # Internal Server Error

    return response


@subject_blueprint.route("/subjects/rate/attending_students", methods=["GET"])
def get_students_attending_subject_rate() -> object:
    try:
        #todas as disciplinas 
        subjects_list = Disciplina.query.all()
        total_students = Aluno.query.all()
        rate = 0
        result = []
        for subject in subjects_list:

            currentStudents = Historico.query.filter(
                Historico.id_disciplina == subject.id,
                (Historico.status == 5)
            ).all()

            rate = len(currentStudents)/len(total_students)

            current = {
                "Subject" : subject.id,
                "Attending students rate" : rate
            }
            result.append(current)

        response = make_response(result)

    except Exception as e:
        response = make_response({"error": str(e)})
        response.status_code = 500
        
    return response


@subject_blueprint.route("/subjects/rate/total_abandonment", methods=["GET"])
def get_total_abandonment_rate() -> object:
    try:
        # Encontrar a quantidade total de alunos
        total_students = Aluno.query.count()

        # Ver todos os alunos que têm o status 4 ou 6
        quiting_students = Historico.query.filter(
            (Historico.status == 4) | (Historico.status == 6)
        ).distinct(Historico.cpf_aluno).count()

        # Calcular a taxa de desistência geral
        taxa_desistencia = (quiting_students / total_students) * 100 if total_students != 0 else 0
        
        result = {
            "Total of students": total_students,
            "Quiting students": quiting_students,
            "Abandonment rate" : taxa_desistencia
        }

        response = make_response(result)

    except Exception as e:
        response = make_response({"error": str(e)})
        response.status_code = 500

    return response

    
@subject_blueprint.route("/subjects/fails/<int:id>", methods=["GET"])
def get_fails_by_subject(id: int) -> object:
    try:
        if not find_subject_by_id(id):
            raise SubjectNotFoundException(id)

        fails = Historico.query.filter(Historico.id_disciplina == id, (Historico.status == 3) | (Historico.status == 4)).count()
        
        response_data = {
            "Fails" : fails
        }

        response = make_response(response_data)

    except SubjectNotFoundException as e:
        response = make_response({"error": str(e)})
        response.status_code = 404

    except Exception as e:
        response = make_response({"error": str(e)})
        response.status_code = 500

    return response


@subject_blueprint.route("/subjects/approval/professor", methods=["GET"])
def get_approval_by_professor() -> object:
    try:
        # Encontrar todos os professores
        professors = Professor.query.all()

        result_by_professor = []

        # Iterar sobre todos os professores
        for professor in professors:
            # Encontrar todas as disciplinas ministradas pelo professor
            professor_subjects = Disciplina.query.filter_by(matricula_professor=professor.matricula).all()

            # Inicializar contadores
            total_subjects = 0
            failed_subjects = 0

            # Calcular a taxa de aprovação para cada disciplina
            for subject in professor_subjects:
                # Contar o número de alunos que foram aprovados na disciplina
                students_approved_in_subject = Historico.query.filter(
                    (Historico.id_disciplina == subject.id) & ((Historico.status == 1) | ( Historico.status == 2))   # Assumindo que o status 1 representa aprovação
                ).count()

                # Contar o número total de alunos na disciplina
                total_students_in_subject = Historico.query.filter(
                    Historico.id_disciplina == subject.id
                ).count()

                # Adicionar ao total geral
                total_students += total_students_in_subject
                approved_students += students_approved_in_subject

            # Calcular a taxa de aprovação geral para o professor
            professor_approval_rate = (approved_students / total_students) * 100 if total_students != 0 else 0

            # Adicionar resultado ao resultado final
            professor_result = professor
            professor_result["Approval rate"] = professor_approval_rate

            result_by_professor.append(professor_result)

        response = make_response(result_by_professor)

    except Exception as e:
        response = make_response({"error": str(e)})
        response.status_code = 500

    return result_by_professor
    
    
@subject_blueprint.route("/subjects/grade/distribution/<int:id>", methods=["GET"])
def get_grade_distribution_by_subject(id: int) -> object:
    try:
        if not find_subject_by_id(id):
            raise SubjectNotFoundException(id)
        
        subjects_count = Historico.query.filter(Historico.id_disciplina == id).count()

        subject_studied = Historico.query.filter(Historico.id_disciplina == id).all()
        
        grades_sum = 0

        for subject in subject_studied:
            historic = Historico.query.filter(Historico.id == subject.id).first()
            if historic:
                grades_sum += historic.nota

        grade_distribution = grades_sum/subjects_count

        response_data = {
            "Grade distribution": grade_distribution
        }

        response = make_response(response_data)

    except SubjectNotFoundException as e:
        response = make_response({"error": str(e)})
        response.status_code = 404

    except Exception as e:
        response = make_response({"error": str(e)})
        response.status_code = 500

    return response

@subject_blueprint.route("/subjects/rate/graduate", methods=["GET"])
def graduation_rate():
    try:
        students = Aluno.query.all()
        students_total = Aluno.query.count()

        graduated = 0
        graduated_rate = 0

        for student in students:
            mandatory_total =  0
            approved_mandatory = 0
    
            approveds = Historico.query.filter(Historico.cpf_aluno == student.cpf, (Historico.status == 1) | (Historico.status == 2) | (Historico.status == 7)).all()
            mandatories = Disciplina.query.filter(Disciplina.tipo == 1).all()
            mandatory_total = Disciplina.query.filter(Disciplina.tipo == 1).count()
            
            for mandatory in mandatories:
                for approved in approveds:
                    if approved.id_disciplina == mandatory.id:
                        approved_mandatory += 1

            if approved_mandatory == mandatory_total:
                graduated += 1
        
        graduated_rate = graduated/students_total

        response_data = {
            "taxa_graduacao" : graduated_rate
        }

        response = make_response(response_data)
        response.status_code = 200

    except Exception as e:
        response = make_response({"error": str(e)})
        response.status_code = 500

    return response
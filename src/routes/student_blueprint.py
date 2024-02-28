from flask import Blueprint, jsonify, request, make_response
from models.db import db
from models.Aluno import Aluno
from models.Historico import Historico
from models.Disciplina import Disciplina
from sqlalchemy import func
from exceptions.Student.StudentNotFoundException import StudentNotFoundException
from exceptions.Student.StudentAlreadyExistsException import StudentAlreadyExistsException
from flask_jwt_extended import jwt_required

# cria o blueprint do aluno
student_blueprint = Blueprint('student', __name__)

# rota para criar um aluno 
@student_blueprint.route('/students', methods=['POST'])
@jwt_required()
def create_student() -> object:
    try:
        student_data = request.json

        student = Aluno.query.get(student_data["cpf"])
        if student:
            raise StudentAlreadyExistsException(student.cpf)

        new_student = Aluno(student_data)
        db.session.add(new_student)
        db.session.commit()

        response = make_response({"created_student": new_student.to_json()})
        response.status_code = 201

    except StudentAlreadyExistsException as e:
        response = make_response({"error": str(e)}) 
        response.status_code = 403

    except Exception as e:
        response = make_response({"error": str(e)})
        response.status_code = 500  # Internal Server Error

    return response


#rota para listar todos os alunos
@student_blueprint.route("/students", methods=["GET"])
@jwt_required()
def list_students() -> object:
    try:
        students_list = Aluno.query.all()
        response = make_response([aluno.to_json() for aluno in students_list])

    except Exception as e:
        response = make_response({"error": str(e)})
        response.status_code = 500  # Internal Server Error

    return response


# encontrar aluno por id
@student_blueprint.route("/students/<string:cpf>", methods=["GET"])
@jwt_required()
def get_student_by_cpf(cpf: str) -> object:
    try:
        student = Aluno.query.get(cpf)
        if not student:
            raise StudentNotFoundException(cpf)

        response = make_response(student.to_json())

    except StudentNotFoundException as e:
        response = make_response({"error": str(e)}) 
        response.status_code = 404

    except Exception as e:
        response = make_response({"error": str(e)})
        response.status_code = 500  # Internal Server Error

    return response


# Atualizar aluno por id
@student_blueprint.route('/students/<string:cpf>', methods=['PUT'])
@jwt_required()
def update_student(cpf: str) -> object:
    try:
        student = Aluno.query.get(cpf)

        if not student:
            raise StudentAlreadyExistsException(student.cpf)

        updated_data = request.json

        student.nome = updated_data.get('nome', student.nome)
        student.arg_class = updated_data.get('arg_class', student.arg_class)
        student.ano_entrada = updated_data.get('ano_entrada', student.ano_entrada)

        db.session.commit()

        response = make_response({"updated_student": student.to_json()})

    except StudentNotFoundException as e:
        response = make_response({"error": str(e)}) 
        response.status_code = 404

    except Exception as e:
        response = make_response({"error": str(e)})
        response.status_code = 500  # Internal Server Error

    return response


# Deletar aluno por id
@student_blueprint.route('/students/<string:cpf>', methods=['DELETE'])
@jwt_required()
def delete_aluno_por_cpf(cpf: str) -> object:
    try:
        student = Aluno.query.get(cpf)

        if not student:
            raise StudentNotFoundException(student.cpf)

        db.session.delete(student)
        db.session.commit()

        response = make_response({"deleted_student": student.to_json()})

    except StudentNotFoundException as e:
        response = make_response({"error": str(e)}) 
        response.status_code = 404

    except Exception as e:
        response = make_response({"error": str(e)})
        response.status_code = 500  # Internal Server Error

    return response


# Taxa de aproveitamento de créditos
@student_blueprint.route("/students/credit/<string:cpf>", methods=["GET"])
@jwt_required()
def get_credits_rate(cpf: str) -> object:
    try:
        student = Aluno.query.filter(Aluno.cpf == cpf).first()
        if not student:
            raise StudentNotFoundException(cpf)

        subject_cursed = Historico.query.filter(Historico.cpf_aluno == student.cpf).all()
        
        credits_cursed = 0
        for subject in subject_cursed:
            disciplina = Disciplina.query.filter(Disciplina.id == subject.id_disciplina).first()
            if disciplina:
                credits_cursed += disciplina.credito

        # Obtendo todas as disciplinas disponíveis
        all_subjects = Disciplina.query.all()

        # Calculando os créditos das disciplinas não cursadas
        credits_not_cursed = sum(subject.credito for subject in all_subjects) - credits_cursed
        credit_rate = credits_cursed / credits_not_cursed

        response_data = {
            "used_credits": credits_cursed,
            "unused_credits" : credits_not_cursed, # Bad result (BD insert)
            "credit_utilization_rate" : credit_rate
            }

        response = make_response(response_data)

    except StudentNotFoundException as e:
        response = make_response({"error": str(e)}) 
        response.status_code = 404

    except Exception as e:
        response = make_response({"error": str(e)})
        response.status_code = 500

    return response


@student_blueprint.route("/students/performance", methods=["GET"])
@jwt_required()
def performance() -> object:
    try:
        students = Aluno.query.all()

        total_enem_students = 0
        total_ssa_students = 0
        total_sum_enem_students = 0
        total_sum_ssa_students = 0

        for student in students:
            if student.arg_class > 100:
                total_enem_students += 1
            else:
                total_ssa_students += 1

            count_aproved_students = Historico.query.filter(
                Historico.cpf_aluno == student.cpf,
                (Historico.status == 1) | (Historico.status == 2)
            ).count()

            if student.arg_class > 100:
                total_sum_enem_students += count_aproved_students
            else:
                total_sum_ssa_students += count_aproved_students

        enem_rate = total_sum_enem_students / total_enem_students if total_enem_students != 0 else 0
        ssa_rate = total_sum_ssa_students / total_ssa_students if total_ssa_students != 0 else 0

        response_data = {
            "Enem": total_enem_students,
            "SSA": total_ssa_students,
            "Number of approvals in subjects by student that entered through Enem": total_sum_enem_students,
            "Number of approvals in subjects by student that entered through Enem": total_sum_ssa_students,
            "SSA_utilization_rate": ssa_rate,
            "Enem_utilization_rate": enem_rate
        }

        response = make_response(response_data)

    except Exception as e:
        response = make_response({"error": str(e)})
        response.status_code = 500

    return response

  
@student_blueprint.route("/students/subjects/electives/<string:cpf>", methods=["GET"])
@jwt_required()
def get_how_many_electives(cpf: str) -> object:
    try:
        student = Aluno.query.get(cpf)
        if not student:
            raise StudentNotFoundException(cpf)
        
        subjects = db.session.query(
            Disciplina
        ).join(
            Historico, Disciplina.id == Historico.id_disciplina
        ).filter(
            Disciplina.tipo == 2,
            Historico.cpf_aluno == cpf,
            (Historico.status == 1) |
            (Historico.status == 2) |
            (Historico.status == 7)
        ).all()

        subjects = [subject.to_json() for subject in subjects]

        response_data = student.to_json()
        response_data["subjects"] = subjects

        response = make_response(response_data)
    
    except StudentNotFoundException as e:
        response = make_response({"error": str(e)}) 
        response.status_code = 404

    except Exception as e:
        response = make_response({"error": str(e)})
        response.status_code = 500  # Internal Server Error

    return response


@student_blueprint.route("/students/subjects/mandatory/<string:cpf>", methods=["GET"])
@jwt_required()
def get_how_many_mandatory(cpf: str) -> object:
    try:
        student = Aluno.query.get(cpf)
        if not student:
            raise StudentNotFoundException(cpf)
        
        subjects = db.session.query(
            Disciplina
        ).join(
            Historico, Disciplina.id == Historico.id_disciplina
        ).filter(
            Disciplina.tipo == 1,
            Historico.cpf_aluno == cpf,
            (Historico.status == 1) |
            (Historico.status == 2) |
            (Historico.status == 7)
        ).all()

        subjects = [subject.to_json() for subject in subjects]

        response_data = student.to_json()
        response_data["subjects"] = subjects

        response = make_response(response_data)
    
    except StudentNotFoundException as e:
        response = make_response({"error": str(e)}) 
        response.status_code = 404

    except Exception as e:
        response = make_response({"error": str(e)})
        response.status_code = 500  # Internal Server Error

    return response


@student_blueprint.route("/students/performance/overall", methods=["GET"])
@jwt_required()
def get_overall_academic_performance() -> object:
    try:
        data = db.session.query(func.avg(Historico.nota).label('avg')).filter(Historico.nota != -999).all()
        total_subjects = Disciplina.query.count()

        response_data = data[0].avg / total_subjects * 100
        response = make_response({"overall_academic_performance": f"{response_data:.2f}%"})

        return response

    except Exception as e:
        response = make_response({"error": str(e)})
        response.status_code = 500  # Internal Server Error
    
    return response


@student_blueprint.route("/students/conclusion_rate/<string:cpf>", methods=["GET"])
@jwt_required()
def get_student_conclusion_rate(cpf: str) -> object:
    try:
        student = Aluno.query.filter(Aluno.cpf == cpf).first()

        if not student:
            raise StudentNotFoundException(cpf)

        approved = 0
        approval_rate = 0

        approved = Historico.query.filter(Historico.cpf_aluno == cpf, (Historico.status == 1) | (Historico.status == 2) | (Historico.status == 7)).count()
        
        approval_rate = approved/50

        response_data = {
            "Approved subjects": approved,
            "Conclusion rate": approval_rate
        }

        response = make_response(response_data)

    except StudentNotFoundException as e:
        response = make_response({"error": str(e)})
        response.status_code = 404

    except Exception as e:
        response = make_response({"error": str(e)})
        response.status_code = 500

    return response

@student_blueprint.route("/students/fails/<string:cpf>", methods=["GET"])
@jwt_required()
def get_student_fails(cpf: str) -> object:
    try:
        student = Aluno.query.filter(Aluno.cpf == cpf).first()

        if not student:
            raise StudentNotFoundException(cpf)

        fails = Historico.query.filter(Historico.cpf_aluno == cpf, (Historico.status == 3) | (Historico.status == 4)).count()
        
        if(fails >= 10):
            response_data = {
                "Fails" : fails
            }
        else:
            response_data = {
                "Fails" : fails
            }

        response = make_response(response_data)

    except StudentNotFoundException as e:
        response = make_response({"error": str(e)})
        response.status_code = 404

    except Exception as e:
        response = make_response({"error": str(e)})
        response.status_code = 500

    return response

  
# media dos alunos por componente curricular 
@student_blueprint.route('/students/average/grade', methods=['GET'])
@jwt_required()
def get_average_grade() -> object:
    try:
        # coletar todas as disciplinas
        subjects = Disciplina.query.all()
        result_by_subject = []

        for subject in subjects:
            # Filtrar os registros para a disciplina específica e os critérios desejados
            subject_historics = Historico.query.filter(
                (Historico.id_disciplina == subject.id) &
                ((Historico.status == 1) | (Historico.status == 2) | (Historico.status == 3) | (Historico.status == 4) | (Historico.status == 5))
            ).all()

            # Calcular a soma das notas dos alunos na disciplina
            sum_subject_grade = sum(historic.nota for historic in subject_historics)

            # Verificar o total de alunos na disciplina
            total_students_on_subject = len(subject_historics)

            # calcular a media dos alunos
            if total_students_on_subject != 0:
                avg = sum_subject_grade / total_students_on_subject
            else:
                avg = 0                

            resultado = {
                'Subject:' : subject.nome,
                'Total number of students in the subject' : total_students_on_subject,
                'Average:' : avg
            }

            result_by_subject.append(resultado)

        response = make_response(result_by_subject)

    except Exception as e:
        # Handle the exception here, you can log the error or return an error response
        response = make_response({'error': str(e)})
        response.status_code = 404
    
    return response
        

@student_blueprint.route('/students/approved/<string:cpf>', methods=['GET'])
@jwt_required()
def get_student_approved_subjects(cpf: str) -> object:
    try:
        subjects = Disciplina.query.all()
        approved_subjects = []

        if not Aluno.query.get(cpf):
            raise StudentNotFoundException(cpf)

        for subject in subjects:
            # Filtrar os registros para a disciplina específica já cursada
            approved_subject = Historico.query.filter(
                (Historico.id_disciplina == subject.id) & ((Historico.cpf_aluno == cpf) & ((Historico.status == 1) | (Historico.status == 2)))
            ).first()  # Alteração aqui para obter apenas um registro

            if approved_subject:
                approved_subjects.append(subject.nome)

        response = make_response(approved_subjects)

    except StudentNotFoundException as e:
        response = make_response({"error": str(e)})
        response.status_code = 404

    except Exception as e:
        # Lidar com a exceção aqui, você pode registrar o erro ou retornar uma resposta de erro
        response = make_response({'error': str(e)})
        response.status_code = 500

    return response

        
@student_blueprint.route("/students/grade/distibution/<string:cpf>", methods=["GET"])
@jwt_required()
def get_student_grade_distribution(cpf: str) -> object:
    try:
        student = Aluno.query.filter(Aluno.cpf == cpf).first()

        if not student:
            raise StudentNotFoundException(cpf)
        
        subjects_count = Historico.query.filter(Historico.cpf_aluno == cpf).count()

        subject_studied = Historico.query.filter(Historico.cpf_aluno == student.cpf).all()
        
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

    except StudentNotFoundException as e:
        response = make_response({"error": str(e)})
        response.status_code = 404

    except Exception as e:
        response = make_response({"error": str(e)})
        response.status_code = 500

    return response

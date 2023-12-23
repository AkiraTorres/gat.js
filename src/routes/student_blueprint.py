from flask import Blueprint, jsonify, request, make_response
from models.db import db
from models.Aluno import Aluno
from models.Historico import Historico
from models.Disciplina import Disciplina
from sqlalchemy import func
from exceptions.Student.StudentNotFoundException import StudentNotFoundException
from exceptions.Student.StudentAlreadyExistsException import StudentAlreadyExistsException

# cria o blueprint do aluno
student_blueprint = Blueprint('alunos', __name__)

# rota para criar um aluno 
@student_blueprint.route('/alunos', methods=['POST'])
def create_aluno():
    try:
        dados_aluno = request.json

        aluno = get_aluno_by_cpf(dados_aluno.cpf)
        if aluno:
            raise StudentAlreadyExistsException(aluno.cpf)

        # novo_aluno = Aluno(nome, cpf, arg_class, ano_entrada)
        novo_aluno = Aluno(dados_aluno)
        db.session.add(novo_aluno)
        db.session.commit()

        response = make_response({'message': 'Aluno criado com sucesso', 'cpf': novo_aluno.cpf})
        response.status_code = 201

    except StudentNotFoundException as e:
        response = make_response({"error": str(e)}) 
        response.status_code = 422

    except Exception as e:
        response = make_response({"error": str(e)})
        response.status_code = 500  # Internal Server Error

    return response


#rota para listar todos os alunos 
@student_blueprint.route("/alunos", methods=["GET"])
def list_alunos():
    try:
        alunos_list = Aluno.query.all()
        response = make_response([aluno.to_json() for aluno in alunos_list])
        response.status_code = 200

    except Exception as e:
        response = make_response({"error": str(e)})
        response.status_code = 500  # Internal Server Error

    return response


# encontrar aluno por id
@student_blueprint.route("/alunos/<cpf>", methods=["GET"])
def get_aluno_by_cpf(cpf):
    try:
        aluno = Aluno.query.get(cpf)
        if not aluno:
            raise StudentNotFoundException(cpf)

        response = make_response(aluno.to_json())
        response.status_code = 200

    except StudentNotFoundException as e:
        response = make_response({"error": str(e)}) 
        response.status_code = 404

    except Exception as e:
        response = make_response({"error": str(e)})
        response.status_code = 500  # Internal Server Error

    return response


# Atualizar aluno por id
@student_blueprint.route('/alunos/<cpf>', methods=['PUT'])
def update_aluno(cpf):
    try:
        aluno = Aluno.query.get(cpf)

        if not aluno:
            raise StudentAlreadyExistsException(aluno.cpf)

        dados_atualizados = request.json

        aluno.nome = dados_atualizados.get('nome', aluno.nome)
        # aluno.cpf = dados_atualizados.get('cpf', aluno.cpf)  # não atualizar o cpf, pois é a chave primária
        aluno.arg_class = dados_atualizados.get('arg_class', aluno.arg_class)
        aluno.ano_entrada = dados_atualizados.get('ano_entrada', aluno.ano_entrada)

        db.session.commit()

        response = make_response({'message': 'Aluno atualizado com sucesso'})

    except StudentNotFoundException as e:
        response = make_response({"error": str(e)}) 
        response.status_code = 422

    except Exception as e:
        response = make_response({"error": str(e)})
        response.status_code = 500  # Internal Server Error

    return response


# Deletar aluno por id
@student_blueprint.route('/alunos/<cpf>', methods=['DELETE'])
def delete_aluno_por_cpf(cpf):
    try:
        aluno = Aluno.query.get(cpf)

        if not aluno:
            raise StudentNotFoundException(aluno.cpf)

        db.session.delete(aluno)
        db.session.commit()

        response = make_response({'message': 'Aluno excluído com sucesso'})

    except StudentNotFoundException as e:
        response = make_response({"error": str(e)}) 
        response.status_code = 404

    except Exception as e:
        response = make_response({"error": str(e)})
        response.status_code = 500  # Internal Server Error

    return response


# Taxa de aproveitamento de créditos
@student_blueprint.route("/creditos_aluno/<cpf>", methods=["GET"])
def get_credits_rate(cpf):
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
            "Créditos aproveitados": credits_cursed,
            "Créditos não aproveitados" : credits_not_cursed, # Bad result (BD insert)
            "Taxa de aproveitamento de créditos" : credit_rate
            }

        response = make_response(response_data)
        response.status_code = 200

    except StudentNotFoundException as e:
        response = make_response({"error": str(e)}) 
        response.status_code = 422

    except Exception as e:
        response_data = {"error": str(e)}
        response = make_response(response_data)
        response.status_code = 500

    return response


@student_blueprint.route("/desempenho/", methods=["GET"])
def performance():
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
            "Numero de aprovações de alunos nas disciplinas que entraram pelo Enem": total_sum_enem_students,
            "Numero de aprovações de alunos nas disciplinas que entraram pelo SSA": total_sum_ssa_students,
            "Taxa de aproveitamento SSA": ssa_rate,
            "Taxa de aproveitamento Enem": enem_rate
        }

        response = make_response(response_data)
        response.status_code = 200

    except Exception as e:
        response = make_response({"error": str(e)})
        response.status_code = 500

    return response

@student_blueprint.route("/taxa_conclusao/<cpf>", methods=["GET"])
def taxa_conclusao(cpf):
    try:
        student = Aluno.query.filter(Aluno.cpf == cpf).first()

        if not student:
            raise StudentNotFoundException(cpf)

        approved = 0
        approval_rate = 0

        approved = Historico.query.filter(Historico.cpf_aluno == cpf, (Historico.status == 1) | (Historico.status == 2) | (Historico.status == 7)).count()
        
        approval_rate = approved/50

        response_data = {
            "Matérias aprovadas": approved,
            "Taxa de conclusão": approval_rate
        }

        response = make_response(response_data)
        response.status_code = 200

    except Exception as e:
        response = make_response({"error": str(e)})
        response.status_code = 500

    return response

@student_blueprint.route("/reprovacoes_aluno/<cpf>", methods=["GET"])
def reprovacoes_aluno(cpf):
    try:
        student = Aluno.query.filter(Aluno.cpf == cpf).first()

        if not student:
            raise StudentNotFoundException(cpf)

        fails = Historico.query.filter(Historico.cpf_aluno == cpf, (Historico.status == 3) | (Historico.status == 4)).count()
        
        if(fails >= 10):
            response_data = {
                "Reprovações" : fails,
                "Alerta" : "Você está com muitas reprovações, entre em contato com a escolaridade"
            }
        else:
            response_data = {
                "Reprovações" : fails
            }

        response = make_response(response_data)
        response.status_code = 200

    except Exception as e:
        response = make_response({"error": str(e)})
        response.status_code = 500

    return response

@student_blueprint.route("/distribuicao_aluno/<cpf>", methods=["GET"])
def distribuicao_aluno(cpf):
    try:
        student = Aluno.query.filter(Aluno.cpf == cpf).first()

        if not student:
            raise StudentNotFoundException(cpf)
        
        subjects_count = Historico.query.filter(Historico.cpf_aluno == cpf).count()

        subject_studied = Historico.query.filter(Historico.cpf_aluno == student.cpf).all()
        
        grades_sum = 0

        for subject in subject_studied:
            historico = Historico.query.filter(Historico.id == subject.id).first()
            if historico:
                grades_sum += historico.nota

        grade_distribution = grades_sum/subjects_count

        response_data = {
            "Distribuição de nota": grade_distribution
        }

        response = make_response(response_data)
        response.status_code = 200

    except Exception as e:
        response = make_response({"error": str(e)})
        response.status_code = 500

    return response
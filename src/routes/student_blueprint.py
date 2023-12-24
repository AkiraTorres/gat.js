from flask import Blueprint, jsonify, request, make_response
from models.db import db
from models.Aluno import Aluno
from models.Historico import Historico
from models.Disciplina import Disciplina
from sqlalchemy import func

# cria o blueprint do aluno
student_blueprint = Blueprint('alunos', __name__)

# rota para criar um aluno 
@student_blueprint.route('/alunos', methods=['POST'])
def create_aluno():
    dados_aluno = request.json

    # novo_aluno = Aluno(nome, cpf, arg_class, ano_entrada)
    novo_aluno = Aluno(dados_aluno)
    db.session.add(novo_aluno)
    db.session.commit()

    response = make_response({'message': 'Aluno criado com sucesso', 'id': novo_aluno.id})
    response.status_code = 201

    return response


#rota para listar todos os alunos 
@student_blueprint.route("/alunos", methods=["GET"])
def list_alunos():
    alunos_list = Aluno.query.all()
    return jsonify([aluno.to_json() for aluno in alunos_list])


# encontrar aluno por id
@student_blueprint.route("/alunos/<cpf>", methods=["GET"])
def get_aluno_by_cpf(cpf):

    aluno = Aluno.query.get(cpf)

    if not aluno:
        response = make_response({'message': 'Aluno não encontrado'})
        response.status_code = 404
    else:
        response = make_response(aluno.to_json())
        response.status_code = 200
    return response


# Atualizar aluno por id
@student_blueprint.route('/alunos/<cpf>', methods=['PUT'])
def update_aluno(cpf):
    aluno = Aluno.query.get(cpf)

    if not aluno:
        response = make_response({'message': 'Aluno não encontrado'})
        response.status_code = 404
        return response

    dados_atualizados = request.json

    aluno.nome = dados_atualizados.get('nome', aluno.nome)
    # aluno.cpf = dados_atualizados.get('cpf', aluno.cpf)  # não atualizar o cpf, pois é a chave primária
    aluno.arg_class = dados_atualizados.get('arg_class', aluno.arg_class)
    aluno.ano_entrada = dados_atualizados.get('ano_entrada', aluno.ano_entrada)

    db.session.commit()

    response = make_response({'message': 'Aluno atualizado com sucesso'})
    return response


# Deletar aluno por id
@student_blueprint.route('/alunos/<cpf>', methods=['DELETE'])
def delete_aluno_por_cpf(cpf):
    aluno = Aluno.query.get(cpf)

    if not aluno:
        response = make_response({'message': 'Aluno não encontrado'})
        response.status_code = 404
        return response

    db.session.delete(aluno)
    db.session.commit()

    response = make_response({'message': 'Aluno excluído com sucesso'})
    return response

# Taxa de aproveitamento de créditos
@student_blueprint.route("/creditos_aluno/<cpf>", methods=["GET"])
def get_credits_rate(cpf):
    try:
        student = Aluno.query.filter(Aluno.cpf == cpf).first()
        if student:


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
            response_status = 200
        else:
            response_data = {"message": "Aluno não encontrado"}
            response_status = 404

        response = make_response(response_data)
        response.status_code = response_status

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
        response_status = 200

        response = make_response(response_data)
        response.status_code = response_status

    except Exception as e:
        response_data = {"error": str(e)}
        response = make_response(response_data)
        response.status_code = 500

    return response


# media dos alunos por componente curricular 

@student_blueprint.route('/mediaComponenteCurricular', methods=['GET'])
def media_componente_curricular():
    try:
        # coletar todas as disciplinas
        disciplinas = Disciplina.query.all()
        resultado_por_disciplina = []

        for disciplina in disciplinas:
            # Filtrar os registros para a disciplina específica e os critérios desejados
            registros_disciplina = Historico.query.filter(
                (Historico.id_disciplina == disciplina.id) &
                ((Historico.status == 1) | (Historico.status == 2) | (Historico.status == 3) | (Historico.status == 4) | (Historico.status == 5))
            ).all()

            # Calcular a soma das notas dos alunos na disciplina
            soma_notas_disciplina = sum(registro.nota for registro in registros_disciplina)

            # Verificar o total de alunos na disciplina
            total_alunos_disciplina = len(registros_disciplina)

            # calcular a media dos alunos
            media = soma_notas_disciplina / total_alunos_disciplina

            resultado = {
                'Disciplina:' : disciplina.nome,
                'Total de alunos' : total_alunos_disciplina,
                'Media:' : media
            }

            resultado_por_disciplina.append(resultado)

        return resultado_por_disciplina

    except Exception as e:
        # Handle the exception here, you can log the error or return an error response
        return {'error': str(e)}
        

@student_blueprint.route('/disciplinasCursadas/<aluno>', methods=['GET'])
def disciplinas_cursadas(aluno):
    try:
        disciplinas = Disciplina.query.all()
        disciplinas_cursadas = []

        for disciplina in disciplinas:
            # Filtrar os registros para a disciplina específica já cursada
            disciplina_cursada = Historico.query.filter(
                (Historico.id_disciplina == disciplina.id) & ((Historico.cpf_aluno == aluno) & ((Historico.status == 1) | (Historico.status == 2)))
            ).first()  # Alteração aqui para obter apenas um registro

            if disciplina_cursada:
                disciplinas_cursadas.append(disciplina.nome)

        return disciplinas_cursadas

    except Exception as e:
        # Lidar com a exceção aqui, você pode registrar o erro ou retornar uma resposta de erro
        return {'error': str(e)}

        
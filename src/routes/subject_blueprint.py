from flask import Blueprint, request, make_response
from models.db import db
from models.Disciplina import Disciplina
from models.Historico import Historico
from sqlalchemy import func

subject_blueprint = Blueprint('disciplinas', __name__)

@subject_blueprint.route("/disciplinas", methods=["GET"])
def list_disciplinas():
    disciplinas_list = Disciplina.query.all()
    return make_response([disc.to_json() for disc in disciplinas_list])


@subject_blueprint.route("/disciplinas/<int:id_disciplina>", methods=["PUT"])
def update_disciplina(id_disciplina):
    # retornar a disciplina do banco de dados 
    disciplina = Disciplina.query.get(id_disciplina)

    if not disciplina:
        response = make_response({'message': 'disciplina não encontrada'})
        response.status_code = 404
        return response

    
    # coletar as informações da requisição
    dados_atualizados = request.json
    disciplina.carga_horaria = dados_atualizados.get('carga_horaria', disciplina.carga_horaria)
    disciplina.codigo = dados_atualizados.get('codigo', disciplina.codigo)
    disciplina.credito = dados_atualizados.get('credito', disciplina.credito)
    disciplina.nome = dados_atualizados.get('nome', disciplina.nome)
    disciplina.tipo = dados_atualizados.get('tipo', disciplina.tipo)

    # subir pro banco de dados 
    db.session.commit()

    return make_response({'message': 'Disciplina atualizada com sucesso'})


@subject_blueprint.route("/disciplinas", methods=["POST"])
def create_subject():
    # coletar os dados
    dados_disciplina = request.json

    # criar um objeto disciplina
    nova_disciplina = Disciplina(dados_disciplina)

    # adicionar no banco de dados 
    db.session.add(nova_disciplina)
    db.session.commit()

    # retornar resposta 

    response = make_response({'message': 'Disciplina criada com sucesso', 'id': nova_disciplina.id})
    response.status_code = 201
    return response

@subject_blueprint.route("/disciplinas/<int:id_disciplina>", methods=["GET"])
def find_subject_by_id(id_disciplina):
    # procurar disciplina pelo no banco de dados 
    disciplina = Disciplina.query.get(id_disciplina)

    # verificar se a disciplina existe 

    if not disciplina:
        response = make_response({'message': 'disciplina não encontrada'})
        response.status_code = 404
        return response
    
    # se existe: mostar a disciplina 
    return  make_response(disciplina.to_json())


@subject_blueprint.route("/disciplinas_que_mais_reprovaram/<int:ano>/<int:semestre>", methods=["GET"])
def disciplinas_que_mais_reprovaram(ano, semestre):
    try:
        disciplinas_reprovadas = db.session.query(
            Disciplina.id.label('id_disciplina'),
            Disciplina.codigo.label('codigo_disciplina'),
            Disciplina.nome.label('nome_disciplina'),
            Disciplina.carga_horaria.label('carga_horaria_disciplina'),
            db.func.count().label('total_reprovacoes')
        ).join(
            Historico, Disciplina.id == Historico.id_disciplina
        ).filter(
            (Historico.status == 3) | (Historico.status == 4),
            Historico.ano == ano,
            Historico.semestre == semestre
        ).group_by(Disciplina.id).order_by(db.desc('total_reprovacoes')).limit(5).all()

        resultados = []
        for disciplina in disciplinas_reprovadas:
            resultado = {
                "id_disciplina": disciplina.id_disciplina,
                "codigo_disciplina": disciplina.codigo_disciplina,
                "nome_disciplina": disciplina.nome_disciplina,
                "carga_horaria_disciplina": disciplina.carga_horaria_disciplina,
                "total_reprovacoes": disciplina.total_reprovacoes
            }
            resultados.append(resultado)

        response_data = {"resultados": resultados}
        response = make_response(response_data)
        response.status_code = 200

    except Exception as e:
        response_data = {"error": str(e)}
        response = make_response(response_data)
        response.status_code = 500

    return response


@subject_blueprint.route("/taxa_reprovacao/<int:id_disciplina>", methods=["GET"])
def get_taxa_reprovacao_disciplina(id_disciplina):
    try:
        query_reprovados = Historico.query.filter(
            Historico.id_disciplina == id_disciplina,
            (Historico.status == 3) | (Historico.status == 4)
        ).count()

        query_total_alunos = Historico.query.filter(
            Historico.id_disciplina == id_disciplina
        ).count()

        if query_total_alunos > 0:
            taxa_reprovacao = (query_reprovados / query_total_alunos) * 100
        else:
            taxa_reprovacao = 0

        response_data = {
            "id_disciplina": id_disciplina,
            "total_alunos": query_total_alunos,
            "reprovados": query_reprovados,
            "taxa_reprovacao": taxa_reprovacao
        }

        response = make_response(response_data)
        response.status_code = 200

    except Exception as e:
        response_data = {"error": str(e)}
        response = make_response(response_data)
        response.status_code = 500  # Internal Server Error

    return response

#Média de Notas por Disciplina
@subject_blueprint.route("/media_disciplina/<int:id_disciplina>", methods=["GET"])
def get_media_disciplina(id_disciplina):
    try:
        sum_of_grade = Historico.query.with_entities(func.sum(Historico.nota)).filter(
            Historico.id_disciplina == id_disciplina,
            (Historico.status == 1) | (Historico.status == 2) | (Historico.status == 3) | (Historico.status == 4)
        ).scalar()

        count_students = Historico.query.filter(
            Historico.id_disciplina == id_disciplina,
            (Historico.status == 1) | (Historico.status == 2) | (Historico.status == 3) | (Historico.status == 4)
        ).count()

        if count_students > 0:
            average_grade = sum_of_grade / count_students
        else:
            average_grade = 0  # Handle the case where there are no students for that discipline

        response_data = {
            "id_disciplina": id_disciplina,
            "média": average_grade, # It's returning bad values (BD inserts erro)
        }

        response = make_response(response_data)
        response.status_code = 200

    except Exception as e:
        response_data = {"error": str(e)}
        response = make_response(response_data)
        response.status_code = 500  # Internal Server Error

    return response

# Taxa de retenção de alunos por disciplina
@subject_blueprint.route("/retencao_disciplina/<int:id_disciplina>", methods=["GET"])
def get_retention_rate_disciplina(id_disciplina):
    try:
        count_aproved_students = Historico.query.filter(
            Historico.id_disciplina == id_disciplina,
            (Historico.status == 1) | (Historico.status == 2)
        ).count()

        count_reproved_students = Historico.query.filter(
            Historico.id_disciplina == id_disciplina,
            (Historico.status == 3) | (Historico.status == 4)
        ).count()

        total_students = count_aproved_students + count_reproved_students

        retention_rate = count_reproved_students/total_students

        response_data = {
            "id_disciplina": id_disciplina,
            "numero_de_aprovados" : count_aproved_students,
            "numero_de_reprovados" : count_reproved_students,
            "taxa de retenção": retention_rate
        }

        response = make_response(response_data)
        response.status_code = 200

    except Exception as e:
        response_data = {"error": str(e)}
        response = make_response(response_data)
        response.status_code = 500  # Internal Server Error

    return response

@subject_blueprint.route("/alunos_retidos_por_disciplina_por_vezes/<int:id_disciplina>/<int:times>", methods=["GET"])
def get_students_failed_more_than_times(id_disciplina, times):
    try:
        reprovados = Historico.query.filter(
            Historico.id_disciplina == id_disciplina,
            (Historico.status == 3) | (Historico.status == 4)
        ).all()

        alunos_reprovados = {}

        for registro in reprovados:
            aluno = registro.cpf_aluno
            if aluno not in alunos_reprovados:
                alunos_reprovados[aluno] = 0
            alunos_reprovados[aluno] += 1

        alunos_reprovados_mais_de_vezes = [aluno for aluno, count in alunos_reprovados.items() if count > times]

        response_data = {
            "id_disciplina": id_disciplina,
            "alunos_reprovados_mais_de_vezes": alunos_reprovados_mais_de_vezes
        }

        response = make_response(response_data)
        response.status_code = 200

    except Exception as e:
        response = make_response({"error": str(e)})
        response.status_code = 500  # Internal Server Error

    return response


@subject_blueprint.route("/disciplina/media/creditos", methods=["GET"])
def get_average_credits_by_subject():
    try:
        data = db.session.query(func.avg(Disciplina.credito).label('avg')).filter(Disciplina.credito != -999)

        average = data[0].avg

        response_data = {"average_credits": eval(f"{average:.2f}")}
        response = make_response(response_data)
    
    except Exception as e:
        response = make_response({"error": str(e)})
        response.status_code = 500  # Internal Server Error

    return response


@subject_blueprint.route("/disciplina/media/carga_horaria", methods=["GET"])
def get_average_workload_by_subject():
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
@subject_blueprint.route("/aprovacao_disciplina/<int:id_disciplina>", methods=["GET"])
def get_approval_rate_disciplina(id_disciplina):
    try:
        count_aproved_students = Historico.query.filter(
            Historico.id_disciplina == id_disciplina,
            (Historico.status == 1) | (Historico.status == 2)
        ).count()

        count_reproved_students = Historico.query.filter(
            Historico.id_disciplina == id_disciplina,
            (Historico.status == 3) | (Historico.status == 4)
        ).count()

        total_students = count_aproved_students + count_reproved_students

        approval_rate = count_aproved_students/total_students

        response_data = {
            "id_disciplina": id_disciplina,
            "numero_de_aprovados" : count_aproved_students,
            "numero_de_reprovados" : count_reproved_students,
            "taxa de aprovacao": approval_rate
        }

        response = make_response(response_data)
        response.status_code = 200

    except Exception as e:
        response_data = {"error": str(e)}
        response = make_response(response_data)
        response.status_code = 500  # Internal Server Error

    return response

@subject_blueprint.route("/reprovacoes_disciplina/<id>", methods=["GET"])
def reprovacoes_disciplina(id):
    try:

        fails = Historico.query.filter(Historico.id_disciplina == id, (Historico.status == 3) | (Historico.status == 4)).count()
        
        response_data = {
            "Reprovações" : fails
        }

        response = make_response(response_data)
        response.status_code = 200

    except Exception as e:
        response = make_response({"error": str(e)})
        response.status_code = 500

    return response

@subject_blueprint.route("/distribuicao_disciplina/<id>", methods=["GET"])
def distribuicao_disciplina(id):
    try:
        
        subjects_count = Historico.query.filter(Historico.id_disciplina == id).count()

        subject_studied = Historico.query.filter(Historico.id_disciplina == id).all()
        
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

from flask import Blueprint, request, make_response
from models.Historico import Historico

from models.Disciplina import Disciplina
from models.Professor import Professor
from models.db import db
from models.Aluno import Aluno

regras_negocio_blueprint = Blueprint('regrasNegocio', __name__)

@regras_negocio_blueprint.route("/taxa_reprovacao/<int:id_disciplina>", methods=["GET"])
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


@regras_negocio_blueprint.route("/taxa_sucesso/<int:ano>", methods=["GET"])
def get_taxa_sucesso_ano(ano):
    try:
        query_aprovados = Historico.query.filter(
            Historico.ano == ano,
            (Historico.status == 1) | (Historico.status == 2)
        ).count()

        query_total_alunos = Historico.query.filter(
            Historico.ano == ano
        ).count()

        if query_total_alunos > 0:
            taxa_sucesso = (query_aprovados / query_total_alunos) * 100
        else:
            taxa_sucesso = 0

        response_data = {
            "ano": ano,
            "total_alunos": query_total_alunos,
            "aprovados": query_aprovados,
            "taxa_sucesso": taxa_sucesso
        }

        response = make_response(response_data)
        response.status_code = 200

    except Exception as e:
        response_data = {"error": str(e)}
        response = make_response(response_data)
        response.status_code = 500  # Internal Server Error

    return response


@regras_negocio_blueprint.route("/taxa_aprovacao_global", methods=["GET"])
def get_taxa_aprovacao_global():
    try:
        query_aprovados = Historico.query.filter(
            (Historico.status == 1) | (Historico.status == 2)
        ).count()

        query_total_alunos = Historico.query.count()

        if query_total_alunos > 0:
            taxa_aprovacao_global = (query_aprovados / query_total_alunos) * 100
        else:
            taxa_aprovacao_global = 0

        response_data = {
            "total_alunos": query_total_alunos,
            "aprovados": query_aprovados,
            "taxa_aprovacao_global": taxa_aprovacao_global
        }

        response = make_response(response_data)
        response.status_code = 200

    except Exception as e:
        response_data = {"error": str(e)}
        response = make_response(response_data)
        response.status_code = 500

    return response


@regras_negocio_blueprint.route("/taxa_retencao/<int:ano>", methods=["GET"])
def get_taxa_retencao(ano):
    try:
        # Contagem de alunos retidos
        query_retidos = Historico.query.filter(
            Historico.ano == ano,
            (Historico.status == 3) | (Historico.status == 4)
        ).count()

        query_total_alunos = Historico.query.filter(
            Historico.ano == ano
        ).count()

        if query_total_alunos > 0:
            taxa_retencao = (query_retidos / query_total_alunos) * 100
        else:
            taxa_retencao = 0

        response_data = {
            "ano": ano,
            "total_alunos": query_total_alunos,
            "retidos": query_retidos,
            "taxa_retencao": taxa_retencao
        }

        response = make_response(response_data)
        response.status_code = 200

    except Exception as e:
        response_data = {"error": str(e)}
        response = make_response(response_data)
        response.status_code = 500  # Internal Server Error

    return response


@regras_negocio_blueprint.route("/carga_horaria_total/<int:id_matricula>", methods=["GET"])
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


@regras_negocio_blueprint.route("/disciplinas_que_mais_reprovaram/<int:ano>/<int:semestre>", methods=["GET"])
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


@regras_negocio_blueprint.route("/alunos_matriculados", methods=["GET"])
def alunos_matriculados():
    try:
        alunos_matriculados = Aluno.query.join(
            Historico, Aluno.cpf == Historico.cpf_aluno
        ).filter(
            Historico.status == 1
        ).all()

        resultados = []
        for aluno in alunos_matriculados:
            resultado = {
                "cpf": aluno.cpf,
                "nome": aluno.nome,
                "arg_class": aluno.arg_class,
                "ano_entrada": aluno.ano_entrada,
            }
            resultados.append(resultado)

        response_data = {"resultados": resultados}
        response = make_response(response_data)
        response.status_code = 200

    except Exception as e:
        response_data = {"error": str(e)}
        response = make_response(response_data)
        response.status_code = 500  # Internal Server Error

    return response
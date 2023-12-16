from flask import Blueprint, request, make_response
from models.Historico import Historico


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
        # Contagem de alunos aprovados
        query_aprovados = Historico.query.filter(
            (Historico.status == 1) | (Historico.status == 2)
        ).count()

        # Contagem total de alunos
        query_total_alunos = Historico.query.count()

        # Calcular a taxa de aprovação global
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
        response.status_code = 500  # Internal Server Error

    return response


@regras_negocio_blueprint.route("/taxa_retencao/<int:ano>", methods=["GET"])
def get_taxa_retencao(ano):
    try:
        # Contagem de alunos retidos
        query_retidos = Historico.query.filter(
            Historico.ano == ano,
            (Historico.status == 3) | (Historico.status == 4)
        ).count()

        # Contagem total de alunos no ano
        query_total_alunos = Historico.query.filter(
            Historico.ano == ano
        ).count()

        # Calcular a taxa de retenção
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
from flask import Blueprint, request, make_response
from models.db import db
from models.Disciplina import Disciplina
from models.Historico import Historico

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


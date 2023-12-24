from flask import Blueprint, request, make_response
from models.db import db
from models.Historico import Historico
from models.Disciplina import Disciplina
from models.Aluno import Aluno
from exceptions.SubjectNotFoundException import SubjectNotFoundException

historic_blueprint = Blueprint('historico', __name__)


# listar historico escolar 
@historic_blueprint.route('/historico', methods=['GET'])
def list_all_historic():
    historicos = Historico.query.all()
    response = make_response([historico.to_json() for historico in historicos])
    return response


# listar historico escolar pelo id do aluno
@historic_blueprint.route('/historico/<string:cpf_aluno>', methods=['GET'])
def get_historic_by_cpf(cpf_aluno):
    try:
        resultados = []

        historicos = Historico.query.filter(Historico.cpf_aluno == cpf_aluno).all()

        for historico in historicos:
            resultado = {
                "id": historico.id,
                "cpf_aluno": historico.cpf_aluno,
                "id_disciplina": historico.id_disciplina,
                "status": historico.status,
                "ano": historico.ano,
                "semestre": historico.semestre,
                "nota": historico.nota,
                "nome_disciplina": Disciplina.query.get(historico.id_disciplina).nome,
            }

            resultados.append(resultado)

        response_data = {"historicos": resultados}
        response = make_response(response_data)
        response.status_code = 200

    except Exception as e:
        response_data = {"error": str(e)}
        response = make_response(response_data)
        response.status_code = 500  # Internal Server Error

    return response


@historic_blueprint.route('/historico/<int:id_aluno>/<int:id_disciplina>', methods=['GET'])
def get_historic_by_ids(id_aluno, id_disciplina):
    historicos = Historico.query.filter_by(id_aluno=id_aluno, id_disciplina=id_disciplina).all()

    if not historicos:
        response = make_response({'message': 'Histórico não encontrado'})
        response.status_code = 404
    else:
        response = make_response([historico.to_json() for historico in historicos])
        response.status_code = 200

    return response


@historic_blueprint.route("/alunos_matriculados", methods=["GET"])
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
        response = make_response({"error": str(e)})
        response.status_code = 500  # Internal Server Error

    return response


@historic_blueprint.route("/taxa_retencao/<int:ano>", methods=["GET"])
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
        response = make_response({"error": str(e)})
        response.status_code = 500  # Internal Server Error

    return response


@historic_blueprint.route("/taxa_aprovacao_global", methods=["GET"])
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
        response = make_response({"error": str(e)})
        response.status_code = 500

    return response


@historic_blueprint.route("/taxa_sucesso/<int:ano>", methods=["GET"])
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
        response = make_response({"error": str(e)})
        response.status_code = 500  # Internal Server Error

    return response


@historic_blueprint.route("/taxa_desistencia/<int:subject_id>", methods=["GET"])
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


@historic_blueprint.route('/historico/subjects_by_student', methods=["GET"])
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

@historic_blueprint.route('/historico', methods=['POST'])
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
            raise Exception()

        historic.cpf_aluno = request.json.get("cpf_aluno")
        historic.id_disciplina = request.json.get("id_disciplina")
        historic.status = request.json.get("status")
        historic.ano = request.json.get("ano")
        historic.semestre = request.json.get("semestre")
        historic.nota = request.json.get("nota")

        db.session.commit()

        response = make_response({"message": f"Historic with id {id} updated successfully"})

    except Exception as e:
        response = make_response({"error": str(e)})
        response.status_code = 500

    return response


@historic_blueprint.route('/historico/<int:id>', methods=["DELETE"])
def delete_historic(id):
    try:
        historic = Historico.query.get(id)

        if not historic:
            pass

        db.session.delete(historic)
        db.session.commit()

        response = make_response({"message": f"Historic with {id} deleted successfully"})

    except Exception as e:
        response = make_response({"error": str(e)})
        response.status_code = 500  # Internal Server Error

    return response
import pytest
from unittest.mock import MagicMock, patch
from flask import Flask, make_response
from models.Professor import Professor
from models.Disciplina import Disciplina
from models.Historico import Historico
from routes.student_blueprint import student_blueprint
from models.Aluno import Aluno
from sqlalchemy import func



def test_create_student():
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.register_blueprint(student_blueprint)  # Register the blueprint
    client = app.test_client()

    with app.app_context():
        with patch('models.Aluno.Aluno.query') as mock_query, patch('models.db.db.session') as mock_session:
            mock_new_student = MagicMock()
            mock_new_student.to_json.return_value = {"cpf": "111.757.432-57", "nome": "Test Student", "ano_entrada": 2022, "arg_class": None}
            mock_query.get.return_value = None

            mock_session.add.return_value = None
            mock_session.commit.return_value = None

            response = client.post('/students', json={"cpf": "111.757.432-57", "nome": "Test Student", "ano_entrada": 2022})

    assert response.status_code == 201
    assert response.get_json() == {"created_student": {"cpf": "111.757.432-57", "nome": "Test Student", "ano_entrada": 2022, "arg_class": None}}


def test_list_students():
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.register_blueprint(student_blueprint)  # Register the blueprint
    client = app.test_client()

    with app.app_context():
        with patch('models.Aluno.Aluno.query') as mock_query:
            mock_student = MagicMock()
            mock_student.to_json.return_value = {"cpf": "111.757.432-57", "nome": "Test Student", "ano_entrada": 2022}
            mock_query.all.return_value = [mock_student]

            response = client.get('/students')

    assert response.status_code == 200
    assert response.get_json() == [{"cpf": "111.757.432-57", "nome": "Test Student", "ano_entrada": 2022}]


def test_get_student_by_cpf():
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.register_blueprint(student_blueprint)  # Register the blueprint
    client = app.test_client()

    with app.app_context():
        with patch('models.Aluno.Aluno.query') as mock_query:
            mock_student = MagicMock()
            mock_student.to_json.return_value = {"cpf": "111.757.432-57", "nome": "Test Student", "ano_entrada": 2022}
            mock_query.get.return_value = mock_student

            response = client.get('/students/111.757.432-57')

    assert response.status_code == 200
    assert response.get_json() == {"cpf": "111.757.432-57", "nome": "Test Student", "ano_entrada": 2022}


def test_update_student():
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.register_blueprint(student_blueprint)  # Register the blueprint
    client = app.test_client()

    with app.app_context():
        with patch('models.Aluno.Aluno.query') as mock_query, patch('models.db.db.session') as mock_session:
            mock_student = MagicMock()
            mock_student.to_json.return_value = {"cpf": "111.757.432-57", "nome": "Updated Student", "ano_entrada": 2022, "arg_class": None}
            mock_query.get.return_value = mock_student

            mock_session.commit.return_value = None

            response = client.put('/students/111.757.432-57', json={"nome": "Updated Student", "ano_entrada": 2022})

    assert response.status_code == 200
    assert response.get_json() == {"updated_student": {"cpf": "111.757.432-57", "nome": "Updated Student", "ano_entrada": 2022, "arg_class": None}}


def test_delete_aluno_por_cpf():
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.register_blueprint(student_blueprint)  # Register the blueprint
    client = app.test_client()

    with app.app_context():
        with patch('models.Aluno.Aluno.query') as mock_query, patch('models.db.db.session') as mock_session:
            mock_student = MagicMock()
            mock_student.to_json.return_value = {"cpf": "111.757.432-57", "nome": "Test Student", "ano_entrada": 2022, "arg_class": None}
            mock_query.get.return_value = mock_student

            mock_session.delete.return_value = None
            mock_session.commit.return_value = None

            response = client.delete('/students/111.757.432-57')

    assert response.status_code == 200
    assert response.get_json() == {"deleted_student": {"cpf": "111.757.432-57", "nome": "Test Student", "ano_entrada": 2022, "arg_class": None}}



def test_get_credits_rate():
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.register_blueprint(student_blueprint)  # Register the blueprint
    client = app.test_client()

    with app.app_context():
        with patch('models.Aluno.Aluno.query') as mock_query_aluno, patch('models.Historico.Historico.query') as mock_query_historico, patch('models.Disciplina.Disciplina.query') as mock_query_disciplina:
            mock_student = MagicMock()
            mock_student.cpf = "111.757.432-57"
            mock_query_aluno.filter.return_value.first.return_value = mock_student

            mock_historico = MagicMock()
            mock_query_historico.filter.return_value.all.return_value = [mock_historico]

            mock_disciplina = MagicMock()
            mock_disciplina.credito = 5
            mock_query_disciplina.filter.return_value.first.return_value = mock_disciplina
            mock_query_disciplina.all.return_value = [mock_disciplina, mock_disciplina]

            response = client.get('/students/credit/111.757.432-57')

    assert response.status_code == 200
    assert response.get_json() == {
        "used_credits": 5,
        "unused_credits": 5,
        "credit_utilization_rate": 1.0
    }


def test_performance():
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.register_blueprint(student_blueprint)  # Register the blueprint
    client = app.test_client()

    with app.app_context():
        with patch('models.Aluno.Aluno.query') as mock_query_aluno, patch('models.Historico.Historico.query') as mock_query_historico:
            mock_student_enem = MagicMock()
            mock_student_enem.arg_class = 101
            mock_student_enem.cpf = "111.757.432-57"

            mock_student_ssa = MagicMock()
            mock_student_ssa.arg_class = 99
            mock_student_ssa.cpf = "111.757.432-58"

            mock_query_aluno.all.return_value = [mock_student_enem, mock_student_ssa]

            mock_query_historico.filter.return_value.count.return_value = 5

            response = client.get('/students/performance')

    assert response.status_code == 200
    assert response.get_json() == {
        "Enem": 1,
        "SSA": 1,
        "Number of approvals in subjects by student that entered through Enem": 5,
        "Number of approvals in subjects by student that entered through Enem": 5,
        "SSA_utilization_rate": 5.0,
        "Enem_utilization_rate": 5.0
    }


# def test_get_how_many_electives():
#     app = Flask(__name__)
#     app.config['TESTING'] = True
#     app.register_blueprint(student_blueprint)  # Register the blueprint
#     client = app.test_client()
#
#     with app.app_context():
#         with patch('models.Aluno.Aluno.query') as mock_query_aluno, patch('models.Disciplina.Disciplina.query') as mock_query_disciplina, patch('models.db.db.session') as mock_session:
#             mock_student = MagicMock()
#             mock_student.cpf = "111.757.432-57"
#             mock_student.to_json.return_value = {"cpf": "111.757.432-57", "nome": "Test Student", "ano_entrada": 2022, "arg_class": None}
#             mock_query_aluno.get.return_value = mock_student
#
#             mock_disciplina = MagicMock()
#             mock_disciplina.to_json.return_value = {"id": 1, "nome": "Test Discipline", "tipo": 2}
#             mock_query_disciplina.join.return_value.filter.return_value.all.return_value = [mock_disciplina]
#
#             response = client.get('/students/subjects/electives/111.757.432-57')
#
#     assert response.status_code == 200
#     assert response.get_json() == {
#         "cpf": "111.757.432-57",
#         "nome": "Test Student",
#         "ano_entrada": 2022,
#         "arg_class": None,
#         "subjects": [{"id": 1, "nome": "Test Discipline", "tipo": 2}]
#     }


# def test_get_how_many_mandatory():
#     app = Flask(__name__)
#     app.config['TESTING'] = True
#     app.register_blueprint(student_blueprint)  # Register the blueprint
#     client = app.test_client()
#
#     with app.app_context():
#         with patch('models.Aluno.Aluno.query') as mock_query_aluno, patch('models.Disciplina.Disciplina.query') as mock_query_disciplina, patch('models.db.db.session') as mock_session:
#             mock_student = MagicMock()
#             mock_student.cpf = "111.757.432-57"
#             mock_student.to_json.return_value = {"cpf": "111.757.432-57", "nome": "Test Student", "ano_entrada": 2022, "arg_class": None}
#             mock_query_aluno.get.return_value = mock_student
#
#             mock_disciplina = MagicMock()
#             mock_disciplina.to_json.return_value = {"id": 1, "nome": "Test Discipline", "tipo": 1}
#             mock_query_disciplina.join.return_value.filter.return_value.all.return_value = [mock_disciplina]
#
#             response = client.get('/students/subjects/mandatory/111.757.432-57')
#
#     assert response.status_code == 200
#     assert response.get_json() == {
#         "cpf": "111.757.432-57",
#         "nome": "Test Student",
#         "ano_entrada": 2022,
#         "arg_class": None,
#         "subjects": [{"id": 1, "nome": "Test Discipline", "tipo": 1}]
#     }

#
# def test_get_overall_academic_performance():
#     app = Flask(__name__)
#     app.config['TESTING'] = True
#     app.register_blueprint(student_blueprint)  # Register the blueprint
#     client = app.test_client()
#
#     with app.app_context():
#         with patch('models.Historico.Historico.query') as mock_query_historico, \
#                 patch('models.db.db.session.commit') as mock_session, \
#                 patch('sqlalchemy.func', return_value=80) as mock_func:
#             mock_query_historico.filter.return_value.all.return_value = [mock_func]
#
#             response = client.get('/students/performance/overall')
#
#     assert response.status_code == 200
#     assert response.get_json() == {"overall_academic_performance": "80.00%"}


def test_get_student_conclusion_rate():
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.register_blueprint(student_blueprint)  # Register the blueprint
    client = app.test_client()

    with app.app_context():
        with patch('models.Aluno.Aluno.query') as mock_query_aluno, patch('models.Historico.Historico.query') as mock_query_historico:
            mock_student = MagicMock()
            mock_student.cpf = "111.757.432-57"
            mock_query_aluno.filter.return_value.first.return_value = mock_student

            mock_query_historico.filter.return_value.count.return_value = 40

            response = client.get('/students/conclusion_rate/111.757.432-57')

    assert response.status_code == 200
    assert response.get_json() == {
        "Approved subjects": 40,
        "Conclusion rate": 0.8
    }


def test_get_student_fails():
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.register_blueprint(student_blueprint)  # Register the blueprint
    client = app.test_client()

    with app.app_context():
        with patch('models.Aluno.Aluno.query') as mock_query_aluno, patch('models.Historico.Historico.query') as mock_query_historico:
            mock_student = MagicMock()
            mock_student.cpf = "111.757.432-57"
            mock_query_aluno.filter.return_value.first.return_value = mock_student

            mock_query_historico.filter.return_value.count.return_value = 15

            response = client.get('/students/fails/111.757.432-57')

    assert response.status_code == 200
    assert response.get_json() == {
        "Fails": 15
    }


def test_get_average_grade():
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.register_blueprint(student_blueprint)  # Register the blueprint
    client = app.test_client()

    with app.app_context():
        with patch('models.Disciplina.Disciplina.query') as mock_query_disciplina, patch('models.Historico.Historico.query') as mock_query_historico:
            mock_subject = MagicMock()
            mock_subject.id = 1
            mock_subject.nome = "Test Subject"
            mock_query_disciplina.all.return_value = [mock_subject]

            mock_historic = MagicMock()
            mock_historic.nota = 8
            mock_query_historico.filter.return_value.all.return_value = [mock_historic, mock_historic]

            response = client.get('/students/average/grade')

    assert response.status_code == 200
    assert response.get_json() == [{
        "Subject:": "Test Subject",
        "Total number of students in the subject": 2,
        "Average:": 8.0
    }]


def test_get_student_approved_subjects():
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.register_blueprint(student_blueprint)  # Register the blueprint
    client = app.test_client()

    with app.app_context():
        with patch('models.Aluno.Aluno.query') as mock_query_aluno, patch('models.Disciplina.Disciplina.query') as mock_query_disciplina, patch('models.Historico.Historico.query') as mock_query_historico:
            mock_student = MagicMock()
            mock_student.cpf = "111.757.432-57"
            mock_query_aluno.get.return_value = mock_student

            mock_subject = MagicMock()
            mock_subject.nome = "Test Subject"
            mock_query_disciplina.all.return_value = [mock_subject]

            mock_historic = MagicMock()
            mock_query_historico.filter.return_value.first.return_value = mock_historic

            response = client.get('/students/approved/111.757.432-57')

    assert response.status_code == 200
    assert response.get_json() == ["Test Subject"]


# def test_get_student_grade_distribution():
#     app = Flask(__name__)
#     app.config['TESTING'] = True
#     app.register_blueprint(student_blueprint)  # Register the blueprint
#     client = app.test_client()
#
#     with app.app_context():
#         with patch('models.Aluno.Aluno.query') as mock_query_aluno, patch('models.Historico.Historico.query') as mock_query_historico:
#             mock_student = MagicMock()
#             mock_student.cpf = "111.757.432-57"
#             mock_query_aluno.filter.return_value.first.return_value = mock_student
#
#             mock_historic = MagicMock()
#             mock_historic.nota = 8
#             mock_query_historico.filter.return_value.count.return_value = 2
#             mock_query_historico.filter.return_value.all.return_value = [mock_historic, mock_historic]
#
#             response = client.get('/students/grade/distribution/111.757.432-57')
#
#     assert response.status_code == 200
#     assert response.get_json() == {
#         "Grade distribution": 8.0
#     }
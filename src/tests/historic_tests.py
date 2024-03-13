from unittest.mock import MagicMock, patch
from flask import Flask
from models.Historico import Historico
from models.Disciplina import Disciplina
from models.Aluno import Aluno
from routes.historic_blueprint import historic_blueprint


def test_list_all_historic():
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.register_blueprint(historic_blueprint)  # Register the blueprint
    client = app.test_client()

    with app.app_context():
        with patch('models.db.db.session.query') as mock_query:
            mock_historic = MagicMock(spec=Historico)
            mock_historic.to_json.return_value = {"id": 1, "cpf_aluno": "12345678901", "id_disciplina": 1, "status": 1, "ano": 2022, "semestre": 1, "nota": 10.0}
            mock_query.return_value.all.return_value = [mock_historic]

            # Fazer uma solicitação GET para o endpoint '/historic'
            response = client.get('/historic')

    assert response.status_code == 200
    assert response.get_json() == [{"id": 1, "cpf_aluno": "12345678901", "id_disciplina": 1, "status": 1, "ano": 2022, "semestre": 1, "nota": 10.0}]


def test_get_history_by_cpf():
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.register_blueprint(historic_blueprint)  # Register the blueprint
    client = app.test_client()

    with app.app_context():
        with patch('models.Historico.Historico.query') as mock_query_historico, patch('models.Disciplina.Disciplina.query') as mock_query_disciplina:
            mock_historic = MagicMock(spec=Historico)
            mock_historic.id = 1
            mock_historic.cpf_aluno = '12345678901'
            mock_historic.id_disciplina = 1
            mock_historic.status = 1
            mock_historic.ano = 2022
            mock_historic.semestre = 1
            mock_historic.nota = 10.0
            mock_query_historico.filter.return_value.all.return_value = [mock_historic]

            mock_disciplina = MagicMock(spec=Disciplina)
            mock_disciplina.nome = 'Test Discipline'
            mock_query_disciplina.get.return_value = mock_disciplina

            # Fazer uma solicitação GET para o endpoint '/historic/get_historic_by_cpf/12345678901'
            response = client.get('/historic/get_historic_by_cpf/12345678901')

    assert response.status_code == 200
    assert response.get_json() == {
        "histories": [
            {
                "id": 1,
                "student_cpf": '12345678901',
                "discipline_id": 1,
                "status": 1,
                "year": 2022,
                "semester": 1,
                "grade": 10.0,
                "discipline_name": 'Test Discipline'
            }
        ]
    }


def test_get_historic_by_ids():
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.register_blueprint(historic_blueprint)  # Register the blueprint
    client = app.test_client()

    with app.app_context():
        with patch('models.Aluno.Aluno.query') as mock_query_aluno, patch('models.Disciplina.Disciplina.query') as mock_query_disciplina, patch('models.Historico.Historico.query') as mock_query_historico:
            mock_aluno = MagicMock(spec=Aluno)
            mock_aluno.cpf = '12345678901'
            mock_query_aluno.get.return_value = mock_aluno

            mock_disciplina = MagicMock(spec=Disciplina)
            mock_disciplina.id = 1
            mock_query_disciplina.get.return_value = mock_disciplina

            mock_historic = MagicMock(spec=Historico)
            mock_historic.to_json.return_value = {"id": 1, "cpf_aluno": "12345678901", "id_disciplina": 1, "status": 1, "ano": 2022, "semestre": 1, "nota": 10.0}
            mock_query_historico.filter.return_value.all.return_value = [mock_historic]

            # Fazer uma solicitação GET para o endpoint '/historic/get_historic_by_ids/12345678901/1'
            response = client.get('/historic/get_historic_by_ids/12345678901/1')

    assert response.status_code == 200
    assert response.get_json() == [{"id": 1, "cpf_aluno": "12345678901", "id_disciplina": 1, "status": 1, "ano": 2022, "semestre": 1, "nota": 10.0}]


def test_enrolled_students():
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.register_blueprint(historic_blueprint)  # Register the blueprint
    client = app.test_client()

    with app.app_context():
        with patch('models.Aluno.Aluno.query') as mock_query_aluno, patch('models.Historico.Historico') as mock_historico:
            mock_aluno = MagicMock(spec=Aluno)
            mock_aluno.cpf = '12345678901'
            mock_aluno.nome = 'Test Student'
            mock_aluno.arg_class = 'Test Class'
            mock_aluno.ano_entrada = 2022
            mock_query_aluno.join.return_value.filter.return_value.all.return_value = [mock_aluno]

            mock_historico.cpf_aluno = '12345678901'
            mock_historico.status = 1

            # Fazer uma solicitação GET para o endpoint '/historic/enrolled_students'
            response = client.get('/historic/enrolled_students')

    assert response.status_code == 200
    assert response.get_json() == {
        "results": [
            {
                "cpf": '12345678901',
                "nome": 'Test Student',
                "arg_class": 'Test Class',
                "ano_entrada": 2022
            }
        ]
    }


def test_get_retention_rate():
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.register_blueprint(historic_blueprint)  # Register the blueprint
    client = app.test_client()

    with app.app_context():
        with patch('models.Historico.Historico.query') as mock_query_historico:
            mock_query_historico.filter.return_value.count.return_value = 10
            mock_query_historico.filter.return_value.filter.return_value.count.return_value = 5

            # Fazer uma solicitação GET para o endpoint '/historic/get_retention_rate/2022'
            response = client.get('/historic/get_retention_rate/2022')

    assert response.status_code == 200
    assert response.get_json() == {
        "year": 2022,
        "total_students": 10,
        "retained": 10,
        "retention_rate": 100.0
    }


def test_get_global_approval_rate():
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.register_blueprint(historic_blueprint)  # Register the blueprint
    client = app.test_client()

    with app.app_context():
        with patch('models.Historico.Historico.query') as mock_query:
            mock_query1 = MagicMock()
            mock_query1.count.return_value = 50  # approved students
            mock_query2 = MagicMock()
            mock_query2.count.return_value = 100  # total students
            mock_query.filter.return_value = mock_query1  # One call to filter
            mock_query.count.return_value = 100  # total students

            response = client.get('/historic/get_global_approval_rate')

    assert response.status_code == 200
    assert response.get_json() == {
        "total_students": 100,
        "approved": 50,
        "global_approval_rate": 50.0,
    }


def test_get_success_rate_year():
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.register_blueprint(historic_blueprint)  # Register the blueprint
    client = app.test_client()

    with app.app_context():
        with patch('models.Historico.Historico.query') as mock_query:
            mock_query1 = MagicMock()
            mock_query1.count.return_value = 50  # approved students
            mock_query2 = MagicMock()
            mock_query2.count.return_value = 100  # total students
            mock_query.filter.side_effect = [mock_query1, mock_query2]  # Two calls to filter

            year = 2022
            response = client.get(f'/historic/get_success_rate_year/{year}')

    assert response.status_code == 200
    assert response.get_json() == {
        "year": year,
        "total_students": 100,
        "approved": 50,
        "success_rate": 50.0,
    }


def test_get_abandonment_by_subject():
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.register_blueprint(historic_blueprint)  # Register the blueprint
    client = app.test_client()

    with app.app_context():
        with patch('models.Historico.Historico.query') as mock_query_historico, patch('models.Disciplina.Disciplina.query') as mock_query_disciplina:
            mock_query_disciplina.filter.return_value.first.return_value = MagicMock()  # Mock subject

            mock_query1 = MagicMock()
            mock_query1.count.return_value = 20  # total abandonment
            mock_query2 = MagicMock()
            mock_query2.count.return_value = 100  # total students
            mock_query_historico.filter.side_effect = [mock_query1, mock_query2]  # Two calls to filter

            subject_id = 1
            response = client.get(f'/historic/get_abandonment_by_subject/{subject_id}')

    assert response.status_code == 200
    assert response.get_json() == {
        "total_abandonment": 20,
        "total": 100,
        "abandonment_rate": 20.0,
    }


def test_subjects_by_student():
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.register_blueprint(historic_blueprint)  # Register the blueprint
    client = app.test_client()

    with app.app_context():
        with patch('models.Disciplina.Disciplina.query') as mock_query_disciplina, patch('models.db.db.session.query') as mock_query_session, patch('models.Historico.Historico'):
            mock_query_disciplina.count.return_value = 100  # total subjects

            mock_student = MagicMock()
            mock_student.cpf = '12345678901'
            mock_student.nome = 'Test Student'
            mock_student.ano_entrada = 2022
            mock_student.total_cursadas = 50
            mock_query_session.return_value.join.return_value.filter.return_value.group_by.return_value.all.return_value = [mock_student]  # Mock students

            response = client.get('/historic/subjects_by_student')

    assert response.status_code == 200
    assert response.get_json() == {
        "average": 50.0,
        "average_percentage": "50.00%"
    }


def test_create_historic():
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.register_blueprint(historic_blueprint)  # Register the blueprint
    client = app.test_client()

    with app.app_context():
        with patch('models.Historico.Historico') as mock_historico, patch('models.db.db.session') as mock_session:
            mock_new_historic = MagicMock()
            mock_new_historic.to_json.return_value = {"id": None, "cpf_aluno": "111.757.432-57", "id_disciplina": 1, "status": 1, "ano": 2016, "semestre": 1, "nota": 8}
            mock_historico.return_value = mock_new_historic

            mock_session.add.return_value = None
            mock_session.commit.return_value = None

            response = client.post('/historic', json={"cpf_aluno": "111.757.432-57", "id_disciplina": 1, "status": 1, "ano": 2016, "semestre": 1, "nota": 8})

    assert response.status_code == 201
    assert response.get_json() == {"created_historic": {"id": None, "cpf_aluno": "111.757.432-57", "id_disciplina": 1, "status": 1, "ano": 2016, "semestre": 1, "nota": 8}}


def test_update_historic():
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.register_blueprint(historic_blueprint)  # Register the blueprint
    client = app.test_client()

    with app.app_context():
        with patch('models.Historico.Historico.query') as mock_query, patch('models.db.db.session.commit'):
            mock_historic = MagicMock()
            mock_historic.to_json.return_value = {"id": 1, "cpf_aluno": "111.757.432-57", "id_disciplina": 1, "status": 1, "ano": 2016, "semestre": 1, "nota": 8}
            mock_query.get.return_value = mock_historic

            response = client.put('/historic/1', json={"cpf_aluno": "111.757.432-57", "id_disciplina": 1, "status": 1, "ano": 2016, "semestre": 1, "nota": 8})

    assert response.status_code == 200
    assert response.get_json() == {"updated_historic": {"id": 1, "cpf_aluno": "111.757.432-57", "id_disciplina": 1, "status": 1, "ano": 2016, "semestre": 1, "nota": 8}}


def test_delete_historic():
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.register_blueprint(historic_blueprint)  # Register the blueprint
    client = app.test_client()

    with app.app_context():
        with patch('models.Historico.Historico.query') as mock_query, patch('models.db.db.session') as mock_session:
            mock_historic = MagicMock()
            mock_historic.to_json.return_value = {"id": 1, "cpf_aluno": "111.757.432-57", "id_disciplina": 1, "status": 1, "ano": 2016, "semestre": 1, "nota": 8}
            mock_query.get.return_value = mock_historic

            mock_session.delete.return_value = None
            mock_session.commit.return_value = None

            response = client.delete('/historic/1')

    assert response.status_code == 200
    assert response.get_json() == {"deleted_historic": {"id": 1, "cpf_aluno": "111.757.432-57", "id_disciplina": 1, "status": 1, "ano": 2016, "semestre": 1, "nota": 8}}

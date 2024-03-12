import pytest
from unittest.mock import MagicMock, patch
from flask import Flask, make_response
from models.Professor import Professor
from models.Disciplina import Disciplina
from models.Historico import Historico
from routes.professor_blueprint import professor_blueprint  # Import the blueprint
from models.db import db

def test_list_professors():
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.register_blueprint(professor_blueprint)  # Register the blueprint
    client = app.test_client()

    with app.app_context():
        with patch('models.Professor.Professor.query') as mock_query:
            mock_professor = MagicMock(spec=Professor)
            mock_professor.matricula = '1234'
            mock_professor.nome = 'Test Professor'
            mock_professor.cpf = '12345678901'
            mock_query.all.return_value = [mock_professor]

            response = client.get('/professors')

    assert response.status_code == 200
    assert response.get_json() == {'professors': [{'registration': '1234', 'name': 'Test Professor', 'cpf': '12345678901'}]}


def test_find_professor_by_cpf():
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.register_blueprint(professor_blueprint)  # Register the blueprint
    client = app.test_client()

    with app.app_context():
        with patch('models.Professor.Professor.query') as mock_query:
            mock_professor = MagicMock(spec=Professor)
            mock_professor.matricula = '1234'
            mock_professor.nome = 'Test Professor'
            mock_professor.cpf = '12345678901'
            mock_query.filter.return_value.first.return_value = mock_professor

            response = client.get('/professors/12345678901')

    assert response.status_code == 200
    assert response.get_json() == {'professor': {'registration': '1234', 'name': 'Test Professor', 'cpf': '12345678901'}}


def test_update_professor_by_cpf():
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.register_blueprint(professor_blueprint)  # Register the blueprint
    client = app.test_client()

    with app.app_context():
        with patch('models.Professor.Professor.query') as mock_query:
            mock_professor = MagicMock(spec=Professor)
            mock_professor.matricula = '1234'
            mock_professor.nome = 'Test Professor'
            mock_professor.cpf = '12345678901'
            mock_query.filter.return_value.first.return_value = mock_professor

            # Fazer uma solicitação PUT para o endpoint '/professors/12345678901' com o novo nome
            response = client.put('/professors/12345678901', json={'name': 'Updated Professor'})

    assert response.status_code == 200
    assert response.get_json() == {'updated_professor': {'registration': '1234', 'name': 'Updated Professor', 'cpf': '12345678901'}}



def test_delete_professor_by_cpf():
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.register_blueprint(professor_blueprint)  # Register the blueprint
    client = app.test_client()

    with app.app_context():
        with patch('models.Professor.Professor.query') as mock_query:
            mock_professor = MagicMock(spec=Professor)
            mock_professor.matricula = '1234'
            mock_professor.nome = 'Test Professor'
            mock_professor.cpf = '12345678901'
            mock_query.filter.return_value.first.return_value = mock_professor

            # Mock the delete method of db.session
            db.session.delete = MagicMock()

            # Fazer uma solicitação DELETE para o endpoint '/professors/12345678901'
            response = client.delete('/professors/12345678901')

    assert response.status_code == 200
    assert response.get_json() == {'deleted_professor': {'registration': '1234', 'name': 'Test Professor', 'cpf': '12345678901'}}


def test_create_professor():
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.register_blueprint(professor_blueprint)  # Register the blueprint
    client = app.test_client()

    with app.app_context():
        with patch('models.Professor.Professor.query') as mock_query, patch('models.db.db.session.add'), patch('models.db.db.session.commit'):
            mock_query.filter.return_value.first.return_value = None

            new_professor_data = {
                "matricula": "1234",
                "cpf": "12345678901",
                "nome": "Test Professor"
            }

            # Fazer uma solicitação POST para o endpoint '/professors' com os dados do novo professor
            response = client.post('/professors', json=new_professor_data)

    assert response.status_code == 201
    assert response.get_json() == {'created_professor': {'registration': '1234', 'cpf': '12345678901', 'name': 'Test Professor'}}


def test_total_workload_professor():
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.register_blueprint(professor_blueprint)  # Register the blueprint
    client = app.test_client()

    with app.app_context():
        with patch('models.db.db.session.query') as mock_query:
            mock_query.return_value.join.return_value.filter.return_value.scalar.return_value = 10

            # Fazer uma solicitação GET para o endpoint '/professors/1234/total_workload'
            response = client.get('/professors/1234/total_workload')

    assert response.status_code == 200
    assert response.get_json() == {'professor_id': 1234, 'total_workload': 10}


def test_professor_performance_rate():
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.register_blueprint(professor_blueprint)  # Register the blueprint
    client = app.test_client()

    with app.app_context():
        with patch('models.Professor.Professor.query') as mock_query_professor, patch('models.Disciplina.Disciplina.query') as mock_query_disciplina, patch('models.Historico.Historico.query') as mock_query_historico:
            mock_professor = MagicMock(spec=Professor)
            mock_professor.matricula = '1234'
            mock_professor.nome = 'Test Professor'
            mock_professor.cpf = '12345678901'
            mock_query_professor.filter.return_value.first.return_value = mock_professor

            mock_disciplina = MagicMock(spec=Disciplina)
            mock_disciplina.id = 1
            mock_disciplina.nome = 'Test Discipline'
            mock_query_disciplina.filter.return_value.all.return_value = [mock_disciplina]

            mock_query_historico.filter.return_value.count.return_value = 10

            # Fazer uma solicitação GET para o endpoint '/professors/12345678901/performance_rate'
            response = client.get('/professors/12345678901/performance_rate')

    assert response.status_code == 200


def test_professor_evaluation():
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.register_blueprint(professor_blueprint)  # Register the blueprint
    client = app.test_client()

    with app.app_context():
        with patch('models.Professor.Professor.query') as mock_query_professor, patch('models.Disciplina.Disciplina.query') as mock_query_disciplina, patch('models.Historico.Historico.query') as mock_query_historico:
            mock_professor = MagicMock(spec=Professor)
            mock_professor.matricula = '1234'
            mock_professor.nome = 'Test Professor'
            mock_professor.cpf = '12345678901'
            mock_query_professor.filter.return_value.first.return_value = mock_professor

            mock_disciplina1 = MagicMock(spec=Disciplina)
            mock_disciplina1.id = 1
            mock_disciplina1.nome = 'Test Discipline 1'

            mock_disciplina2 = MagicMock(spec=Disciplina)
            mock_disciplina2.id = 2
            mock_disciplina2.nome = 'Test Discipline 2'

            mock_query_disciplina.filter.return_value.all.return_value = [mock_disciplina1, mock_disciplina2]

            mock_query_historico.filter.return_value.count.side_effect = [10, 0, 10, 10]  # 10 approved, 0 reproved for discipline 1 and 10 approved, 10 reproved for discipline 2

            # Fazer uma solicitação GET para o endpoint '/professors/12345678901/evaluation'
            response = client.get('/professors/12345678901/evaluation')

    assert response.status_code == 200
    assert response.get_json() == {'professor': {'registration': '1234', 'name': 'Test Professor', 'cpf': '12345678901', 'evaluation': 8}}


def test_get_average_subjects_by_professor():
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.register_blueprint(professor_blueprint)  # Register the blueprint
    client = app.test_client()

    with app.app_context():
        with patch('models.db.db.session.query') as mock_query, patch('models.Professor.Professor.query') as mock_query_professor:
            mock_professor = MagicMock(spec=Professor)
            mock_professor.matricula = '1234'
            mock_professor.nome = 'Test Professor'
            mock_professor.cpf = '12345678901'
            mock_professor.total_subjects = 2
            mock_query_professor.all.return_value = [mock_professor]

            mock_query.return_value.join.return_value.group_by.return_value.all.return_value = [mock_professor]

            # Fazer uma solicitação GET para o endpoint '/professors/average_subjects'
            response = client.get('/professors/average_subjects')

    assert response.status_code == 200
    assert response.get_json() == {'average_subjects_by_professor': 2.0}


def test_get_professor_subjects():
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.register_blueprint(professor_blueprint)  # Register the blueprint
    client = app.test_client()

    with app.app_context():
        with patch('models.Professor.Professor.query') as mock_query_professor, patch('models.Disciplina.Disciplina.query') as mock_query_disciplina:
            mock_professor = MagicMock(spec=Professor)
            mock_professor.matricula = '1234'
            mock_professor.nome = 'Test Professor'
            mock_professor.cpf = '12345678901'
            mock_query_professor.filter.return_value.first.return_value = mock_professor

            mock_disciplina = MagicMock(spec=Disciplina)
            mock_disciplina.id = 1
            mock_disciplina.nome = 'Test Discipline'
            mock_disciplina.to_json.return_value = {"id": 1, "name": "Test Discipline"}
            mock_query_disciplina.filter.return_value.all.return_value = [mock_disciplina]

            # Fazer uma solicitação GET para o endpoint '/professors/12345678901/subjects'
            response = client.get('/professors/12345678901/subjects')

    assert response.status_code == 200
    assert response.get_json() == {
        "professor_registration": '1234',
        "professor_name": 'Test Professor',
        "subjects": [{"id": 1, "name": "Test Discipline"}]
    }


def test_get_non_existent_professor():
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.register_blueprint(professor_blueprint)
    client = app.test_client()

    with app.app_context():
        with patch('models.Professor.Professor.query') as mock_query:
            mock_query.filter.return_value.first.return_value = None

            response = client.get('/professors/99999999999')

    assert response.status_code == 404


def test_update_non_existent_professor():
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.register_blueprint(professor_blueprint)
    client = app.test_client()

    with app.app_context():
        with patch('models.Professor.Professor.query') as mock_query:
            mock_query.filter.return_value.first.return_value = None

            response = client.put('/professors/99999999999', json={'name': 'Updated Professor'})

    assert response.status_code == 404


def test_delete_non_existent_professor():
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.register_blueprint(professor_blueprint)
    client = app.test_client()

    with app.app_context():
        with patch('models.Professor.Professor.query') as mock_query:
            mock_query.filter.return_value.first.return_value = None

            response = client.delete('/professors/99999999999')

    assert response.status_code == 404


def test_create_professor_with_invalid_data():
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.register_blueprint(professor_blueprint)
    client = app.test_client()

    with app.app_context():
        with patch('models.Professor.Professor.query') as mock_query, patch('models.db.db.session.add'), patch('models.db.db.session.commit'):
            mock_query.filter.return_value.first.return_value = None

            new_professor_data = {
                "matricula": "1234",
                "cpf": "12345678901",
                "nome": ""
            }

            response = client.post('/professors', json=new_professor_data)

    assert response.status_code == 201
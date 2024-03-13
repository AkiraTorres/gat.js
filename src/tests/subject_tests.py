from unittest.mock import MagicMock, patch
from flask import Flask
from routes.subject_blueprint import subject_blueprint


def test_list_subjects():
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.register_blueprint(subject_blueprint)  # Register the blueprint
    client = app.test_client()

    with app.app_context():
        with patch('models.Disciplina.Disciplina.query') as mock_query_disciplina:
            mock_subject = MagicMock()
            mock_subject.to_json.return_value = {"id": 1, "name": "Test Subject"}
            mock_query_disciplina.all.return_value = [mock_subject]

            response = client.get('/subjects')

    assert response.status_code == 200
    assert response.get_json() == [{"id": 1, "name": "Test Subject"}]


def test_update_disciplina():
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.register_blueprint(subject_blueprint)  # Register the blueprint
    client = app.test_client()

    with app.app_context():
        with patch('models.Disciplina.Disciplina.query') as mock_query_disciplina, patch('models.db.db.session.commit'):
            mock_subject = MagicMock()
            mock_subject.to_json.return_value = {"id": 1, "name": "Updated Test Subject", "carga_horaria": 60, "codigo": "COD01", "credito": 4, "tipo": "Obrigatória"}
            mock_query_disciplina.get.return_value = mock_subject

            response = client.put('/subjects/1', json={"name": "Updated Test Subject", "carga_horaria": 60, "codigo": "COD01", "credito": 4, "tipo": "Obrigatória"})

    assert response.status_code == 200
    assert response.get_json() == {"updated_subject": {"id": 1, "name": "Updated Test Subject", "carga_horaria": 60, "codigo": "COD01", "credito": 4, "tipo": "Obrigatória"}}


def test_find_subject_by_id():
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.register_blueprint(subject_blueprint)  # Register the blueprint
    client = app.test_client()

    with app.app_context():
        with patch('models.Disciplina.Disciplina.query') as mock_query_disciplina:
            mock_subject = MagicMock()
            mock_subject.to_json.return_value = {"id": 1, "name": "Test Subject"}
            mock_query_disciplina.get.return_value = mock_subject

            response = client.get('/subjects/1')

    assert response.status_code == 200
    assert response.get_json() == {"id": 1, "name": "Test Subject"}


def test_delete_subject_by_id():
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.register_blueprint(subject_blueprint)  # Register the blueprint
    client = app.test_client()

    with app.app_context():
        with patch('models.Disciplina.Disciplina.query') as mock_query_disciplina, patch('models.db.db.session') as mock_session:
            mock_subject = MagicMock()
            mock_subject.to_json.return_value = {"id": 1, "name": "Test Subject"}
            mock_query_disciplina.get.return_value = mock_subject

            mock_session.delete.return_value = None
            mock_session.commit.return_value = None

            response = client.delete('/subjects/1')

    assert response.status_code == 200
    assert response.get_json() == {"deleted_subject": {"id": 1, "name": "Test Subject"}}


def test_get_most_failed_subjects():
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.register_blueprint(subject_blueprint)  # Register the blueprint
    client = app.test_client()

    with app.app_context():
        with patch('models.db.db.session.query') as mock_query, patch('models.Disciplina.Disciplina') as mock_disciplina, patch('models.Historico.Historico') as mock_historico:
            mock_subject = MagicMock()
            mock_subject.id_disciplina = 1
            mock_subject.codigo_disciplina = "COD01"
            mock_subject.nome_disciplina = "Test Subject"
            mock_subject.carga_horaria_disciplina = 60
            mock_subject.total_reprovacoes = 10
            mock_query.return_value.join.return_value.filter.return_value.group_by.return_value.order_by.return_value.limit.return_value.all.return_value = [mock_subject]

            response = client.get('/subjects/most_failed/2022/1')

    assert response.status_code == 200
    assert response.get_json() == {"results": [{"subject_id": 1, "subject_cod": "COD01", "subject_name": "Test Subject", "subject_workload": 60, "subject_total_fails": 10}]}


def test_get_subject_fails_rate():
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.register_blueprint(subject_blueprint)  # Register the blueprint
    client = app.test_client()

    with app.app_context():
        with patch('models.Disciplina.Disciplina.query') as mock_query_disciplina, patch('models.Historico.Historico.query') as mock_query_historico:
            mock_subject = MagicMock()
            mock_query_disciplina.get.return_value = mock_subject

            mock_total_students = MagicMock()
            mock_total_students.count.return_value = 10  # Total students
            mock_failed_students = MagicMock()
            mock_failed_students.count.return_value = 5  # Failed students

            mock_query_historico.filter.side_effect = [mock_failed_students, mock_total_students]

            response = client.get('/subjects/rate/fails/1')

    assert response.status_code == 200
    assert response.get_json() == {"subject_id": 1, "total_students": 10, "failed_students": 5, "fail_rate": 50.0}


def test_get_retention_rate_disciplina():
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.register_blueprint(subject_blueprint)  # Register the blueprint
    client = app.test_client()

    with app.app_context():
        with patch('models.Disciplina.Disciplina.query') as mock_query_disciplina, patch('models.Historico.Historico.query') as mock_query_historico:
            mock_subject = MagicMock()
            mock_query_disciplina.get.return_value = mock_subject

            mock_approved_students = MagicMock()
            mock_approved_students.count.return_value = 10  # Approved students
            mock_failed_students = MagicMock()
            mock_failed_students.count.return_value = 5  # Failed students

            mock_query_historico.filter.side_effect = [mock_approved_students, mock_failed_students]

            response = client.get('/subjects/rate/retention/1')

    assert response.status_code == 200
    assert response.get_json() == {
        "subject_id": 1,
        "Number of approved students": 10,
        "Number of failed students": 5,
        "Retention rate": 0.3333333333333333
    }


def test_get_students_that_failed_more_than_times():
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.register_blueprint(subject_blueprint)  # Register the blueprint
    client = app.test_client()

    with app.app_context():
        with patch('models.Disciplina.Disciplina.query') as mock_query_disciplina, patch('models.Historico.Historico.query') as mock_query_historico:
            mock_subject = MagicMock()
            mock_query_disciplina.get.return_value = mock_subject

            mock_failed_student = MagicMock()
            mock_failed_student.cpf_aluno = "111.757.432-57"
            mock_query_historico.filter.return_value.all.return_value = [mock_failed_student] * 3  # Failed students

            response = client.get('/subjects/students/failed_by_times/1/2')

    assert response.status_code == 200
    assert response.get_json() == {
        "subject_id": 1,
        "students_that_failed_more_than_n_times": ["111.757.432-57"]
    }


def test_get_average_credits_by_subject():
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.register_blueprint(subject_blueprint)  # Register the blueprint
    client = app.test_client()

    with app.app_context():
        with patch('models.db.db.session.query') as mock_query:
            mock_avg = MagicMock()
            mock_avg.avg = 4.5  # Average credits
            mock_query.return_value.filter.return_value = [mock_avg]

            response = client.get('/subjects/average/credits')

    assert response.status_code == 200
    assert response.get_json() == {"average_credits": 4.5}


def test_get_average_workload_by_subject():
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.register_blueprint(subject_blueprint)  # Register the blueprint
    client = app.test_client()

    with app.app_context():
        with patch('models.db.db.session.query') as mock_query:
            mock_avg = MagicMock()
            mock_avg.avg = 60.5  # Average workload
            mock_query.return_value = [mock_avg]

            response = client.get('/subjects/average/workload')

    assert response.status_code == 200
    assert response.get_json() == {"average_workload": 60.5}


def test_get_approval_rate_disciplina():
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.register_blueprint(subject_blueprint)  # Register the blueprint
    client = app.test_client()

    with app.app_context():
        with patch('models.Disciplina.Disciplina.query') as mock_query_disciplina, patch('models.Historico.Historico.query') as mock_query_historico:
            mock_subject = MagicMock()
            mock_query_disciplina.get.return_value = mock_subject

            mock_approved_students = MagicMock()
            mock_approved_students.count.return_value = 10  # Approved students
            mock_failed_students = MagicMock()
            mock_failed_students.count.return_value = 5  # Failed students

            mock_query_historico.filter.side_effect = [mock_approved_students, mock_failed_students]

            response = client.get('/subject/approval/1')

    assert response.status_code == 200
    assert response.get_json() == {
        "subject_id": 1,
        "number of approved students": 10,
        "number of failed students": 5,
        "approval rate": 0.6666666666666666 # Round to two decimal places
    }


def test_get_students_attending_subject_rate():
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.register_blueprint(subject_blueprint)  # Register the blueprint
    client = app.test_client()

    with app.app_context():
        with patch('models.Disciplina.Disciplina.query') as mock_query_disciplina, patch('models.Aluno.Aluno.query') as mock_query_aluno, patch('models.Historico.Historico.query') as mock_query_historico:
            mock_subject = MagicMock()
            mock_subject.id = 1
            mock_query_disciplina.all.return_value = [mock_subject]  # Mock subjects

            mock_student = MagicMock()
            mock_query_aluno.all.return_value = [mock_student] * 10  # Mock total students

            mock_current_student = MagicMock()
            mock_query_historico.filter.return_value.all.return_value = [mock_current_student] * 5  # Mock current students

            response = client.get('/subjects/rate/attending_students')

    assert response.status_code == 200
    assert response.get_json() == [{"Subject": 1, "Attending students rate": 0.5}]


def test_get_total_abandonment_rate():
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.register_blueprint(subject_blueprint)  # Register the blueprint
    client = app.test_client()

    with app.app_context():
        with patch('models.Aluno.Aluno.query') as mock_query_aluno, patch('models.Historico.Historico.query') as mock_query_historico:
            mock_query_aluno.count.return_value = 10  # Total students

            mock_query_historico.filter.return_value.distinct.return_value.count.return_value = 5  # Quitting students

            response = client.get('/subjects/rate/total_abandonment')

    assert response.status_code == 200
    assert response.get_json() == {
        "Total of students": 10,
        "Quiting students": 5,
        "Abandonment rate": 50.0
    }


def test_get_fails_by_subject():
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.register_blueprint(subject_blueprint)  # Register the blueprint
    client = app.test_client()

    with app.app_context():
        with patch('models.Disciplina.Disciplina.query') as mock_query_disciplina, patch('models.Historico.Historico.query') as mock_query_historico:
            mock_subject = MagicMock()
            mock_query_disciplina.get.return_value = mock_subject

            mock_failed_students = MagicMock()
            mock_failed_students.count.return_value = 5  # Failed students

            mock_query_historico.filter.return_value = mock_failed_students

            response = client.get('/subjects/fails/1')

    assert response.status_code == 200
    assert response.get_json() == {"Fails": 5}


def test_graduation_rate():
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.register_blueprint(subject_blueprint)  # Register the blueprint
    client = app.test_client()

    with app.app_context():
        with patch('models.Aluno.Aluno.query') as mock_query_aluno, patch('models.Historico.Historico.query') as mock_query_historico, patch('models.Disciplina.Disciplina.query') as mock_query_disciplina:
            mock_student = MagicMock()
            mock_student.cpf = "111.757.432-57"
            mock_query_aluno.all.return_value = [mock_student]  # Mock students
            mock_query_aluno.count.return_value = 1  # Total students

            mock_approved = MagicMock()
            mock_approved.id_disciplina = 1
            mock_query_historico.filter.return_value.all.return_value = [mock_approved]  # Approved subjects

            mock_mandatory = MagicMock()
            mock_mandatory.id = 1
            mock_query_disciplina.filter.return_value.all.return_value = [mock_mandatory]  # Mandatory subjects
            mock_query_disciplina.filter.return_value.count.return_value = 1  # Total mandatory subjects

            response = client.get('/subjects/rate/graduate')

    assert response.status_code == 200
    assert response.get_json() == {"taxa_graduacao": 1.0}


# def test_get_approval_by_professor():
#     app = Flask(__name__)
#     app.config['TESTING'] = True
#     app.register_blueprint(subject_blueprint)  # Register the blueprint
#     client = app.test_client()
#
#     with app.app_context():
#         with patch('models.Professor.Professor.query') as mock_query_professor, patch('models.Disciplina.Disciplina.query') as mock_query_disciplina, patch('models.Historico.Historico.query') as mock_query_historico:
#             mock_professor = MagicMock()
#             mock_professor.matricula = 1
#             mock_professor.to_json.return_value = {"matricula": 1}  # Mock professor's JSON representation
#             mock_query_professor.all.return_value = [mock_professor]  # Mock professors
#
#             mock_subject = MagicMock()
#             mock_subject.id = 1
#             mock_query_disciplina.filter_by.return_value.all.return_value = [mock_subject]  # Mock subjects
#
#             mock_approved_students = MagicMock()
#             mock_approved_students.count.return_value = 10  # Approved students
#             mock_total_students = MagicMock()
#             mock_total_students.count.return_value = 20  # Total students
#
#             mock_query_historico.filter.side_effect = [mock_approved_students, mock_total_students]
#
#             response = client.get('/subjects/approval/professor')
#
#     assert response.status_code == 200
#     assert response.get_json() == [{"matricula": 1, "Approval rate": 50.0}]


# def test_get_grade_distribution_by_subject():
#     app = Flask(__name__)
#     app.config['TESTING'] = True
#     app.register_blueprint(subject_blueprint)  # Register the blueprint
#     client = app.test_client()
#
#     with app.app_context():
#         with patch('models.Disciplina.Disciplina.query') as mock_query_disciplina, patch('models.Historico.Historico.query') as mock_query_historico:
#             mock_subject = MagicMock()
#             mock_query_disciplina.get.return_value = mock_subject
#
#             mock_subjects_count = MagicMock()
#             mock_subjects_count.count.return_value = 2  # Subjects count
#             mock_query_historico.filter.return_value = mock_subjects_count
#
#             mock_subject_studied = MagicMock()
#             mock_subject_studied.nota = 5
#             mock_query_historico.filter.return_value.all.return_value = [mock_subject_studied, mock_subject_studied]  # Subjects studied
#
#             response = client.get('/subjects/grade/distribution/1')
#
#     assert response.status_code == 200
#     assert response.get_json() == {"Grade distribution": 5.0}


# def test_get_subject_average_grade():
#     app = Flask(__name__)
#     app.config['TESTING'] = True
#     app.register_blueprint(subject_blueprint)  # Register the blueprint
#     client = app.test_client()
#
#     with app.app_context():
#         with patch('models.Disciplina.Disciplina.query') as mock_query_disciplina, patch('models.Historico.Historico.query') as mock_query_historico:
#             mock_subject = MagicMock()
#             mock_query_disciplina.get.return_value = mock_subject
#
#             mock_sum_of_grades = MagicMock()
#             mock_sum_of_grades.scalar.return_value = 50  # Sum of grades
#             mock_total_students = MagicMock()
#             mock_total_students.count.return_value = 10  # Total students
#
#             mock_query_historico.filter.side_effect = [mock_sum_of_grades, mock_total_students]
#
#             response = client.get('/subjects/grade/average/1')
#
#     assert response.status_code == 200
#     assert response.get_json() == {"subject_id": 1, "average": 5.0}


# def test_create_subject():
#     app = Flask(__name__)
#     app.config['TESTING'] = True
#     app.register_blueprint(subject_blueprint)  # Register the blueprint
#     client = app.test_client()
#
#     with app.app_context():
#         with patch('models.Disciplina.Disciplina') as mock_disciplina, patch('models.Disciplina.Disciplina.query') as mock_query_disciplina, patch('models.db.db.session') as mock_session:
#             mock_new_subject = MagicMock()
#             mock_new_subject.to_json.return_value = {"id": 1, "name": "New Test Subject", "carga_horaria": 60, "codigo": "COD01", "credito": 4, "tipo": "Obrigatória"}
#             mock_disciplina.return_value = mock_new_subject
#
#             mock_query_disciplina.get.return_value = None
#
#             mock_session.add.return_value = None
#             mock_session.commit.return_value = None
#
#             response = client.post('/subjects', json={"name": "New Test Subject", "carga_horaria": 60, "codigo": "COD01", "credito": 4, "tipo": "Obrigatória"})
#
#     assert response.status_code == 201
#     assert response.get_json() == {"created_subject": {"id": 1, "name": "New Test Subject", "carga_horaria": 60, "codigo": "COD01", "credito": 4, "tipo": "Obrigatória"}}

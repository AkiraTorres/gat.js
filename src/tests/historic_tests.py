import pytest
from app import app
from unittest.mock import patch
from flask import make_response

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


# Teste simples 2+ 2
def test_two_plus_two():
    assert 2 + 2 == 4



@patch('src.routes.historic_blueprint.list_all_historic')
def test_list_historic(mock_list_all_historic, client):
    mock_list_all_historic.return_value = make_response([])  # Mock o valor de retorno para ser um objeto Flask Response
    response = client.get("/historic")
    assert response.status_code == 200




@patch('app.create_historic')  # Substitua 'app.create_historic' pelo caminho correto para a função
def test_create_historic(mock_create, client):
    mock_create.return_value = {'message': 'Historic created.'}, 201  # Substitua por qualquer valor que a função real retornaria
    historic = {
        "cpf_aluno": "111.757.432-57",
        "id_disciplina": 4,
        "status": 1,
        "ano": 2016,
        "semestre": 1,
        "nota": 8
    }
    response = client.post("/historic", json=historic)
    assert response.status_code == 201


@patch('app.get_historic_by_cpf')  # Substitua 'app.get_historic_by_cpf' pelo caminho correto para a função
def test_get_history_by_cpf(mock_get, client):
    mock_get.return_value = [], 200
    response = client.get("/historic/get_historic_by_cpf/111.757.432-57")
    assert response.status_code == 200

@patch('app.get_historic_by_ids')  # Substitua 'app.get_historic_by_ids' pelo caminho correto para a função
def test_get_historic_by_ids(mock_get, client):
    mock_get.return_value = [], 200
    response = client.get("/historic/get_historic_by_ids/111.757.432-57/4")
    assert response.status_code == 200

@patch('app.get_enrolled_students')  # Substitua 'app.get_enrolled_students' pelo caminho correto para a função
def test_enrolled_students(mock_get, client):
    mock_get.return_value = [], 200
    response = client.get("/historic/enrolled_students")
    assert response.status_code == 200

@patch('app.get_retention_rate')  # Substitua 'app.get_retention_rate' pelo caminho correto para a função
def test_get_retention_rate(mock_get, client):
    mock_get.return_value = [], 200
    response = client.get("/historic/get_retention_rate/2014")
    assert response.status_code == 200


@patch('app.get_global_approval_rate')  # Substitua 'app.get_global_approval_rate' pelo caminho correto para a função
def test_get_global_approval_rate(mock_get, client):
    mock_get.return_value = [], 200
    response = client.get("/historic/get_global_approval_rate")
    assert response.status_code == 200

@patch('app.get_success_rate_year')  # Substitua 'app.get_success_rate_year' pelo caminho correto para a função
def test_get_success_rate_year(mock_get, client):
    mock_get.return_value = [], 200
    response = client.get("/historic/get_success_rate_year/2014")
    assert response.status_code == 200

@patch('app.get_abandonment_by_subject')  # Substitua 'app.get_abandonment_by_subject' pelo caminho correto para a função
def test_get_abandonment_by_subject(mock_get, client):
    mock_get.return_value = [], 200
    response = client.get("/historic/get_abandonment_by_subject/3")
    assert response.status_code == 200

@patch('app.get_subjects_by_student')  # Substitua 'app.get_subjects_by_student' pelo caminho correto para a função
def test_subjects_by_student(mock_get, client):
    mock_get.return_value = [], 200
    response = client.get("/historic/subjects_by_student")
    assert response.status_code == 200

# Testes de integração
@patch('app.create_historic')  # Substitua 'app.create_historic' pelo caminho correto para a função
def test_post_create_historic(mock_create, client):
    mock_create.return_value = {'message': 'Historic created.'}, 201
    historic = {
        "ano": 2018,
        "semestre": 1,
        "aluno_cpf": "111.249.650-26",
        "disciplina_id": 2,
        "nota": 10,
        "faltas": 0
    }

    response = client.post("/historic", json=historic)
    assert response.status_code == 201

@patch('app.update_historic_by_id')  # Substitua 'app.update_historic_by_id' pelo caminho correto para a função
def test_put_update_historic_by_id(mock_update, client):
    mock_update.return_value = {'message': 'Historic updated.'}, 200
    historic = {
        "ano": 2018,
        "semestre": 1,
        "aluno_cpf": "111.249.650-26",
        "disciplina_id": 2,
        "nota": 10,
        "faltas": 0
    }
    response = client.put("/historic", json=historic)
    assert response.status_code == 200

@patch('app.get_historic')  # Substitua 'app.get_historic' pelo caminho correto para a função
def test_list_historic(mock_get, client):
    mock_get.return_value = [], 200
    response = client.get("/historic")
    assert response.status_code == 200

@patch('app.get_historic_by_cpf')  # Substitua 'app.get_historic_by_cpf' pelo caminho correto para a função
def test_get_historic_by_cpf(mock_get, client):
    mock_get.return_value = [], 200
    response = client.get("/historics/get_historic_by_cpf/111.249.650-26")
    assert response.status_code == 200

@patch('app.get_historic_by_ids')  # Substitua 'app.get_historic_by_ids' pelo caminho correto para a função
def test_get_historic_by_ids(mock_get, client):
    mock_get.return_value = [], 200
    response = client.get("/historics/get_historic_by_ids/111.249.650-26, 2")
    assert response.status_code == 200

@patch('app.get_enrolled_students')  # Substitua 'app.get_enrolled_students' pelo caminho correto para a função
def test_enrolled_students(mock_get, client):
    mock_get.return_value = [], 200
    response = client.get("/historic/enrolled_students")
    assert response.status_code == 200

@patch('app.get_retention_rate')  # Substitua 'app.get_retention_rate' pelo caminho correto para a função
def test_get_retention_rate(mock_get, client):
    mock_get.return_value = [], 200
    response = client.get("/historic/get_retention_rate/2018")
    assert response.status_code == 200

@patch('app.get_global_seccess_rate_year')  # Substitua 'app.get_global_seccess_rate_year' pelo caminho correto para a função
def test_get_global_seccess_rate_year(mock_get, client):
    mock_get.return_value = [], 200
    response = client.get("/historic/get_global_seccess_rate_year/2018")
    assert response.status_code == 200
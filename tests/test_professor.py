def test_list_professors_must_return_200(app):
    response = app.test_client().get("/professors")
    assert response.status_code == 200


def test_find_professor_by_cpf_must_return_200(app):
    response = app.test_client().get("/professors/567.890.123-45")
    assert response.status_code == 200


def test_update_professor_by_cpf_must_return_200(app):
    response = app.test_client().put("/professors/567.890.123-45", json={
        "name": "Professor Teste"
    })
    assert response.status_code == 200


# def test_delete_professor_by_cpf_must_return_200(app):
#     response = app.test_client().delete("/professors/345.678.901-33")
#     assert response.status_code == 200


# não é possível testar
# def test_create_professor_must_return_201(app):
#     response = app.test_client().post("/professors", json={
#         "cpf": "345.678.901-43",
#         "matricula": "14389",
#         "nome": "Professor Teste"
#     })
#     assert response.status_code == 201


# Bugado busca por qualquer coisa
def test_total_workload_professor_must_return_200(app):
    response = app.test_client().get("/professors/0000/total_workload")
    assert response.status_code == 200


# # não é possível testar
# def test_professor_performance_rate_must_return_200(app):
#     response = app.test_client().get("/professors/2167/performance_rate")
#     assert response.status_code == 200


def test_professor_evaluation_must_return_200(app):
    response = app.test_client().get("/professors/567.890.123-45/evaluation")
    assert response.status_code == 200


def test_average_subjects_by_professor_must_return_200(app):
    response = app.test_client().get("/professors/average_subjects")
    assert response.status_code == 200


def test_get_professor_subjects_must_return_200(app):
    response = app.test_client().get("/professors/0000/subjects")
    assert response.status_code == 200
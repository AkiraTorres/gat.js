def test_list_all_historic_must_return_http_200(app):
    response = app.test_client().get('/historic')
    assert response.status_code == 200


def test_get_historic_by_cpf_must_return_http_200(app):
    response = app.test_client().get('/historic/get_historic_by_cpf/12345678900')
    assert response.status_code == 200


def test_enrolled_students_must_return_http_200(app):
    response = app.test_client().get('/historic/enrolled_students')
    assert response.status_code == 200


def test_get_retention_rate_must_return_http_200(app):
    response = app.test_client().get('/historic/get_retention_rate/2023')
    assert response.status_code == 200


def test_get_global_approval_rate_must_return_http_200(app):
    response = app.test_client().get('/historic/get_global_approval_rate')
    assert response.status_code == 200


def test_get_success_rate_year_must_return_http_200(app):
    response = app.test_client().get('/historic/get_success_rate_year/2022')
    assert response.status_code == 200


def test_get_abandonment_by_subject_must_return_http_200(app):
    response = app.test_client().get('/historic/get_abandonment_by_subject/1')
    assert response.status_code == 200


def test_subjects_by_student_must_return_http_200(app):
    response = app.test_client().get('/historic/subjects_by_student')
    assert response.status_code == 200


# #não é possível testar
# def test_create_historic_must_return_http_201(app):
#     response = app.test_client().post('/historic/create_historic', json={
#         "id_aluno": 1,
#         "id_disciplina": 1,
#         "ano": 2021,
#         "semestre": 1,
#         "nota": 10,
#         "faltas": 0
#     })
#     assert response.status_code == 201


# # Não é possível testar
# def test_update_historic_must_return_http_200(app):
#     response = app.test_client().put('/historic/1', json={
#         "ano": 2013,
#         "cpf_aluno": "111.485.533-48",
#         "id": 1,
#         "id_disciplina": 1,
#         "nota": "10.00",
#         "semestre": 1,
#         "status": 4
#     })
#     assert response.status_code == 200


# # Não é possível testar
# def test_delete_historic_must_return_http_200(app):
#     response = app.test_client().delete('/historico/1')
#     assert response.status_code == 200


# # Não é possível testar
# def test_get_historic_by_ids_must_return_http_200(app):
#     response = app.test_client().get('/historic/get_historic_by_ids/111.256.963-77/4')
#     assert response.status_code == 200
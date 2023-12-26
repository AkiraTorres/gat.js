def test_list_subjects_must_return_http_200(app):
    response = app.test_client().get('/subjects')
    assert response.status_code == 200


# #não é possível testar
# def test_update_subject_must_return_http_200(app):
#     response = app.test_client().put('/subjects/1', json={
#         "carga_horaria": 60,
#         "codigo": "123456",
#         "credito": 4,
#         "id": 1,
#         "nome": "Teste",
#         "tipo": "Obrigatória"
#     })
#     assert response.status_code == 200


# #não é possível testar
# def test_create_subject_must_return_http_201(app):
#     response = app.test_client().post('/subjects', json={
#         "carga_horaria": 60,
#         "codigo": "123456",
#         "credito": 4,
#         "id": 1,
#         "nome": "Teste",
#         "tipo": "Obrigatória"
#     })
#     assert response.status_code == 201



def test_find_subject_by_id_must_return_http_200(app):
    response = app.test_client().get('/subjects/1')
    assert response.status_code == 200


# #não é possível testar
# def test_delete_subject_by_id_must_return_http_200(app):
#     response = app.test_client().delete('/subjects/1')
#     assert response.status_code == 200


def test_get_most_failed_subjects_must_return_http_200(app):
    response = app.test_client().get('/subjects/most_failed/2021/1')
    assert response.status_code == 200


def test_get_subject_fails_rate_must_return_http_200(app):
    response = app.test_client().get('/subjects/rate/fails/1')
    assert response.status_code == 200


def test_get_subject_average_grade_must_return_http_200(app):
    response = app.test_client().get('/subjects/grade/average/2')
    assert response.status_code == 200


def test_get_retention_rate_disciplina_must_return_http_200(app):
    response = app.test_client().get('/subjects/rate/retention/1')
    assert response.status_code == 200


def test_get_students_that_failed_more_than_times_must_return_http_200(app):
    response = app.test_client().get('/subjects/students/failed_by_times/1/1')
    assert response.status_code == 200


def test_get_average_credits_by_subject_must_return_http_200(app):
    response = app.test_client().get('/subjects/average/credits')
    assert response.status_code == 200


def test_get_average_workload_by_subject_must_return_http_200(app):
    response = app.test_client().get('/subjects/average/workload')
    assert response.status_code == 200


def test_get_approval_rate_disciplina_must_return_http_200(app):
    response = app.test_client().get('/subject/approval/1')
    assert response.status_code == 200


def test_get_students_attending_subject_rate_must_return_http_200(app):
    response = app.test_client().get('/subjects/rate/attending_students')
    assert response.status_code == 200


def test_get_total_abandonment_rate_must_return_http_200(app):
    response = app.test_client().get('/subjects/rate/total_abandonment')
    assert response.status_code == 200


def test_get_fails_by_subject_must_return_http_200(app):
    response = app.test_client().get('/subjects/fails/1')
    assert response.status_code == 200


def test_get_approval_by_professor_must_return_http_200(app):
    response = app.test_client().get('/subjects/approval/professor')
    assert response.status_code == 200


def test_get_grade_distribution_by_subject_must_return_http_200(app):
    response = app.test_client().get('/subjects/grade/distribution/1')
    assert response.status_code == 200


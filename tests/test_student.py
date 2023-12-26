# #Não é possível testar
# def test_create_student_must_return_http_201(app):
#     response = app.test_client().post('/students', json={
#         "ano_entrada": 2021,
#         "cpf": "12345678900",
#         "nome": "Teste",
#         "turma": "1A"
#     })
#     assert response.status_code == 201


def test_list_students_must_return_http_200(app):
    response = app.test_client().get('/students')
    assert response.status_code == 200


def test_get_student_by_cpf_must_return_http_200(app):
    response = app.test_client().get('/students/111.616.457-79')
    assert response.status_code == 200


def test_update_student_must_return_http_200(app):
    response = app.test_client().put('/students/111.616.457-79', json={
        "ano_entrada": 2021,
        "cpf": "111.616.457-79",
        "nome": "Teste",
        "turma": "1A"
    })
    assert response.status_code == 200


# def test_delete_student_by_cpf_must_return_http_200(app):
#     response = app.test_client().delete('/students/111.090.825-98')
#     assert response.status_code == 200


def test_get_credits_rate_must_return_http_200(app):
    response = app.test_client().get('/students/credit/111.628.656-73')
    assert response.status_code == 200


def test_performance_must_return_http_200(app):
    response = app.test_client().get('/students/performance/')
    assert response.status_code == 200


def test_get_how_many_electives_must_return_http_200(app):
    response = app.test_client().get('/students/subjects/electives/111.628.656-73')
    assert response.status_code == 200


def test_get_how_many_mandatory_must_return_http_200(app):
    response = app.test_client().get('/students/subjects/mandatory/111.628.656-73')
    assert response.status_code == 200


def test_get_overall_academic_performance_must_return_http_200(app):
    response = app.test_client().get('/students/performance/overall')
    assert response.status_code == 200


def test_get_student_conclusion_rate_must_return_http_200(app):
    response = app.test_client().get('/students/conclusion_rate/111.628.656-73')
    assert response.status_code == 200


def test_get_student_fails_must_return_http_200(app):
    response = app.test_client().get('/students/fails/111.628.656-73')
    assert response.status_code == 200


def test_get_average_grade_must_return_http_200(app):
    response = app.test_client().get('/students/average/grade')
    assert response.status_code == 200


def test_get_student_approved_subjects_must_return_http_200(app):
    response = app.test_client().get('/students/approved/111.628.656-73')
    assert response.status_code == 200


def test_get_student_grade_distribution_must_return_http_200(app):
    response = app.test_client().get('/students/grade/distibution/111.628.656-73')
    assert response.status_code == 200
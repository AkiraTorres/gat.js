import unittest
from app import app  # Supondo que app seja a sua aplicação Flask

class testHistoricBlueprint(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()


    def test_list_historic(self):
        response = self.app.get('/historic')
        self.assertEqual(response.status_code, 200)


    def test_get_historic_by_cpf(self):
        response = self.app.get('/historics/get_historic_by_cpf/111.249.650-26')
        self.assertEqual(response.status_code, 200)


    def test_get_historic_by_ids(self):
        response = self.app.get('/historics/get_historic_by_ids/111.249.650-26, 2')
        self.assertEqual(response.status_code, 200)


    def test_enrolled_students(self):
        response = self.app.get('/historic/enrolled_students')
        self.assertEqual(response.status_code, 200)


    def test_get_retention_rate(self):
        response = self.app.get('/historic/get_retention_rate/2018')
        self.assertEqual(response.status_code, 200)


    def test_get_global_seccess_rate_year(self):
        response = self.app.get('/historic/get_global_seccess_rate_year/2018')
        self.assertEqual(response.status_code, 200)


    def test_get_abandonment_by_student(self):
        response = self.app.get('/historic/get_abandonment_by_student/111.249.650-26')
        self.assertEqual(response.status_code, 200)


    def test_subjects_by_student(self):
        response = self.app.get('/historic/subjects_by_student/111.249.650-26')
        self.assertEqual(response.status_code, 200)

    def test_post_create_historic(self):
        historic_data = {
            "ano": 2018,
            "semestre": 1,
            "aluno_cpf": "111.249.650-26",
            "disciplina_id": 2,
            "nota": 10,
            "faltas": 0
        }
        response = self.app.post('/historic', json=historic_data)
        self.assertEqual(response.status_code, 201)


    def test_put_update_historic_by_id(self):
        historic_data = {
            "ano": 2018,
            "semestre": 1,
            "aluno_cpf": "111.249.650-26",
            "disciplina_id": 2,
            "nota": 10,
            "faltas": 0
        }
        response = self.app.put('/historic/1', json=historic_data)
        self.assertEqual(response.status_code, 200)


    def test_delete_historic_by_id(self):
        response = self.app.delete('/historic/1')
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()

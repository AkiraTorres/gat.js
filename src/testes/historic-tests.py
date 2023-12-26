import unittest
from app import app

class TestHistoricBlueprint(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    
    def test_list_historic(self):
        response = self.app.get("/historic")
        self.assertEqual(response.status_code, 200)


    def test_create_historic(self):
        historic = {
            "cpf_aluno": "111.757.432-57",
            "id_disciplina": 4,
            "status": 1,
            "ano": 2016,
            "semestre": 1,
            "nota": 8
        }
        response = self.app.post("/historic", json=historic)
        self.assertEqual(response.status_code, 201)


    def test_get_history_by_cpf(self):
        response = self.app.get("/historic/get_historic_by_cpf/111.757.432-57")
        self.assertEqual(response.status_code, 200)


    def test_get_historic_by_ids(self):
        response = self.app.get("/historic/get_historic_by_ids/111.757.432-57/4")
        self.assertEqual(response.status_code, 200)


    def test_enrolled_students(self):
        response = self.app.get("/historic/enrolled_students")
        self.assertEqual(response.status_code, 200)


    def test_get_retention_rate(self):
        response = self.app.get("/historic/get_retention_rate/2014")
        self.assertEqual(response.status_code, 200)


    def test_get_global_approval_rate(self):
        response = self.app.get("/historic/get_global_approval_rate")
        self.assertEqual(response.status_code, 200)


    def test_get_success_rate_year(self):
        response = self.app.get("/historic/get_success_rate_year/2014")
        self.assertEqual(response.status_code, 200)


    def test_get_abandonment_by_subject(self):
        response = self.app.get("/historic/get_abandonment_by_subject/3")
        self.assertEqual(response.status_code, 200)


    def test_subjects_by_student(self):
        response = self.app.get("/historic/subjects_by_student")
        self.assertEqual(response.status_code, 200)

    
    def test_update_historic(self):
        historic = {
            "ano": 2014,
            "cpf_aluno": "111.485.533-48",
            "id": 1,
            "id_disciplina": 1,
            "nota": "10.00",
            "semestre": 1,
            "status": 4
        }
        response = self.app.put("/historic/1", json=historic)
        self.assertEqual(response.status_code, 200)

    
    def test_delete_historic(self):
        response = self.app.delete("/historic/3")
        self.assertEqual(response.status_code, 200)






if __name__ == '__main__':
    unittest.main()

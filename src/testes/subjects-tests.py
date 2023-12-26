import unittest
from app import app  
from flask import Flask, jsonify
from flask.testing import FlaskClient


class TestSubjectBlueprint(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_list_disciplinas(self):
        response = self.app.get('/subjects')
        self.assertEqual(response.status_code, 200)
    def test_update_disciplina(self):
        # Dados simulados para atualização
        disciplina_data = {
            "carga_horaria": 30,
            "codigo": "MYUU9134",
            "credito": 2,
            "id": 3,
            "nome": "Design de Realidade Simulada.",
            "tipo": 1
        }
        response = self.app.put('/subjects/3', json=disciplina_data)
        self.assertEqual(response.status_code, 200)

    def test_create_subject(self):
        nova_disciplina = {
            "id": 234,
            "carga_horaria": 45,
            "codigo": "TST103",
            "credito": 3,
            "nome": "Nova Disciplina",
            "tipo": "Optativa", 
            "matricula_professor": "2"
        }

        response = self.app.post('/subjects', json=nova_disciplina)
        self.assertEqual(response.status_code, 403) #Attention

    def test_find_subject_by_id(self):
        response = self.app.get('/subjects/3')
        self.assertEqual(response.status_code, 200)
    def test_delete_subject_by_id(self):
        response = self.app.delete('/subjects/4')
        self.assertEqual(response.status_code, 500) #Attentio
    def test_get_most_failed_subjects(self):
        response = self.app.get('/subjects/most_failed/2017/2')
        self.assertEqual(response.status_code, 200)
    def test_get_subject_fails_rate(self):
        response = self.app.get('/subjects/rate/fails/4')
        self.assertEqual(response.status_code, 200)
    def test_get_subject_average_grade(self):
        response = self.app.get('/subjects/grade/average/24')
        self.assertEqual(response.status_code, 200)
    def test_get_retention_rate_disciplina(self):
        response = self.app.get('/subjects/rate/retention/24')
        self.assertEqual(response.status_code, 200)
    def test_get_students_that_failed_more_than_times(self):
        response = self.app.get('/subjects/students/failed_by_times/24/2')
        self.assertEqual(response.status_code, 200)
    def test_get_average_credits_by_subject(self):
        response = self.app.get('/subjects/average/credits')
        self.assertEqual(response.status_code, 200)
    def test_get_average_workload_by_subject(self):
        response = self.app.get('/subjects/average/workload')
        self.assertEqual(response.status_code, 200)
    def test_get_approval_rate_disciplina(self):
        response = self.app.get('/subject/approval/1')
        self.assertEqual(response.status_code, 200)
    def test_get_students_attending_subject_rate(self):
        response = self.app.get('/subjects/rate/attending_students')
        self.assertEqual(response.status_code, 200)
    def test_get_total_abandonment_rate(self):
        response = self.app.get('/subjects/rate/total_abandonment')
        self.assertEqual(response.status_code, 200)
    def test_get_fails_by_subject(self):
        response = self.app.get('/subjects/fails/1')
        self.assertEqual(response.status_code, 200)
    def test_get_approval_by_professor(self):
        response = self.app.get('/subjects/approval/professor')
        self.assertEqual(response.status_code, 200)
    def test_get_grade_distribution_by_subject(self):
        response = self.app.get('/subjects/grade/distribution/1')
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
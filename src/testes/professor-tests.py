import unittest
from app import app  # Supondo que app seja a sua aplicação Flask
from flask import Flask, jsonify
from flask.testing import FlaskClient

class TestProfessorBlueprint(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
    def test_list_professors(self):
        response = self.app.get('/professors')
        self.assertEqual(response.status_code, 200)
    def test_find_professor_by_cpf(self):
        response = self.app.get('/professors/234.567.890-12') 
        self.assertEqual(response.status_code, 200)
    def test_update_professor_by_cpf(self):
        professor_data = {
            "matricula": 5832,
            "cpf": "234.567.890-12",
            "nome": "Gustavo"
        }
        response = self.app.put('/professors/234.567.890-12', json=professor_data)  
        self.assertEqual(response.status_code, 200)
    def test_delete_professor_by_cpf(self):
        response = self.app.delete('/professors/123.456.789-01')
        self.assertEqual(response.status_code, 200)


    def test_create_professor(self):
        professor_data = {
            "nome": "Maria da Silva",
            "cpf": "987.654.321-00",
            "matricula": 2095
        }
        response = self.app.post('/professors', json=professor_data)
        self.assertEqual(response.status_code, 403) # Atention
    def test_total_workload_professor(self):
        response = self.app.get('/professors/1765/total_workload')
        self.assertEqual(response.status_code, 200)
    def test_professor_performance_rate(self):
        response = self.app.get('/professors/234.567.890-12/performance_rate')
        self.assertEqual(response.status_code, 200)
    def test_professor_evaluation(self):
        response = self.app.get('/professors/234.567.890-12/evaluation')
        self.assertEqual(response.status_code, 200)
    def test_get_average_subjects_by_professor(self):
        response = self.app.get('/professors/average_subjects')
        self.assertEqual(response.status_code, 200)
    def test_get_professor_subjects(self):
        response = self.app.get('/professors/234.567.890-12/subjects')
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()

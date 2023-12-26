import unittest
from app import app
from flask import Flask, jsonify
from flask.testing import FlaskClient

class TestStudentsBlueprint(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
    def test_list_students(self):
        response = self.app.get('/students')
        self.assertEqual(response.status_code, 200)
    def test_find_student_by_cpf(self):
        response = self.app.get('/students/111.304.739-63') 
        self.assertEqual(response.status_code, 200)
    def test_update_student_by_cpf(self):
        student_data = {
            "ano_entrada": 2016,
            "arg_class": "40.0",
            "cpf": "111.304.739-63",
            "nome": "Caronte"
        }
        response = self.app.put('/students/111.304.739-63', json=student_data)  
        self.assertEqual(response.status_code, 200)
    def test_create_student(self):
        student_data = {
            "ano_entrada": 2017,
            "arg_class": "700.0",
            "cpf": "987.654.321-00",
            "nome": "Maria da Silva"
        }
        response = self.app.post('/students', json=student_data)
        self.assertEqual(response.status_code, 201) # Atention
    def test_delete_student_by_cpf(self):
        response = self.app.delete('/students/987.654.321-00')
        self.assertEqual(response.status_code, 200)
    def test_get_credits_rate(self):
        response = self.app.get('/students/credit/111.249.650-26')
        self.assertEqual(response.status_code, 200)
    def test_performance(self):
        response = self.app.get('/students/performance')
        self.assertEqual(response.status_code, 200)
    def test_get_how_many_electives(self):
        response = self.app.get('/students/subjects/electives/111.249.650-26')
        self.assertEqual(response.status_code, 200)
    def test_get_how_many_mandatory(self):
        response = self.app.get('/students/subjects/mandatory/111.249.650-26')
        self.assertEqual(response.status_code, 200)
    def test_get_overall_academic_performance(self):
        response = self.app.get('/students/performance/overall')
        self.assertEqual(response.status_code, 200)
    def test_get_student_conclusion_rate(self):
        response = self.app.get('/students/conclusion_rate/111.249.650-26')
        self.assertEqual(response.status_code, 200)
    def test_get_student_fails(self):
        response = self.app.get('/students/fails/111.249.650-26')
        self.assertEqual(response.status_code, 200)
    def test_get_average_grade(self):
        response = self.app.get('/students/average/grade')
        self.assertEqual(response.status_code, 200)
    def test_get_student_approved_subjects(self):
        response = self.app.get('/students/approved/111.249.650-26')
        self.assertEqual(response.status_code, 200)
    def test_get_student_grade_distribution(self):
        response = self.app.get('/students/grade/distibution/111.249.650-26')
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
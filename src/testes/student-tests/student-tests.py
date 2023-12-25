import unittest
from app import app  # Supondo que app seja a sua aplicação Flask
from flask import Flask, jsonify
from flask.testing import FlaskClient

class TestStudentBlueprint(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_create_aluno(self):
        # Simulando dados para criar um aluno
        aluno_data = {
            "nome": "João",
            "cpf": "12345678900",  # Substitua pelo CPF válido
            "arg_class": 150,  # Substitua pelo valor de arg_class válido
            "ano_entrada": 2022  # Substitua pelo ano de entrada válido
        }

        response = self.app.post('/alunos', json=aluno_data)
        self.assertEqual(response.status_code, 201)
        # Verifique se o aluno foi criado corretamente, se necessário

    def test_list_alunos(self):
        response = self.app.get('/alunos')
        self.assertEqual(response.status_code, 200)
        # Verifique se a resposta contém dados válidos, se necessário

    def test_get_aluno_by_cpf(self):
        response = self.app.get('/alunos/12345678900')  # Substitua pelo CPF válido
        self.assertEqual(response.status_code, 200)
        # Verifique se a resposta contém dados válidos, se necessário

    def test_update_aluno(self):
        # Simulando dados para atualizar um aluno
        aluno_data = {
            "nome": "João Silva",  # Atualize os campos necessários
            "arg_class": 200,  # Atualize os campos necessários
            "ano_entrada": 2023  # Atualize os campos necessários
        }

        response = self.app.put('/alunos/12345678900', json=aluno_data)  # Substitua pelo CPF válido
        self.assertEqual(response.status_code, 200)
        # Verifique se o aluno foi atualizado corretamente, se necessário

    def test_delete_aluno_por_cpf(self):
        response = self.app.delete('/alunos/12345678900')  # Substitua pelo CPF válido
        self.assertEqual(response.status_code, 200)
        # Verifique se o aluno foi excluído corretamente, se necessário

    def test_get_credits_rate(self):
        response = self.app.get('/creditos_aluno/12345678900')  # Substitua pelo CPF válido
        self.assertEqual(response.status_code, 200)
        # Verifique se a resposta contém dados válidos, se necessário

    def test_performance(self):
        response = self.app.get('/desempenho/')
        self.assertEqual(response.status_code, 200)
        # Verifique se a resposta contém dados válidos, se necessário

if __name__ == '__main__':
    unittest.main()

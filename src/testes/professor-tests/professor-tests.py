import unittest
from app import app  # Supondo que app seja a sua aplicação Flask
from flask import Flask, jsonify
from flask.testing import FlaskClient

class TestProfessorBlueprint(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_lista_professores(self):
        response = self.app.get('/professor')
        self.assertEqual(response.status_code, 200)
        # Verifique se a resposta contém dados válidos, se necessário

    def test_buscar_professor_por_cpf(self):
        response = self.app.get('/professor/12345678900')  # Substitua pelo CPF válido
        self.assertEqual(response.status_code, 200)
        # Verifique se a resposta contém dados válidos, se necessário

    def test_atualizar_professor(self):
        professor_data = {
            "nome": "João Silva"  # Atualize os campos necessários
        }

        response = self.app.put('/professor/12345678900', json=professor_data)  # Substitua pelo CPF válido
        self.assertEqual(response.status_code, 200)
        # Verifique se o professor foi atualizado corretamente, se necessário

    def test_excluir_professor(self):
        response = self.app.delete('/professor/12345678900')  # Substitua pelo CPF válido
        self.assertEqual(response.status_code, 200)
        # Verifique se o professor foi excluído corretamente, se necessário

    def test_criar_professor(self):
        professor_data = {
            "nome": "Maria da Silva",  # Substitua pelos dados necessários
            "cpf": "98765432100",  # Substitua pelo CPF válido
            "matricula": "ABC123"  # Substitua pela matrícula válida
        }

        response = self.app.post('/professor', json=professor_data)
        self.assertEqual(response.status_code, 201)
        # Verifique se o professor foi criado corretamente, se necessário

    def test_carga_horaria_total_professor(self):
        response = self.app.get('/carga_horaria_total/123')  # Substitua pela matrícula válida
        self.assertEqual(response.status_code, 200)
        # Verifique se a resposta contém dados válidos, se necessário

    def test_taxa_professor(self):
        response = self.app.get('/taxa_professor/12345678900')  # Substitua pelo CPF válido
        self.assertEqual(response.status_code, 200)
        # Verifique se a resposta contém dados válidos, se necessário

    def test_avaliacao_professor(self):
        response = self.app.get('/avaliacao_professor/12345678900')  # Substitua pelo CPF válido
        self.assertEqual(response.status_code, 200)
        # Verifique se a resposta contém dados válidos, se necessário

if __name__ == '__main__':
    unittest.main()

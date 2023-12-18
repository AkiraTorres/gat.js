import unittest
from app import app  # Importe a sua aplicação Flask aqui
from flask import Flask, jsonify
from flask.testing import FlaskClient

class TestSubjectBlueprint(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_list_disciplinas(self):
        response = self.app.get('/disciplinas')
        self.assertEqual(response.status_code, 200)
        # Verifique se a resposta contém dados válidos, se necessário

    def test_update_disciplina(self):
        disciplina_data = {
            "carga_horaria": 60,  # Atualize os campos necessários
            "codigo": "ABC123",  # Atualize os campos necessários
            "credito": 4,  # Atualize os campos necessários
            "nome": "Nome da Disciplina",  # Atualize os campos necessários
            "tipo": "Obrigatória"  # Atualize os campos necessários
        }

        response = self.app.put('/disciplinas/1', json=disciplina_data)  # Substitua pelo ID válido da disciplina
        self.assertEqual(response.status_code, 200)
        # Verifique se a disciplina foi atualizada corretamente, se necessário

    def test_create_subject(self):
        disciplina_data = {
            "carga_horaria": 60,  # Insira os campos necessários
            "codigo": "DEF456",  # Insira os campos necessários
            "credito": 4,  # Insira os campos necessários
            "nome": "Nome da Nova Disciplina",  # Insira os campos necessários
            "tipo": "Optativa"  # Insira os campos necessários
        }

        response = self.app.post('/disciplinas', json=disciplina_data)
        self.assertEqual(response.status_code, 201)
        # Verifique se a disciplina foi criada corretamente, se necessário

    # Adicione testes para as demais rotas aqui

if __name__ == '__main__':
    unittest.main()

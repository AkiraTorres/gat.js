import unittest
from app import app  # Supondo que app seja a sua aplicação Flask

class TestHistoricoBlueprint(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_find_historico(self):
        response = self.app.get('/historico')
        self.assertEqual(response.status_code, 200)
        # Verifique se a resposta contém dados válidos, se necessário

    def test_get_historic_by_cpf(self):
        response = self.app.get('/historico/12345678900')  # Substitua pelo CPF válido
        self.assertEqual(response.status_code, 200)
        # Verifique se a resposta contém dados válidos, se necessário

    def test_get_historic_by_ids(self):
        response = self.app.get('/historico/1/2')  # Substitua pelos IDs válidos
        self.assertEqual(response.status_code, 200)
        # Verifique se a resposta contém dados válidos, se necessário

    def test_alunos_matriculados(self):
        response = self.app.get('/alunos_matriculados')
        self.assertEqual(response.status_code, 200)
        # Verifique se a resposta contém dados válidos, se necessário

    def test_get_taxa_retencao(self):
        response = self.app.get('/taxa_retencao/2023')  # Substitua pelo ano válido
        self.assertEqual(response.status_code, 200)
        # Verifique se a resposta contém dados válidos, se necessário

    def test_get_taxa_aprovacao_global(self):
        response = self.app.get('/taxa_aprovacao_global')
        self.assertEqual(response.status_code, 200)
        # Verifique se a resposta contém dados válidos, se necessário

    def test_get_taxa_sucesso_ano(self):
        response = self.app.get('/taxa_sucesso/2023')  # Substitua pelo ano válido
        self.assertEqual(response.status_code, 200)
        # Verifique se a resposta contém dados válidos, se necessário

if __name__ == '__main__':
    unittest.main()

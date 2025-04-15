from rest_framework.test import APITestCase
from rest_framework import status
from consultas.models import Consulta, Profissional
from django.contrib.auth.models import User
from decimal import Decimal

class MockPagamentoViewTestCase(APITestCase):
    def setUp(self):
        # Cria um usuário para a autenticação se necessário
        self.user = User.objects.create_user(username='testuser', password='testpassword')

        # Cria um profissional de saúde
        self.profissional = Profissional.objects.create(
            nome='Profissional Teste',
            asaas_recipient_id='mock_wallet_id_profissional'
        )

        # Cria uma consulta associada ao profissional
        self.consulta = Consulta.objects.create(
            valor=Decimal('100.00'),
            profissional=self.profissional
        )

        # Define o URL da view para o mock de pagamento
        self.url = '/api/pagamentos/mock/'

    def test_mock_pagamento_success(self):
        # Testa se o mock de pagamento funciona corretamente
        data = {
            'consulta_id': self.consulta.id
        }
        
        # Realiza o POST na API
        response = self.client.post(self.url, data, format='json')
        
        # Verifica se o código de status retornado é 200 (OK)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verifica se a resposta contém os dados esperados
        self.assertIn('object', response.data)
        self.assertEqual(response.data['object'], 'payment')
        
        # Verifica se o valor total corresponde ao valor da consulta
        self.assertEqual(response.data['value'], float(self.consulta.valor))
        
        # Verifica se os valores dos splits são corretos
        valor_profissional = round(self.consulta.valor * Decimal('0.90'), 2)
        valor_plataforma = self.consulta.valor - valor_profissional
        self.assertEqual(response.data['split'][0]['fixedValue'], float(valor_profissional))
        self.assertEqual(response.data['split'][1]['fixedValue'], float(valor_plataforma))

    def test_mock_pagamento_consulta_inexistente(self):
        # Testa o caso quando a consulta não existe
        data = {
            'consulta_id': 9999  # ID que não existe
        }

        # Realiza o POST na API
        response = self.client.post(self.url, data, format='json')

        # Verifica se o código de status retornado é 404 (NOT FOUND)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # Verifica se a resposta contém a mensagem de erro
        self.assertIn('erro', response.data)
        self.assertEqual(response.data['erro'], 'Consulta não encontrada.')


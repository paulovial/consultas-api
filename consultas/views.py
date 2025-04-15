from rest_framework import viewsets, filters
from .models import ProfissionalSaude, Consulta
from .serializers import ProfissionalSaudeSerializer, ConsultaSerializer

class ProfissionalSaudeViewSet(viewsets.ModelViewSet):
    queryset = ProfissionalSaude.objects.all()
    serializer_class = ProfissionalSaudeSerializer

class ConsultaViewSet(viewsets.ModelViewSet):
    queryset = Consulta.objects.all()    
    serializer_class = ConsultaSerializer

    def get_queryset(self):
        profissional_id = self.request.query_params.get('profissional')
        if profissional_id:
            return Consulta.objects.filter(profissional_id=profissional_id)
        return Consulta.objects.all()

from django.shortcuts import render

def home(request):
    return render(request, 'consultas/home.html')

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from decimal import Decimal
from consultas.models import Consulta, Profissional

class MockPagamentoView(APIView):
    def post(self, request, *args, **kwargs):
        consulta_id = request.data.get('consulta_id')
        try:
            consulta = Consulta.objects.get(id=consulta_id)
            profissional = consulta.profissional
        except Consulta.DoesNotExist:
            return Response({'erro': 'Consulta não encontrada.'}, status=status.HTTP_404_NOT_FOUND)

        valor_total = Decimal(consulta.valor)
        valor_profissional = round(valor_total * Decimal('0.90'), 2)
        valor_plataforma = valor_total - valor_profissional

        mock_response = {
            "object": "payment",
            "id": "pay_mock123456",
            "value": float(valor_total),
            "status": "PENDING",
            "split": [
                {
                    "walletId": profissional.asaas_recipient_id or "mock_wallet_id_profissional",
                    "fixedValue": float(valor_profissional),
                    "status": "RECEIVED"
                },
                {
                    "walletId": "mock_wallet_id_plataforma",
                    "fixedValue": float(valor_plataforma),
                    "status": "RECEIVED"
                }
            ]
        }
        consulta.status_pagamento = 'PENDENTE'  # Ou outro status dependendo do seu modelo
        consulta.save()

        # Você pode criar um objeto de pagamento, caso tenha o modelo para isso
        Pagamento.objects.create(
            consulta=consulta,
            valor=valor_total,
            status='PENDING',
            mock_id=mock_response['id'],
            profissional=profissional
        )

        return Response(mock_response, status=status.HTTP_200_OK)



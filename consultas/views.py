from decimal import Decimal, ROUND_HALF_UP

from django.shortcuts import render, get_object_or_404

from rest_framework import viewsets, filters, status
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Profissional, Consulta, Pagamento
from .serializers import ProfissionalSerializer, ConsultaSerializer

class ProfissionalViewSet(viewsets.ModelViewSet):
    queryset = Profissional.objects.all()
    serializer_class = ProfissionalSerializer

class ConsultaViewSet(viewsets.ModelViewSet):
    queryset = Consulta.objects.all()    
    serializer_class = ConsultaSerializer

    def get_queryset(self):
        profissional_id = self.request.query_params.get('profissional')
        if profissional_id:
            return Consulta.objects.filter(profissional_id=profissional_id)
        return Consulta.objects.all()

def home(request):
    return render(request, 'consultas/home.html')

class MockPagamentoView(APIView):
    def post(self, request, *args, **kwargs):
        consulta_id = request.data.get('consulta_id')
        consulta = get_object_or_404(Consulta, id=consulta_id)
        profissional = consulta.profissional

        valor_total = Decimal(consulta.valor)
        valor_profissional = (valor_total * Decimal('0.90')).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
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

        consulta.status_pagamento = 'PENDENTE'
        consulta.save()

        Pagamento.objects.create(
            consulta=consulta,
            valor=valor_total,
            status='PENDING',
            mock_id=mock_response['id'],
            profissional=profissional
        )

        return Response(mock_response, status=status.HTTP_200_OK)


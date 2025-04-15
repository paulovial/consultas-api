from rest_framework import serializers
from .models import Profissional, Consulta

class ProfissionalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profissional
        fields = '__all__'

    def validate_nome_social(self, value):
        return value.strip()

    def validate_contato(self, value):
        if not value.strip().isdigit():
            raise serializers.ValidationError("Contato deve conter apenas números.")
        return value

class ConsultaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Consulta
        fields = '__all__'

    def validate(self, data):
        if data['data'] is None:
            raise serializers.ValidationError("Data da consulta é obrigatória.")
        return data


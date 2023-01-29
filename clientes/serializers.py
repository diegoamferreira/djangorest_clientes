from rest_framework import serializers

from clientes.models import Cliente
from clientes.validators import cpf_valido, nome_valido, rg_valido, celular_valido


class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = '__all__'

    def validate(self, data):
        if not cpf_valido(data['cpf']):
            raise serializers.ValidationError({'cpf': 'CPF Inválido'})
        if not nome_valido(data['nome']):
            raise serializers.ValidationError({'nome': 'O Nome não pode conter números'})
        if not rg_valido(data['rg']):
            raise serializers.ValidationError({'rg': 'O RG deve ter 9 dígitos'})
        if not celular_valido(data['celular']):
            raise serializers.ValidationError({'celular': 'Número de celular inválido, padrão: 12 12345-1234'})
        return data

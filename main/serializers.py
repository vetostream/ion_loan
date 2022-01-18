from main.models import Client, Loan
from rest_framework import serializers


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'


class LoanSerializer(serializers.ModelSerializer):
    client_full_name = serializers.SerializerMethodField()
    client_birth_date = serializers.SerializerMethodField()

    class Meta:
        model = Loan
        fields = '__all__'

    def get_client_full_name(self, obj):
        return f"{obj.client.last_name}, {obj.client.first_name}"
    
    def get_client_birth_date(self, obj):
        return obj.client.birth_date
    
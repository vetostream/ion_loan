from main.models import Client, Loan, Loan_Detail, Collection
from rest_framework import serializers


class ClientSerializer(serializers.ModelSerializer):
    active_loans = serializers.SerializerMethodField()

    class Meta:
        model = Client
        fields = '__all__'

    def get_active_loans(self, obj):
        active_loans = obj.loan_set.filter(loan_status='approved').values_list('pk', flat=True)
        loan_details = LoanDetailSerializer(Loan_Detail.objects.filter(loan__pk__in=active_loans), many=True).data

        return loan_details


class LoanDetailSerializer(serializers.ModelSerializer):
    loan_amount = serializers.SerializerMethodField()

    class Meta:
        model = Loan_Detail
        fields = '__all__'

    def get_loan_amount(self, obj):
        return obj.loan.principal_amount


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


class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = '__all__'

from main.models import Client, Collection_Detail, Loan, Loan_Detail, Collection, Transaction, Refund, Udi_Table
from rest_framework import serializers


class ClientSerializer(serializers.ModelSerializer):
    active_loans = serializers.SerializerMethodField()
    collections = serializers.SerializerMethodField()
    active_loan_headers = serializers.SerializerMethodField()

    class Meta:
        model = Client
        fields = '__all__'

    def get_active_loans(self, obj):
        active_loans = obj.loan_set.filter(loan_status='approved').values_list('pk', flat=True)
        loan_details = LoanDetailSerializer(Loan_Detail.objects.filter(loan__pk__in=active_loans), many=True).data

        return loan_details

    def get_active_loan_headers(self, obj):
        return LoanSerializer(obj.loan_set.filter(loan_status='approved'), many=True).data

    def get_collections(self, obj):
        # return serialized_collections
        my_collections = obj.collection_set.all()
        serialized_collections = CollectionSerializer(my_collections, many=True)

        return serialized_collections.data


class LoanDetailSerializer(serializers.ModelSerializer):
    loan_amount = serializers.SerializerMethodField()
    loan_control_number = serializers.SerializerMethodField()

    class Meta:
        model = Loan_Detail
        fields = '__all__'

    def get_loan_amount(self, obj):
        return obj.loan.principal_amount

    def get_loan_control_number(self, obj):
        return obj.loan.control_number


class UdiTableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Udi_Table
        fields = '__all__'


class LoanSerializer(serializers.ModelSerializer):
    client_full_name = serializers.SerializerMethodField()
    client_birth_date = serializers.SerializerMethodField()
    running_balance = serializers.SerializerMethodField()
    loan_detail = serializers.SerializerMethodField()
    udi_table = serializers.SerializerMethodField()
    amortization = serializers.SerializerMethodField()
    payments = serializers.SerializerMethodField()

    class Meta:
        model = Loan
        fields = '__all__'

    def get_client_full_name(self, obj):
        return f"{obj.client.last_name}, {obj.client.first_name}"
    
    def get_client_birth_date(self, obj):
        return obj.client.birth_date

    def get_running_balance(self, obj):
        return obj.running_balance

    def get_loan_detail(self, obj):
        return LoanDetailSerializer(obj.loan_detail_set.all(), many=True).data

    def get_udi_table(self, obj):
        return UdiTableSerializer(obj.udi_table_set.all().order_by('date_payment'), many=True).data

    def get_payments(self, obj):
        return CollectionDetailWithoutLoanSerializer(obj.collection_detail_set.all(), many=True).data

    def get_amortization(self, obj):
        if obj.loan_detail_set.count() == 0:
            return 0

        return obj.loan_detail_set.first().amount


class CollectionDetailSerializer(serializers.ModelSerializer):
    loan = LoanSerializer(read_only=True)

    class Meta:
        model = Collection_Detail
        fields = '__all__'


class CollectionSerializer(serializers.ModelSerializer):
    collection_details = CollectionDetailSerializer(many=True, read_only=True)

    class Meta:
        model = Collection
        fields = '__all__'


class CollectionWithoutDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = '__all__'


class CollectionDetailWithoutLoanSerializer(serializers.ModelSerializer):
    collection = CollectionWithoutDetailSerializer(read_only=True)
    class Meta:
        model = Collection_Detail
        fields = '__all__'


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'


class RefundSerializer(serializers.ModelSerializer):
    class Meta:
        model = Refund
        fields = '__all__'        

from main.models import Client, Collection_Detail, Loan, Loan_Detail, Collection
from rest_framework import serializers


class ClientSerializer(serializers.ModelSerializer):
    active_loans = serializers.SerializerMethodField()
    collections = serializers.SerializerMethodField()

    class Meta:
        model = Client
        fields = '__all__'

    def get_active_loans(self, obj):
        active_loans = obj.loan_set.filter(loan_status='approved').values_list('pk', flat=True)
        loan_details = LoanDetailSerializer(Loan_Detail.objects.filter(loan__pk__in=active_loans), many=True).data

        return loan_details

    def get_collections(self, obj):
        # my_collection_details = Collection_Detail.objects.filter(collection__client=obj)
        # serialized_collections = CollectionDetailSerializer(my_collection_details, many=True).data

        # return serialized_collections
        my_collections = obj.collection_set.all()
        serialized_collections = CollectionSerializer(my_collections, many=True)

        return serialized_collections.data


class LoanDetailSerializer(serializers.ModelSerializer):
    loan_amount = serializers.SerializerMethodField()
    is_paid = serializers.SerializerMethodField()

    class Meta:
        model = Loan_Detail
        fields = '__all__'

    def get_loan_amount(self, obj):
        return obj.loan.principal_amount

    def get_is_paid(self, obj):
        return obj.collection_detail.count() > 0


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


class CollectionDetailSerializer(serializers.ModelSerializer):
    paid_transaction_id = serializers.SerializerMethodField()

    class Meta:
        model = Collection_Detail
        fields = '__all__'

    def get_paid_transaction_id(self, obj):
        types = {
            'loan_detail': 'LOAN',
            'cash_advance': 'CA'
        }

        if obj.content_type.model == 'loan_detail':
            return f"{types[obj.content_type.model]}-{obj.content_object.loan.pk}"
        else:
            return "CA"


class CollectionSerializer(serializers.ModelSerializer):
    collection_details = CollectionDetailSerializer(many=True, read_only=True)

    class Meta:
        model = Collection
        fields = '__all__'
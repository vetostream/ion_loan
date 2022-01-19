from dateutil.relativedelta import relativedelta
from main.models import Client, Collection_Detail, Loan, Loan_Detail, Collection
from main.serializers import ClientSerializer, LoanSerializer, CollectionSerializer
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response


CONTENT_TYPES = {
    'loan_detail': Loan_Detail
}


class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.none()
    serializer_class = ClientSerializer

    def get_queryset(self):
        lastname = self.request.query_params.get('lastname', None)
        if lastname:
            return Client.objects.filter(
                last_name__istartswith=lastname
            )
        return Client.objects.all()


class LoanViewSet(viewsets.ModelViewSet):
    queryset = Loan.objects.none()
    serializer_class = LoanSerializer

    def get_queryset(self):
        lastname = self.request.query_params.get('client_last_name', None)
        loan_status = self.request.query_params.get('loan_status', None)

        if lastname:
            return Loan.objects.filter(
                client__last_name__istartswith=lastname,
                loan_status__iexact=loan_status
            )

        return Loan.objects.all()

    @action(detail=True, methods=['post'])
    def approve_loan(self, request, pk):
        loan_status = request.data.get('loan_status', None)
        loan = Loan.objects.get(pk=pk)
        payment_schedules = []

        if loan_status == 'approved':
            amount = loan.principal_amount / loan.term

            for cycle in range(0, loan.term):
                running_balance = (loan.principal_amount) - (amount * (cycle + 1))
                if cycle == 0:
                    payment_schedules.append({
                        'loan': loan,
                        'date_payment': loan.start_payment,
                        'amount': amount,
                        'balance': running_balance
                    })
                else:
                    date_counter = loan.start_payment + relativedelta(months=cycle)
                    payment_schedules.append({
                        'loan': loan,
                        'date_payment': date_counter,
                        'amount': amount,
                        'balance': running_balance
                    })

            # Create Loan Detail
            for payment in payment_schedules:
                Loan_Detail.objects.create(**payment)
            
            loan.loan_status = loan_status
            loan.save()

        return Response({'message': 'Loan Approved'}, status=status.HTTP_201_CREATED)


class CollectionViewSet(viewsets.ModelViewSet):
    queryset = Collection.objects.none()
    serializer_class = CollectionSerializer

    def get_queryset(self):
        return Collection.objects.all()

    def perform_create(self, serializer):
        collection = serializer.save()
        details = self.request.data.get('detail', None)

        for detail in details:
            content_object = CONTENT_TYPES[detail.get('content_type')].objects.get(pk=detail.get('content_id'))
            Collection_Detail.objects.create(
                content_object=content_object,
                collection=collection,
                amount_used=detail.get('amount')
            )

        super().perform_create(serializer)

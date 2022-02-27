from datetime import datetime, date
from dateutil.relativedelta import relativedelta
from main.models import Client, Collection_Detail, Loan, Loan_Detail, Collection, Transaction
from main.serializers import ClientSerializer, LoanSerializer, CollectionSerializer, CollectionDetailSerializer, TransactionSerializer
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
        net_cash_out = request.data.get('net_cash_out', None)
        loan = Loan.objects.get(pk=pk)
        payment_schedules = []

        if loan_status == 'approved' and net_cash_out:
            amount = loan.principal_amount / loan.term
            principal_amount = loan.principal_amount

            if not loan.is_advance:
                principal_amount = loan.principal_amount + loan.udi
                amount = principal_amount / loan.term

            for cycle in range(0, loan.term):
                running_balance = (principal_amount) - (amount * (cycle + 1))
                if cycle == 0:
                    payment_schedules.append(Loan_Detail(
                        loan=loan,
                        date_payment=loan.start_payment,
                        amount=amount,
                        balance=running_balance
                    ))
                else:
                    date_counter = loan.start_payment + relativedelta(months=cycle)
                    payment_schedules.append(Loan_Detail(
                        loan=loan,
                        date_payment=date_counter,
                        amount=amount,
                        balance=running_balance
                    ))

            Loan_Detail.objects.bulk_create(payment_schedules)
            
            loan.loan_status = loan_status
            loan.net_cash_out = net_cash_out
            loan.date_granted = date.today()

            loan.save()

            # Create a Transaction
            Transaction.objects.create(
                account=Transaction.LIABILITIES,
                description=f"LOAN-{loan.pk} | Maturity Date: {loan.maturity_date} | {loan.client.last_name} {loan.client.first_name}",
                transaction_side=Transaction.CREDIT,
                amount=net_cash_out
            )

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

        # Create a Transaction
        Transaction.objects.create(
            account=Transaction.ASSETS,
            description=f"COLLECTION-{collection.pk}-{collection.reference_code} | {collection.client.last_name} {collection.client.first_name}",
            transaction_side=Transaction.DEBIT,
            amount=collection.collection_amount
        )

        super().perform_create(serializer)


class CollectionDetailViewSet(viewsets.ModelViewSet):
    queryset = Collection_Detail.objects.none()
    serializer_class = CollectionDetailSerializer

    def get_queryset(self):
        return Collection_Detail.objects.all()


class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.none()
    serializer_class = TransactionSerializer

    def get_queryset(self):
        transaction_date = self.request.query_params.get('transaction_date', None)
        start_date = self.request.query_params.get('start_date', None)
        end_date = self.request.query_params.get('end_date', None)

        if transaction_date:
            return Transaction.objects.filter(post_date=transaction_date).order_by('post_date')
        else:
            return Transaction.objects.filter(
                post_date__gte=start_date,
                post_date__lte=end_date
            ).order_by('post_date')

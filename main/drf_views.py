from datetime import datetime, date
from gc import collect
from dateutil.relativedelta import relativedelta
from main.models import Client, Collection_Detail, Loan, Loan_Detail, Collection, Transaction, Refund
from main.serializers import ClientSerializer, LoanSerializer, CollectionSerializer, CollectionDetailSerializer, TransactionSerializer, RefundSerializer
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q


CONTENT_TYPES = {
    'loan_detail': Loan_Detail
}


class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.none()
    serializer_class = ClientSerializer

    def get_queryset(self):
        lastname = self.request.query_params.get('lastname', None)
        if lastname:
            lastname = lastname.strip()
            return Client.objects.filter(
                Q(last_name__istartswith=lastname) | Q(first_name__istartswith=lastname)
            )
        return Client.objects.all()

class LoanViewSet(viewsets.ModelViewSet):
    queryset = Loan.objects.none()
    serializer_class = LoanSerializer


    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
        super().perform_create(serializer)

    def get_queryset(self):
        print(self.request.user)
        lastname = self.request.query_params.get('client_last_name', None)
        loan_status = self.request.query_params.get('loan_status', None)
        client_id = self.request.query_params.get('client_id', None)

        if client_id:
            return Loan.objects.filter(
                client=client_id,
                loan_status='approved'
            ).order_by('date_granted')

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

        if not net_cash_out:
            net_cash_out = loan.net_cash_out

        if loan_status == 'approved' and net_cash_out:
            amount = loan.principal_amount / loan.term
            principal_amount = loan.principal_amount

            if not loan.is_advance:
                principal_amount = loan.principal_amount + loan.udi
                amount = principal_amount / loan.term

            if loan.loan_mode == 'monthly':
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
            else:
                amount = amount / 2
                semi_monthly = loan.term * 2
                for cycle in range(0, semi_monthly):
                    running_balance = (principal_amount) - (amount * (cycle + 1))
                    if cycle == 0:
                        payment_schedules.append(Loan_Detail(
                            loan=loan,
                            date_payment=loan.start_payment,
                            amount=amount,
                            balance=running_balance
                        ))
                    else:
                        date_counter = loan.start_payment + relativedelta(days=cycle*15)
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
                description=f"{loan.control_number} | {loan.client.last_name} {loan.client.first_name}",
                loan=loan,
                transaction_side=Transaction.CREDIT,
                amount=net_cash_out,
                created_by=self.request.user
            )

            # Generate UDI TABLE
            loan.generate_udi_table()

        return Response({'message': 'Loan Approved'}, status=status.HTTP_201_CREATED)


class CollectionViewSet(viewsets.ModelViewSet):
    queryset = Collection.objects.none()
    serializer_class = CollectionSerializer
 
    def get_queryset(self):
        client_id = self.request.query_params.get('client_id', None)

        if client_id:
            return Collection.objects.filter(
                client=client_id,
            ).order_by('-post_date', 'pk')

        return Collection.objects.all()

    def perform_create(self, serializer):
        collection = serializer.save(created_by=self.request.user)
        selected_loans_pk = self.request.data.get('selected_loans', None)

        selected_loans = Loan.objects.filter(pk__in=selected_loans_pk)

        collection_amount = collection.collection_amount
        total_amount_to_pay = 0

        for loan in selected_loans:
            total_amount_to_pay += loan.loan_detail_set.first().amount
            if collection_amount > 0:
                amortization = loan.loan_detail_set.first().amount

                if collection_amount > amortization:
                    if amortization > loan.running_balance:
                        amortization = loan.running_balance

                    Collection_Detail.objects.create(
                        collection=collection,
                        loan=loan,
                        amount_used=amortization
                    )
                    collection_amount = collection_amount - amortization
                elif collection_amount > loan.running_balance:
                    Collection_Detail.objects.create(
                        collection=collection,
                        loan=loan,
                        amount_used=loan.running_balance
                    )
                    collection_amount = collection_amount - loan.running_balance
                else:
                    Collection_Detail.objects.create(
                        collection=collection,
                        loan=loan,
                        amount_used=collection_amount
                    )
                    collection_amount = 0

        if (collection_amount > 0):
            # There is AP for this collection
            collection.refundable_amount = collection_amount
            collection.save()

        collection.total_amount_to_pay = total_amount_to_pay
        collection.save()

        # Create a Transaction
        Transaction.objects.create(
            account=Transaction.ASSETS,
            description=f"COLLECTION-{collection.post_date.strftime('%m/%d/%Y')}-{collection.reference_code} | {collection.client.last_name} {collection.client.first_name}",
            transaction_side=Transaction.DEBIT,
            amount=collection.collection_amount,
            collection=collection,
            post_date=collection.post_date,
            created_by=self.request.user
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
            return Transaction.objects.filter(post_date=transaction_date).order_by('post_date', 'loan__pk', 'collection__pk')
        else:
            return Transaction.objects.filter(
                post_date__gte=start_date,
                post_date__lte=end_date
            ).order_by('post_date', 'loan__pk', 'collection__pk')

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
        super().perform_create(serializer)


class RefundViewSet(viewsets.ModelViewSet):
    queryset = Refund.objects.none()
    serializer_class = RefundSerializer

    def get_queryset(self):
        return Refund.objects.all()

    def perform_create(self, serializer):
        refund = serializer.save(created_by=self.request.user)

        # mark collection as refunded
        refund.collection.is_refunded = True
        refund.collection.save()

        # Create Refund Transaction
        Transaction.objects.create(
            account=Transaction.LIABILITIES,
            description=f"Refund | {refund.collection.client.last_name} {refund.collection.client.first_name}",
            transaction_side=Transaction.CREDIT,
            amount=refund.collection.refundable_amount,
            refund=refund,
            post_date=refund.refund_date,
            created_by=self.request.user
        )

        super().perform_create(serializer)
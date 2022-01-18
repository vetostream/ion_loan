from main.models import Client, Loan
from rest_framework import viewsets
from main.serializers import ClientSerializer, LoanSerializer


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

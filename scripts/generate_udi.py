#!/usr/bin/python3

import os, sys

from decimal import Decimal
from dateutil.relativedelta import relativedelta

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0,BASE_DIR)

os.environ['DJANGO_SETTINGS_MODULE'] = 'loanapp.settings'

import django
django.setup()

from main.models import Loan

# Generating UDI Table
for loan in Loan.objects.filter(client__pk=16):
    # Calculate Loan Factor
    udi_factor = (loan.term * (loan.term + 1)) / 2


    per_month = loan.udi / Decimal(udi_factor)

    udi_table = []
    reversed_term_index = loan.term
    previous_principal = 0.0

    for i in range(1, loan.term+1):
        payment = Decimal(per_month * reversed_term_index)

        date_payment = loan.start_payment + relativedelta(months=i-1)

        if i == loan.term:
            principal = Decimal(0.0)
        else:
            if previous_principal == 0:
                principal = loan.udi - payment
            else:
                principal = previous_principal - payment

        previous_principal = principal
        reversed_term_index -= 1

        udi_table.append((i, round(payment, 2), round(principal, 2), per_month, date_payment.strftime("%B %Y")))

    print(udi_table)
    print("\n\n")

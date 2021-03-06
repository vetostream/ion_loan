import datetime
from enum import unique
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models


class Super_Model(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class Client(Super_Model):
    first_name = models.CharField(max_length=50, null=False)
    middle_name = models.CharField(max_length=50, null=False)
    last_name = models.CharField(max_length=50, null=False)
    address = models.TextField(max_length=300, null=False)
    contact_number = models.CharField(max_length=50, null=False)
    birth_date = models.CharField(max_length=50)
    pension = models.DecimalField(max_digits=10, decimal_places=2)
    sss_no = models.CharField(max_length=150)
    co_maker = models.CharField(max_length=150)


class Loan(Super_Model):
    LOAN_TYPES = [
        ('pension', 'Pension'),
        ('salary', 'Salary')
    ]

    LOAN_STATUS = [
        ('pending', 'Pending'),
        ('declined', 'Declined'),
        ('approved', 'Approved')
    ]

    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    term = models.IntegerField(null=False)
    interest = models.DecimalField(max_digits=5, decimal_places=2, null=False)
    principal_amount = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    date_granted = models.DateField(null=True)
    start_payment = models.DateField(null=True)
    maturity_date = models.DateField(null=True)
    loan_type = models.CharField(max_length=50, choices=LOAN_TYPES, default='pension')
    is_advance = models.BooleanField(default=False)
    loan_status = models.CharField(max_length=50, choices=LOAN_STATUS, default='pending')
    fee_others = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    llrf = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    processing_fee = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    net_cash_out =  models.DecimalField(max_digits=10, decimal_places=2, null=True)


class Collection(Super_Model):
    client = models.ForeignKey(Client, on_delete=models.DO_NOTHING)
    reference_code = models.TextField(max_length=300, null=False)
    collection_amount = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    refundable_amount = models.DecimalField(max_digits=10, decimal_places=2, null=False)


class Collection_Detail(Super_Model):
    collection = models.ForeignKey(Collection, on_delete=models.CASCADE, null=False, related_name="collection_details")
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    amount_used = models.DecimalField(max_digits=10, decimal_places=2, null=False)


class Loan_Detail(Super_Model):
    loan = models.ForeignKey(Loan, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    balance = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    date_payment = models.DateField()
    date_paid = models.DateField(null=True)
    collection_detail = GenericRelation(Collection_Detail)


class Transaction(Super_Model):
    ASSETS = 'assets'
    LIABILITIES = 'liabilities'
    EQUITY = 'equity'

    DEBIT = 'debit'
    CREDIT = 'credit'

    ACCOUNT_TYPES = (
        (ASSETS, 'Assets'),
        (LIABILITIES, 'Liabilities'),
        (EQUITY, 'Equity')
    )

    TRANSACTION_TYPE = (
        (DEBIT, 'Debit'),
        (CREDIT, 'Credit')
    )

    account = models.CharField(max_length=50, choices=ACCOUNT_TYPES, null=False)
    post_date = models.DateField(null=True)
    description = models.CharField(max_length=255, null=False)
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    transaction_side = models.CharField(max_length=10, choices=TRANSACTION_TYPE, null=False)

    def save(self, *args, **kwargs):
        if self.post_date is None:
            self.post_date = datetime.date.today()

        super().save(*args, **kwargs)

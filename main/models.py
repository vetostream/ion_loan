import datetime
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models
import decimal


class Super_Model(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class Client(Super_Model):
    first_name = models.CharField(max_length=50, null=False)
    middle_name = models.CharField(max_length=50, null=True, blank=True)
    last_name = models.CharField(max_length=50, null=False)
    address = models.TextField(max_length=300, null=False)
    contact_number = models.CharField(max_length=50, null=True)
    birth_date = models.CharField(max_length=50, null=True)
    pension = models.DecimalField(max_digits=10, decimal_places=2)
    sss_no = models.CharField(max_length=150, null=True)
    co_maker = models.CharField(max_length=150, null=True, blank=True)
    bank_name = models.CharField(max_length=150, null=True)
    account_number = models.CharField(max_length=150, null=True)


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
    control_number  = models.CharField(max_length=50, null=True)
    loan_type = models.CharField(max_length=50, choices=LOAN_TYPES, default='pension')
    is_advance = models.BooleanField(default=False)
    loan_status = models.CharField(max_length=50, choices=LOAN_STATUS, default='pending')
    fee_others = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    llrf = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    processing_fee = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    udi = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    gross_cash_out =  models.DecimalField(max_digits=10, decimal_places=2, null=True)
    net_cash_out =  models.DecimalField(max_digits=10, decimal_places=2, null=True)
    net_adjustment = models.DecimalField(max_digits=10, decimal_places=2, null=True, help_text="To deduct on net cash out when there is outstanding balance")

    def save(self, *args, **kwargs):
        # calculate UDI
        interest_rate = round(self.interest * self.term, 2)
        self.udi = round((self.principal_amount * interest_rate) / 100, 2)

        # calculate llrf
        self.llrf = round((self.principal_amount / 1000) * (self.term + 1), 2)
        self.processing_fee = round(decimal.Decimal(150.0), 2) #fixed
        self.fee_others = round(decimal.Decimal(0.05) * self.udi, 2)

        total_deductions = round(self.llrf + self.processing_fee + self.fee_others, 2)

        if self.is_advance:
            self.gross_cash_out = round(self.principal_amount - self.udi, 2)
        else:
            self.gross_cash_out = self.principal_amount

        self.net_cash_out = round(self.gross_cash_out - total_deductions, 2)

        if self.net_adjustment:
            self.net_cash_out = round(self.net_cash_out - self.net_adjustment, 2)

        super().save(*args, **kwargs)

class Collection(Super_Model):
    client = models.ForeignKey(Client, on_delete=models.DO_NOTHING)
    reference_code = models.TextField(max_length=300, null=False)
    collection_amount = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    refundable_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    post_date = models.DateField(null=False)


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
    receivable = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    payable = models.DecimalField(max_digits=10, decimal_places=2, null=True)


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

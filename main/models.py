import datetime
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models import Sum
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
    contact_number = models.CharField(max_length=50, null=True, blank=True)
    birth_date = models.CharField(max_length=50, null=True)
    pension = models.DecimalField(max_digits=10, decimal_places=2)
    sss_no = models.CharField(max_length=150, null=True, blank=True)
    co_maker = models.CharField(max_length=150, null=True, blank=True)
    bank_name = models.CharField(max_length=150, null=True, blank=True)
    account_number = models.CharField(max_length=150, null=True, blank=True)

    def __str__(self):
        return f"{self.last_name}, {self.first_name} ({self.birth_date})"


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
    is_cash_advance = models.BooleanField(default=False)
    add_fee_others = models.BooleanField(default=True)
    co_maker = models.CharField(max_length=150, null=True, blank=True)

    def __str__(self):
        return f"{self.control_number} - {self.client.first_name} {self.client.last_name} - {self.principal_amount}"

    def save(self, *args, **kwargs):
        # calculate UDI
        interest_rate = round(self.interest * self.term, 2)
        self.udi = round((self.principal_amount * interest_rate) / 100, 2)

        # calculate llrf
        if not self.is_cash_advance:
            self.llrf = round((self.principal_amount / 1000) * (self.term + 1), 2)
            self.processing_fee = round(decimal.Decimal(150.0), 2) #fixed
            self.fee_others = round(decimal.Decimal(0.05) * self.udi, 2)
        else:
            self.llrf = 0
            self.processing_fee = 0
            self.fee_others = 0

        if not self.add_fee_others:
            self.fee_others = 0

        total_deductions = round(self.llrf + self.processing_fee + self.fee_others, 2)

        if self.is_advance:
            self.gross_cash_out = round(self.principal_amount - self.udi, 2)
        else:
            self.gross_cash_out = self.principal_amount

        self.net_cash_out = round(self.gross_cash_out - total_deductions, 2)

        if self.net_adjustment:
            self.net_cash_out = round(self.net_cash_out - self.net_adjustment, 2)

        super().save(*args, **kwargs)

    @property
    def running_balance(self):
        initial_balance = self.principal_amount

        if not self.is_advance:
            initial_balance += self.udi

        # Check Collection Detail for total amount collected
        total_collections = Collection_Detail.objects.filter(
            loan=self,
        ).aggregate(Sum('amount_used'))

        if not total_collections.get('amount_used__sum', None):
            return initial_balance

        return initial_balance - total_collections['amount_used__sum']


class Collection(Super_Model):
    client = models.ForeignKey(Client, on_delete=models.DO_NOTHING)
    reference_code = models.TextField(max_length=300, null=False)
    collection_amount = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    refundable_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    post_date = models.DateField(null=False)


class Collection_Detail(Super_Model):
    collection = models.ForeignKey(Collection, on_delete=models.CASCADE, null=False, related_name="collection_details")
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True, blank=True)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    content_object = GenericForeignKey('content_type', 'object_id')
    amount_used = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    loan = models.ForeignKey(Loan, on_delete=models.CASCADE, null=True, blank=True)


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

    def __str__(self):
        return f"{self.description} / {self.account} / {self.post_date.strftime('%m/%d/%Y')} / {self.amount} / {self.transaction_side}"

    def save(self, *args, **kwargs):
        if self.post_date is None:
            self.post_date = datetime.date.today()

        super().save(*args, **kwargs)

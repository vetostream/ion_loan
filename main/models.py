from django.contrib.contenttypes.fields import GenericForeignKey
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


class Loan_Detail(Super_Model):
    loan = models.ForeignKey(Loan, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    balance = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    date_payment = models.DateField()
    date_paid = models.DateField(null=True)


class Collection(Super_Model):
    client = models.ForeignKey(Client, on_delete=models.DO_NOTHING)
    reference_code = models.TextField(max_length=300, null=False)
    collection_amount = models.DecimalField(max_digits=10, decimal_places=2, null=False)


class Collection_Detail(Super_Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    amount_used = models.DecimalField(max_digits=10, decimal_places=2, null=False)

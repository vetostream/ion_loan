from django.db import models


class Client(models.Model):
    first_name = models.CharField(max_length=50, null=False)
    middle_name = models.CharField(max_length=50, null=False)
    last_name = models.CharField(max_length=50, null=False)
    address = models.TextField(max_length=300, null=False)
    contact_number = models.CharField(max_length=50, null=False)
    birth_date = models.CharField(max_length=50)
    pension = models.DecimalField(max_digits=10, decimal_places=2)
    sss_no = models.CharField(max_length=150)
    co_maker = models.CharField(max_length=150)


class Loan(models.Model):
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


class Loan_Detail(models.Model):
    loan = models.ForeignKey(Loan, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    balance = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    date_payment = models.DateField()
    date_paid = models.DateField()

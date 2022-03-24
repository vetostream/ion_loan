import json
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import ensure_csrf_cookie
from django.http import FileResponse, JsonResponse
from .models import Transaction, Loan
from django.db.models import Sum
from .utils import generate_to_pdf
from num2words import num2words


@ensure_csrf_cookie
def set_csrf_token(request):
    return JsonResponse({"details": "CSRF cookie set"})

@require_POST
def login_view(request):
    data = json.loads(request.body)
    username = data.get('username')
    password = data.get('password')
    user = authenticate(username=username, password=password)

    if user is not None:
        login(request, user)
        return JsonResponse({"detail": "Success"})

    return JsonResponse({"detail": "Invalid credentials"}, status=400)

@require_POST
def logout_view(request):
    logout(request)
    return JsonResponse({"detail": "Success"})

def check_session(request):
    print(request.user.is_authenticated)
    if request.user.is_authenticated:
        return JsonResponse({"user": request.user.username})

    return JsonResponse({"detail": "No session user"}, status=400)

def cash_flow_statement(request, start_date, end_date=None):
    report_title = "Daily Cash Flow Statement"
    ranged = False

    transactions = Transaction.objects.filter(
        post_date=start_date
    ).order_by('post_date')

    if end_date is not None:
        ranged = True
        report_title = "Ranged Cash Flow Statement"
        transactions = Transaction.objects.filter(
            post_date__gte=start_date,
            post_date__lte=end_date
        ).order_by('post_date')

    total_debit = transactions.filter(transaction_side="debit").aggregate(
        Sum('amount')
    )
    total_credit = transactions.filter(transaction_side="credit").aggregate(
        Sum('amount')
    )

    context = {
        'transactions': transactions,
        'report_title': report_title,
        'total_debit': total_debit,
        'total_credit': total_credit,
        'ranged': ranged,
        'start_date': start_date,
        'end_date': end_date
    }

    pdf = generate_to_pdf("cash_flow_statement.html", context, f"cash-flow-statement-{start_date.strftime('%Y-%m-%d')}")

    return FileResponse(open(pdf, 'rb'), content_type="application/pdf")

def computation_report(request, loan_id):
    loan = Loan.objects.get(pk=loan_id)

    total_deductions = round(loan.udi + loan.llrf + loan.processing_fee + loan.fee_others, 2)
    installment = loan.principal_amount / loan.term
    principal_amount = loan.principal_amount

    if not loan.is_advance:
        total_deductions = round(loan.llrf + loan.processing_fee + loan.fee_others, 2)
        principal_amount = loan.principal_amount + loan.udi
        installment = principal_amount / loan.term

    context = {
        'loan': loan,
        'total_loan_amount': loan.principal_amount + loan.udi,
        'total_deductions': total_deductions,
        'installment': installment
    }

    pdf = generate_to_pdf("computation_report.html", context, f"computation-report-{loan_id}")

    return FileResponse(open(pdf, 'rb'), content_type="application/pdf")

def promissory_report(request, loan_id):
    loan = Loan.objects.get(pk=loan_id)

    total_deductions = round(loan.udi + loan.llrf + loan.processing_fee + loan.fee_others, 2)
    installment = loan.principal_amount / loan.term
    principal_amount = loan.principal_amount

    if not loan.is_advance:
        total_deductions = round(loan.llrf + loan.processing_fee + loan.fee_others, 2)
        principal_amount = loan.principal_amount + loan.udi
        installment = principal_amount / loan.term

    context = {
        'loan': loan,
        'total_loan_amount': loan.principal_amount + loan.udi,
        'total_deductions': total_deductions,
        'installment': installment,
        'principal_amount_words': num2words(loan.principal_amount).upper(),
        'loan_detail': loan.loan_detail_set.all()
    }

    pdf = generate_to_pdf("promissory_report.html", context, f"promissory-report-{loan_id}")

    return FileResponse(open(pdf, 'rb'), content_type="application/pdf")

def disclosure_of_loan(request, loan_id):
    loan = Loan.objects.get(pk=loan_id)
    
    non_financial_charge_total = loan.llrf + loan.processing_fee + loan.fee_others

    installment = loan.principal_amount / loan.term
    principal_amount = loan.principal_amount

    if not loan.is_advance:
        principal_amount = loan.principal_amount + loan.udi
        installment = principal_amount / loan.term

    context = {
        'loan': loan,
        'non_financial_charge_total': non_financial_charge_total,
        'installment': installment
    }

    pdf = generate_to_pdf("disclosure_of_loan.html", context, f"disclosure-form-{loan_id}")
    return FileResponse(open(pdf, 'rb'), content_type="application/pdf")

def retrieve_opening_cash_balance(request, start_date):
    # Fetch Transactions Before start_date
    opening_balance = 0

    debit_transactions = Transaction.objects.filter(
        post_date__lt=start_date,
        transaction_side='debit'
    ).aggregate(Sum('amount'))
    credit_transactions = Transaction.objects.filter(
        post_date__lt=start_date,
        transaction_side='credit'
    ).aggregate(Sum('amount'))

    opening_balance = (debit_transactions['amount__sum'] or 0) - (credit_transactions['amount__sum'] or 0)

    side = 'debit'

    if opening_balance < 0:
        side = 'credit'

    return JsonResponse({'opening_balance': abs(opening_balance), 'side': side}, safe=False)

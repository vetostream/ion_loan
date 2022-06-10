from datetime import datetime
import json
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import ensure_csrf_cookie
from django.http import FileResponse, JsonResponse, HttpResponse
from django.db.models.functions import TruncMonth
from .models import Transaction, Loan, Collection
from django.db.models import Sum
from .utils import generate_to_pdf
from num2words import num2words
from dateutil.relativedelta import relativedelta
import xlsxwriter
from django.conf import settings


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
        'loan_detail': loan.loan_detail_set.all(),
        'name_one': request.GET.get('name_one', ''),
        'name_two': request.GET.get('name_two', ''),
        'name_three': request.GET.get('name_three', '')
    }

    pdf = generate_to_pdf("promissory_report.html", context, f"promissory-report-{loan_id}", page_size='Legal')

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

    # or Folio?
    pdf = generate_to_pdf("disclosure_of_loan.html", context, f"disclosure-form-{loan_id}", page_size='Legal')
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

def loan_masterlist(request, year, month):
    loan_date = datetime.now().replace(year=year, month=month, day=1) + relativedelta(months=1)
    loans = Loan.objects.filter(date_granted__lt=loan_date)

    # We just want the monthly transactions
    offset_date = loan_date.replace(month=month)
    transactions = loans.filter(date_granted__gte=offset_date).order_by('date_granted')

    aggregates = loans.annotate(
        month=TruncMonth('date_granted')).values('month').order_by('-month').annotate(
            total_principal_loan=Sum('principal_amount'),
            total_udi=Sum('udi'),
            total_cashout=Sum('net_cash_out'),
            total_llrf=Sum('llrf'),
            total_pfee=Sum('processing_fee'),
            total_others=Sum('fee_others')
        )

    totals = loans.aggregate(
        total_principal_loan=Sum('principal_amount'),
        total_udi=Sum('udi'),
        total_cashout=Sum('net_cash_out'),
        total_llrf=Sum('llrf'),
        total_pfee=Sum('processing_fee'),
        total_others=Sum('fee_others')
    )

    context = {
        'aggregates': aggregates,
        'totals': totals,
        'loan_date': loan_date.replace(month=month),
        'transactions': transactions
    }

    # or Folio?
    pdf = generate_to_pdf("loan_masterlist.html", context, f"loan-masterlist-{year}", page_size='Legal', orientation="landscape")
    return FileResponse(open(pdf, 'rb'), content_type="application/pdf")

def cashloan_masterlist(request, year, month):
    loan_date = datetime.now().replace(year=year, month=month, day=1) + relativedelta(months=1)
    loans = Loan.objects.filter(date_granted__lt=loan_date, is_cash_advance=True)

    # We just want the monthly transactions
    offset_date = loan_date.replace(month=month)
    transactions = loans.filter(date_granted__gte=offset_date).order_by('date_granted')

    aggregates = loans.annotate(
        month=TruncMonth('date_granted')).values('month').order_by('-month').annotate(
            total_principal_loan=Sum('principal_amount'),
            total_udi=Sum('udi'),
            total_cashout=Sum('net_cash_out'),
            total_llrf=Sum('llrf'),
            total_pfee=Sum('processing_fee'),
            total_others=Sum('fee_others')
        )

    totals = loans.aggregate(
        total_principal_loan=Sum('principal_amount'),
        total_udi=Sum('udi'),
        total_cashout=Sum('net_cash_out'),
        total_llrf=Sum('llrf'),
        total_pfee=Sum('processing_fee'),
        total_others=Sum('fee_others')
    )

    context = {
        'aggregates': aggregates,
        'totals': totals,
        'loan_date': loan_date.replace(month=month),
        'transactions': transactions
    }

    # or Folio?
    pdf = generate_to_pdf("loan_masterlist.html", context, f"cashloan-masterlist-{year}", page_size='Legal', orientation="landscape")
    return FileResponse(open(pdf, 'rb'), content_type="application/pdf")

def cash_receipts_xls(request):
    path = f"{settings.REPORTS_PATH}/cash-receipts.xlsx"
    workbook = xlsxwriter.Workbook(path)
    worksheet = workbook.add_worksheet()

    collections = Collection.objects.order_by('post_date__month', 'post_date__day').values(
        'client__first_name',
        'client__last_name',
        'client__bank_name',
        'collection_amount',
        'refundable_amount',
        'post_date')

    last_date = None

    row_counter = 1

    for collection in collections:
        current_date = collection['post_date']

        if last_date != current_date:
            # Another date, Recreate Headers
            if row_counter != 1:
                row_counter += 4

            worksheet.merge_range(f'A{row_counter}:D{row_counter}', 'D Last Frontier Lending Corporation')
            row_counter += 1
            worksheet.merge_range(f'A{row_counter}:D{row_counter}', 'CASH RECEIPT')
            row_counter += 1
            worksheet.merge_range(f'A{row_counter}:D{row_counter}', current_date.strftime('%m/%d/%Y'))

            row_counter += 1
            worksheet.write(row_counter, 0, "NAME")
            worksheet.write(row_counter, 1, "BANKS")
            worksheet.write(row_counter, 2, "AMOUNT")
            worksheet.write(row_counter, 3, "LOAN")
            worksheet.write(row_counter, 4, "AR")
            worksheet.write(row_counter, 5, "AR")
            worksheet.write(row_counter, 6, "AR")
            worksheet.write(row_counter, 7, "AP")
            row_counter += 2

        worksheet.set_column(row_counter, 0, 25)

        if collection['refundable_amount'] is not None:
            total_loan_amount = collection['collection_amount'] + collection['refundable_amount']
        else:
            total_loan_amount = collection['collection_amount']

        worksheet.write(row_counter, 0, f"{collection['client__last_name']}, {collection['client__first_name']}")
        worksheet.write(row_counter, 1, collection['client__bank_name'])
        worksheet.write(row_counter, 2, collection['collection_amount']) # collected amount
        worksheet.write(row_counter, 3, total_loan_amount) # total loan amount
        worksheet.write(row_counter, 4, "")
        worksheet.write(row_counter, 5, "")
        worksheet.write(row_counter, 6, "")
        worksheet.write(row_counter, 7, collection['refundable_amount'])
        row_counter +=1

        last_date = current_date


    workbook.close()

    return FileResponse(open(path, 'rb'), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

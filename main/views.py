import json
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import ensure_csrf_cookie
from django.http import FileResponse, JsonResponse
from .models import Transaction
from django.db.models import Sum
from .utils import generate_to_pdf

@ensure_csrf_cookie
def set_csrf_token(request):
    return JsonResponse({"details": "CSRF cookie set"})

@require_POST
def login_view(request):
    data = json.loads(request.body)
    username = data.get('username')
    password = data.get('password')
    print(data)
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

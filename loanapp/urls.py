"""loanapp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, register_converter
from datetime import datetime
from rest_framework import routers

from main.drf_views import ClientViewSet, LoanViewSet, CollectionViewSet, CollectionDetailViewSet, RefundViewSet, TransactionViewSet
from main.views import *

router = routers.SimpleRouter()
router.register(r'clients', ClientViewSet)
router.register(r'loans', LoanViewSet)
router.register(r'collections', CollectionViewSet)
router.register(r'collectiondetails', CollectionDetailViewSet)
router.register(r'transactions', TransactionViewSet)
router.register(r'refunds', RefundViewSet)

class DateConverter:
    regex = '\d{4}-\d{2}-\d{2}'

    def to_python(self, value):
        return datetime.strptime(value, '%Y-%m-%d')

    def to_url(self, value):
        return value

register_converter(DateConverter, 'date')

urlpatterns = [
    path('api/v1/', include(router.urls)),
    path('admin/', admin.site.urls),

    # Reports
    path('api/v1/reports/cash_flow_statement/<date:start_date>/<date:end_date>/', cash_flow_statement),
    path('api/v1/functions/calculate_opening_cash/<date:start_date>/', retrieve_opening_cash_balance),
    path('api/v1/reports/cash_flow_statement/<date:start_date>/', cash_flow_statement),
    path('api/v1/reports/computation_report/<int:loan_id>/', computation_report),
    path('api/v1/reports/promissory_report/<int:loan_id>/', promissory_report),
    path('api/v1/reports/disclosure_of_loan/<int:loan_id>/', disclosure_of_loan),
    path('api/v1/reports/loan_masterlist/<int:year>/<int:month>/', loan_masterlist_xls),
    path('api/v1/reports/cashloan_masterlist/<int:year>/<int:month>/', cashloan_masterlist_xls),
    path('api/v1/reports/loan_masterlist_xls/<int:year>/<int:month>/', loan_masterlist_xls),
    path('api/v1/reports/cash_receipts/<int:year>/<int:month>/', cash_receipts_xls),
    path('api/v1/reports/udi_reports/<int:year>/', udi_reports_xls),
    path('api/v1/set_csrf/', set_csrf_token),
    path('api/v1/login/', login_view),
    path('api/v1/logout/', logout_view),
    path('api/v1/check_session/', check_session),
]

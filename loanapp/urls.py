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

from main.drf_views import ClientViewSet, LoanViewSet, CollectionViewSet, CollectionDetailViewSet, TransactionViewSet
from main.views import cash_flow_statement

router = routers.SimpleRouter()
router.register(r'clients', ClientViewSet)
router.register(r'loans', LoanViewSet)
router.register(r'collections', CollectionViewSet)
router.register(r'collectiondetails', CollectionDetailViewSet)
router.register(r'transactions', TransactionViewSet)

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
    path('reports/cash_flow_statement/<date:start_date>/<date:end_date>/', cash_flow_statement),
    path('reports/cash_flow_statement/<date:start_date>/', cash_flow_statement),
]

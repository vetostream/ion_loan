from django.contrib import admin
from main.models import Loan, Loan_Detail, Client, Collection, Collection_Detail, Transaction

admin.site.register(Client)
admin.site.register(Transaction)

class Loan_Detail_Inline(admin.TabularInline):
    model = Loan_Detail

class LoanAdmin(admin.ModelAdmin):
    inlines = [Loan_Detail_Inline]

class Collection_Detail_Inline(admin.TabularInline):
    model = Collection_Detail

class CollectionAdmin(admin.ModelAdmin):
    inlines = [Collection_Detail_Inline]

admin.site.register(Collection, CollectionAdmin)
admin.site.register(Loan, LoanAdmin)

from django.contrib import admin
from main.models import Loan, Loan_Detail, Client, Collection, Collection_Detail, Transaction, Udi_Table

admin.site.register(Client)
admin.site.register(Transaction)
admin.site.register(Collection_Detail)

class Loan_Detail_Inline(admin.TabularInline):
    model = Loan_Detail

class Udi_Table_Inline(admin.TabularInline):
    model = Udi_Table

class LoanAdmin(admin.ModelAdmin):
    list_display = ["client", "loan_type", "term", "interest", "principal_amount", "start_payment", "control_number", "is_advance", "net_cash_out", "gross_cash_out"]
    inlines = [Loan_Detail_Inline, Udi_Table_Inline]
    search_fields = ["control_number", "client__first_name", "client__lastname"]

class Collection_Detail_Inline(admin.TabularInline):
    model = Collection_Detail

class CollectionAdmin(admin.ModelAdmin):
    inlines = [Collection_Detail_Inline]

class Udi_Table_Admin(admin.ModelAdmin):
    list_display = ("loan", "payment", "principal", "date_payment")
    search_fields = ["loan__client__first_name", "loan__client__last_name"]


admin.site.register(Collection, CollectionAdmin)
admin.site.register(Loan, LoanAdmin)
admin.site.register(Udi_Table, Udi_Table_Admin)

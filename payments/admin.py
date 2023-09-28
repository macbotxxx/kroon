from django.contrib import admin
from .models import Payment_Topup
# Register your models here.

@admin.register(Payment_Topup)
class Payment_TopupAdmin (admin.ModelAdmin):
    list_display = ('user', 'payment_ref', 'payment_method', 'amount_paid','currency', 'verified', 'status', 'pending_duration')
    list_display_link = ('user', 'payment_ref', 'payment_method', 'amount_paid', 'verified', 'status')
    readonly_fields = ('created_date', 'modified_date', )

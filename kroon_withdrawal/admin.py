from django.contrib import admin
from .models import Kroon_Withdrawal_Record

@admin.register(Kroon_Withdrawal_Record)
class UserKroon_Withdrawal_RecordMobileMoneyAdmin(admin.ModelAdmin):
    list_display = ('user', 'reference', 'amount',  'currency', 'is_approved', 'status', 'created_date')
    list_display_links = ('user', 'reference','amount',  'currency',  'is_approved', 'status', 'created_date')
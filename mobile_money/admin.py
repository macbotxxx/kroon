from django.contrib import admin
from .models import NetworkProvider, MobileMoneyAccount, MobileMoneyTopUp

# Register your models here.
@admin.register(NetworkProvider)
class NetworkProvider(admin.ModelAdmin):
    list_display = ('network_provider', 'country', 'active')
    list_display_links = ('network_provider', 'country', 'active')


@admin.register(MobileMoneyAccount)
class MobileMoneyAccountAdmin(admin.ModelAdmin):
    list_display = ('user',  'currency','phone_number', 'network', 'created_date', 'modified_date')
    list_display_links = ('user',  'currency','phone_number', 'network', 'created_date', 'modified_date')


@admin.register(MobileMoneyTopUp)
class MobileMoneyTopUpAdmi(admin.ModelAdmin):
    list_display = ('user', 'amount', 'currency', 'email', 'transactional_ref', 'phone_number', 'network')
    list_display_links = ('user', 'amount', 'currency', 'email', 'transactional_ref', 'phone_number', 'network')

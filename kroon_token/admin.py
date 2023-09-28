from django.contrib import admin
from .models import TokenRate, PurchaseTokenFees, WithDrawTokenFees , Currency_Convertion

# Register your models here.

@admin.register(TokenRate)
class TokenRateAdmin(admin.ModelAdmin):
    list_display  = ('currency', 'token_rate', 'created_date', 'modified_date',)
    list_display_links  = ('currency', )

@admin.register(PurchaseTokenFees)
class PurchaseTokenFeesAdmin(admin.ModelAdmin):
    list_display = ('country','operator', 'application_fee', 'vat_fee', 'agent_fee','top_up_limit', 'active',)
    list_display_links = ('country','operator', 'application_fee', 'vat_fee', 'agent_fee','top_up_limit','active',)


@admin.register(WithDrawTokenFees)
class WithDrawTokenFeesAdmin(admin.ModelAdmin):
    list_display = ('country','operator', 'application_fee', 'vat_fee', 'agent_fee','withdrawal_limit','active',)
    list_display_links = ('country','operator', 'application_fee', 'vat_fee', 'agent_fee','withdrawal_limit','active',)


@admin.register(Currency_Convertion)
class Currency_ConvertionAdmin (admin.ModelAdmin):
    list_display = ('default_currency', 'converted_currency', 'convertion_amount', 'convertion_rate')
    list_display_links = ('default_currency', 'converted_currency', 'convertion_amount', 'convertion_rate')
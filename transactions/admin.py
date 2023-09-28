from django.contrib import admin
from .models import Transactions, KroonTokenTransfer, KroonTokenRequest, TransactionalPin, UserRequestToken
from import_export import resources
from import_export.admin import ExportActionMixin

# Register your models here.

@admin.register(Transactions)
class TransactionAdmin(ExportActionMixin, admin.ModelAdmin):
    
    list_display = ('user',  'transactional_id', 'amount',  'action', 'status', 'created_date')

    list_display_links = ('transactional_id','user',)

    readonly_fields = ('created_date', 'modified_date','user', 'benefactor', 'recipient', 'transactional_id', 'flw_ref', 'amount', 'amount_in_localcurrency', 'currency', 'local_currency', 'amount_settled', 'debited_kroon_amount', 'credited_kroon_amount', 'kroon_balance', 'payment_type', 'narration', 'device_fingerprint', 'transactional_date', 'ip_address', 'card', 'card_first_6digits', 'card_last_4digits', 'card_issuer', 'card_country', 'card_type', 'card_expiry', 'action', )

    search_fields = ('transactional_id','card_first_6digits', 'card_last_4digits','user__email')

    list_filter = ('action', 'status',)



@admin.register(KroonTokenTransfer)
class KroonTokenTransferAdmin(admin.ModelAdmin):
    list_display = ('transactional_id', 'sender', 'recipient', 'kroon_token', 'status')
    list_display_links = ('transactional_id', 'sender','recipient', 'kroon_token', 'status')
    readonly_fields = ("transactional_id",'created_date', 'modified_date', )
    


@admin.register(KroonTokenRequest)
class KroonTokenRequestAdmin(admin.ModelAdmin):
    list_display = ('recipient', 'sender', 'transactional_id', 'amount_in_kroon_token', 'status')
    list_display_link = ('recipient', 'sender', 'transactional_id', 'amount_in_kroon_token', 'status')
    readonly_fields = ("transactional_id",'created_date', 'modified_date', )




@admin.register(TransactionalPin)
class TransactionalPinAdmin(admin.ModelAdmin):
    list_display = ('user', 'password')
    list_display_links = ('user', 'password')
    readonly_fields = ('user', 'password', 'created_date', 'modified_date', )

@admin.register(UserRequestToken)
class UserRequestTokenAdmin(admin.ModelAdmin):
    list_display = ('recipient', 'sender', 'transactional_id', 'amount_in_kroon_token', 'wallet_id', 'action', 'status')
    list_display_links = ('recipient', 'sender', 'transactional_id', 'amount_in_kroon_token', 'wallet_id', 'action', 'status')


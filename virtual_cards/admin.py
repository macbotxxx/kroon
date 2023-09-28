from django.contrib import admin
from .models import Virtual_Cards_Details , All_Cards_Transactions
from import_export.admin import ExportActionMixin





@admin.register(Virtual_Cards_Details)
class VirtualCardDetailsAdmin(admin.ModelAdmin):
    list_display = ('card_id','name_on_card','masked_pan','card_type', 'is_active', 'created_date')
    list_display_links = ('card_id','name_on_card','masked_pan',)
    # readonly_fields = ('user', 'card_id', 'account_id', 'amount', 'currency', 'card_hash', 'card_pan', 'masked_pan', 'address', 'city', 'state', 'postal_code', 'cvv', 'expiration', 'send_to', 'bin_check_name', 'card_type', 'name_on_card', 'is_active', 'created_date', 'modified_date', )


@admin.register(All_Cards_Transactions)
class All_Cards_TransactionsAdmin(ExportActionMixin, admin.ModelAdmin):
    
    list_display = ('user',  'transactional_id', 'balance',  'action', 'status', 'created_date')

    list_display_links = ('transactional_id','user',)

    readonly_fields = ('user', 'transactional_id', 'card_id', 'flw_ref', 'gateway_reference', 'balance', 'currency', 'debited_amount', 'credited_amount', 'payment_type', 'narration', 'transactional_date', 'action', 'status')

    search_fields = ('transactional_id','card_first_6digits', 'card_last_4digits','user__email')

    list_filter = ('action', 'status',)
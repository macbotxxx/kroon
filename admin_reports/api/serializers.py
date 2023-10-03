from rest_framework import serializers
from kroon.users.models import User
from transactions.models import Transactions, KroonTokenTransfer , KroonTokenRequest, UserRequestToken


class UserListSerializers(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['name','wallet_id','email','gender','created_date','modified_date',]


class TransactionsListSerializers(serializers.ModelSerializer):

    class Meta:
        model = Transactions
        fields = [
            'transactional_id',
            'amount',
            'currency',
            'amount_in_localcurrency', 
            'local_currency',
            'action',
            'status',
            'created_date',
            'modified_date',
            ]
        
class TransactionDetailsSerializers(serializers.ModelSerializer):
    benefactor = UserListSerializers( read_only=True )
    recipient = UserListSerializers( read_only=True )
    class Meta:
        model = Transactions
        fields = [
            'transactional_id',
            'amount',
            'currency',
            'amount_in_localcurrency', 
            'local_currency',
            'action',
            'status',
            'created_date',
            'modified_date',
            ]
        read_only_fields = ['benefactor', 'recipient', 'transactional_id', 'flw_ref', 'amount', 'amount_in_localcurrency', 'currency', 'local_currency', 'amount_settled', 'debited_kroon_amount', 'credited_kroon_amount', 'kroon_balance', 'payment_type', 'narration', 'device_fingerprint', 'transactional_date', 'ip_address', 'card', 'card_first_6digits', 'card_last_4digits', 'card_issuer', 'card_country', 'card_type', 'card_expiry', 'billing_id', 'billing_name', 'billing_mobile_number', 'billing_email', 'billing_date', 'service_providers', 'action', 'status',]
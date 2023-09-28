from django.core import exceptions
from django.http import request
from rest_framework import serializers
from rest_framework.fields import CurrentUserDefault

from transactions.models import Transactions, KroonTokenTransfer, KroonTokenRequest,  UserRequestToken
from kroon.users.models import User


# MODEL SERIALIZERS START HERE

class UserDetails (serializers.ModelSerializer):
    
    class Meta:
        model = User
        ref_name = "User 1"
        fields = ('id', 'name','wallet_id', 'email', 'merchant_business_name')

class TransactionSerializer (serializers.ModelSerializer):
    user = UserDetails(read_only = True)
    benefactor = UserDetails(read_only = True)
    recipient = UserDetails(read_only = True)

    class Meta:
        model = Transactions
        fields = "__all__"
        read_only_fields = ('user', 'benefactor', 'recipient', 'transactional_id', 'flw_ref', 'amount', 'amount_in_localcurrency', 'currency', 'local_currency', 'amount_settled', 'debited_kroon_amount', 'credited_kroon_amount', 'kroon_balance', 'payment_type', 'narration', 'device_fingerprint', 'transactional_date', 'ip_address', 'card', 'card_first_6digits', 'card_last_4digits', 'card_issuer', 'card_country', 'card_type', 'card_expiry', 'billing_id', 'billing_name', 'billing_mobile_number', 'billing_email', 'billing_date', 'action', 'status', 'transactional_id', 'sender', 'recipient', 'kroon_token', 'action', 'status', 'created_date', 'modified_date', 'id', 'pending_duration')


class TransferTokenHistorySerializer (serializers.ModelSerializer):
    
    class Meta:
        model = KroonTokenTransfer
        fields = "__all__"


class KroonTokenRequestSerializer (serializers.ModelSerializer):
    class Meta:
        model = KroonTokenRequest
        fields = ["amount_in_kroon_token",]

class KroonRequestDetails (serializers.ModelSerializer):
    recipient = UserDetails()
    sender = UserDetails()

    class Meta:
        model = KroonTokenRequest
        fields = "__all__"
        read_only_fields = ('id','recipient', 'sender', 'transactional_id', 'amount_in_kroon_token', 'wallet_id', 'status','created_date', 'modified_date')


class WalletSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id','first_name', 'last_name', 'wallet_id', 'email', 'contact_number', 'merchant_business_name')
        read_only_fields = ['id','first_name', 'last_name','email', 'contact_number', 'merchant_business_name']






# MODEL SERIALIZERS END HERE


CURRENCY_CHOICES = (
    ('NGN', 'NGN'),
    ('SAR', 'SAR'),
    ('GHZ', 'GHZ'),
)

class TokenConvertionSerializer(serializers.Serializer):
    amount = serializers.DecimalField(max_digits = 300, decimal_places = 2)
    currency = serializers.ChoiceField(choices = CURRENCY_CHOICES)


class TransferTokenSerializer (serializers.Serializer):
    kroon_token_ammount = serializers.DecimalField(max_digits = 300, decimal_places = 2)
    wallet_id = serializers.CharField()
    transaction_pin = serializers.CharField()


class TransferTokenDetails (serializers.ModelSerializer):
    sender = UserDetails(read_only = True)
    recipient = UserDetails(read_only = True)

    class Meta:
        model = KroonTokenTransfer
        fields = "__all__"
        read_only_fields = ('id','transactional_id', 'kroon_token', 'status','sender', 'recipient', 'created_date', 'modified_date')


class PayTokenRequestSerializer(serializers.Serializer):
    kroon_token_amount = serializers.DecimalField(max_digits = 300, decimal_places = 2)
    wallet_id = serializers.CharField()
    transactional_id = serializers.CharField()
    transactional_pin = serializers.CharField()


class TransactionPasswordsSerializer(serializers.Serializer):
    pin = serializers.CharField()
    pin_confirm = serializers.CharField()


class ChangerTransactionPinSerializer (serializers.Serializer):
    old_pin = serializers.CharField()
    new_pin = serializers.CharField()
    new_pin2 = serializers.CharField()


class UserKroonTransferSerializer(serializers.ModelSerializer):
    request_pin = serializers.CharField()

    class Meta:
        model = UserRequestToken
        fields = "__all__"
        read_only_fields = ('id','recipient', 'sender', 'transactional_id','action', 'status','accepted_status', 'created_date', 'modified_date',)


class UserTokenTransferDetails (serializers.ModelSerializer):
    sender = UserDetails(read_only = True)
    recipient = UserDetails(read_only = True)

    class Meta:
        model = UserRequestToken
        fields = "__all__"
        read_only_fields = ('id','transactional_id', 'sender', 'amount_in_kroon_token','wallet_id', 'status', 'recipient', 'accepted_status','created_date', 'modified_date')


class DeclineTokenRequestSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserRequestToken
        fields = "__all__"
        read_only_fields = ('id', 'amount_in_kroon_token', 'recipient', 'sender',  'wallet_id', 'action', 'status', 'created_date', 'modified_date')


class AcceptTokenRequestSerializer(serializers.ModelSerializer):
    transactional_pin = serializers.CharField()

    class Meta:
        model = UserRequestToken
        fields = "__all__"
        read_only_fields = ('id',  'wallet_id', 'action',  'recipient', 'sender', 'status', 'created_date','accepted_status', 'modified_date')


class StatementOfAccountSerilizers (serializers.Serializer):
    start_date = serializers.DateField()
    end_date = serializers.DateField()


class CancelFastCheckoutRequestSerializer (serializers.Serializer):
    transactional_id = serializers.CharField()


class Transactional_Pin_Serializer (serializers.Serializer):
    transactional_pin = serializers.CharField()
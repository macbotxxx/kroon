from rest_framework import serializers 
from django.utils.translation import gettext_lazy as _

from kroon_withdrawal.models import  Kroon_Withdrawal_Record
from kroon.users.models import UserBankDetails, User
from mobile_money.models import MobileMoneyAccount


class UserDetails (serializers.ModelSerializer):
    class Meta:
        model = User
        ref_name = "user3"
        fields = ('id','name', 'email', 'wallet_id')

class MobileMoneyAccountDetails (serializers.ModelSerializer):
    class Meta:
        model = MobileMoneyAccount
        ref_name = "mobile_money_user_details_2"
        fields = ('email', 'phone_number', 'network')

class WithdrawRecipientSerializer(serializers.Serializer):
    transactional_pin = serializers.CharField()
    amount = serializers.DecimalField(max_digits = 300, decimal_places = 2)

WITHDRAWAL_TYPE = (
    ('local_bank', _("Local Bank")),
    ('mobile_money', _("Mobile Money")),
)



class UserWithdrawal_RecordSerializer(serializers.ModelSerializer):
    transactional_pin = serializers.CharField()
    withdrawal_type = serializers.ChoiceField(choices=WITHDRAWAL_TYPE)
    amount_in_kroon = serializers.DecimalField(max_digits = 300, decimal_places = 2)
    class Meta:
        model = Kroon_Withdrawal_Record
        fields = "__all__"
        read_only_fields = ('id','user', 'full_name', 'account_number', 'transaction_id', 'bank_name',  'fee', 'currency', 'debit_currency', 'reference', 'billing_full_name', 'billing_email', 'billing_mobile_number', 'billing_recipient_address', 'action', 'is_approved', 'status', 'created_date', 'modified_date', 'beneficiary_name', 'date_requested', 'narration', 'estimated_delivery','settled', 'bank_code', 'recipient_code','paystack_reference')



class BankDetails (serializers.ModelSerializer):
    class Meta:
        model = UserBankDetails
        fields = ("account_name", "account_number", "bank_name", )

class Withdrawal_RecordDetailsSerializer(serializers.ModelSerializer):
    user = UserDetails(read_only = True)
    class Meta:
        model = Kroon_Withdrawal_Record
        fields = "__all__"
        read_only_fields = ('id','user', 'full_name', 'account_number', 'transaction_id', 'bank_name', 'amount', 'fee', 'currency', 'debit_currency', 'reference', 'billing_full_name', 'billing_email', 'billing_mobile_number', 'billing_recipient_address', 'action', 'is_approved', 'status', 'created_date', 'modified_date')


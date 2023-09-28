from rest_framework import serializers
from kroon_token.models import TokenRate,PurchaseTokenFees,WithDrawTokenFees


class TokenRateSerializer(serializers.ModelSerializer):
    class Meta:
        model = TokenRate
        fields = ['token_rate']
       

class PurchaseTokenFeesSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseTokenFees
        fields = ["operator","application_fee", "vat_fee", "top_up_limit", "kroon_transfer_rate", "virtual_card_fees"]

class WithDrawTokenFeesSerializer(serializers.ModelSerializer):
    class Meta:
        model = WithDrawTokenFees
        fields =["operator","application_fee", "vat_fee", "withdrawal_limit", "withdrawal_fee"]
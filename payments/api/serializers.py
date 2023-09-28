from rest_framework import serializers

from payments.models import  Payment_Topup 
from kroon.users.models import User

# MODEL SERIALIZERS START HERE

class UserDetails (serializers.ModelSerializer):
    
    class Meta:
        model = User
        ref_name = "User 1"
        fields = ('id', 'name','wallet_id', 'email', 'merchant_business_name')




class PaymentTopUpSerializer (serializers.ModelSerializer):
    class Meta:
        model = Payment_Topup
        exclude = ('user',)
        read_only_fields = ('id','payment_ref', 'verified','payment_method','currency','action', 'status', 'created_date', 'modified_date', 'settled', 'pending_duration','payment_link','etransac_ref')



class PaymentTopUpVerificationSerializer (serializers.Serializer):

    payment_ref = serializers.CharField()
    amount_paid = serializers.DecimalField(max_digits = 300, decimal_places = 2)


class CancelPaymentRequestSerializer(serializers.Serializer):
    
    payment_ref = serializers.CharField()
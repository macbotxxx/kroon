from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from kroon_gift.models import KroonGift
from kroon.users.models import User

class UserDetails(serializers.ModelSerializer):
    class Meta:
        model = User
        ref_name = "user4"
        fields = ('name', 'email', 'wallet_id')

class KroonGiftSerializer(serializers.Serializer):
    transactional_pin = serializers.CharField()
    email = serializers.EmailField()
    amount = serializers.DecimalField(max_digits = 300, decimal_places = 2)
    redeem_pin = serializers.CharField()


class RedeemKroonGift(serializers.Serializer):
    email = serializers.EmailField()
    redeem_pin = serializers.CharField()
    transactional_pin = serializers.CharField()


class KroonGiftInfoSerializer(serializers.Serializer):
    email = serializers.EmailField()

class GiftDetails(serializers.ModelSerializer):
    user = UserDetails(read_only = True)
    class Meta:
        model = KroonGift
        fields = ('user','email','amount','settled','transactional_id','created_date', 'modified_date',)
        


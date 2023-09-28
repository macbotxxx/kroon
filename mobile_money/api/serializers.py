from rest_framework import serializers
from mobile_money.models import NetworkProvider, MobileMoneyAccount, MobileMoneyTopUp
from locations.models import Country
from kroon.users.models import User

class CountryDetails(serializers.ModelSerializer):
    class Meta:
        model = Country
        ref_name = "mobile_money_country_details"
        fields = ('id','name', 'phone_code')


class UserDetails (serializers.ModelSerializer):
    class Meta:
        model = User
        ref_name = "user2"
        fields = ('id','name', 'email', 'wallet_id')

class NetworkProviderSerializer(serializers.ModelSerializer):
    country = CountryDetails(read_only = True)
    class Meta:
        model = NetworkProvider
        fields = "__all__"
        read_only_fields = ('id','network_provider', 'country', 'active', 'created_date', 'modified_date')


class MobileMoneyAccountSerializer(serializers.ModelSerializer):
    # network = serializers.UUIDField(required=False)
    class Meta:
        model = MobileMoneyAccount
        fields = "__all__"
        read_only_fields = ('id','user', 'currency','created_date', 'modified_date',)

    # def get_validation_exclusions(self):
    #     exclusions = super(MobileMoneyAccountSerializer, self).get_validation_exclusions()
    #     return exclusions + ['network']


class MobileAccountDetails (serializers.ModelSerializer):
    user = UserDetails(read_only = True)
    network = NetworkProviderSerializer(read_only = True)
    class Meta:
        model = MobileMoneyAccount
        fields = "__all__"
        read_only_fields = ('id','user', 'currency','network','phone_number','email','client_ip','device_fingerprint', 'created_date', 'modified_date')


class MobileMoneyTopUpSerializer(serializers.ModelSerializer):
    user = UserDetails(read_only = True)
    class Meta:
        model = MobileMoneyTopUp
        fields = "__all__"
        read_only_fields = ('id','user', 'amount', 'currency', 'email', 'transactional_ref', 'phone_number', 'network','created_date', 'modified_date',)
        

class MobileMoneyTopUpSerializerForm(serializers.ModelSerializer):
    transactional_pin = serializers.CharField()
    class Meta:
        model = MobileMoneyTopUp
        fields = "__all__"
        read_only_fields = ('id','user',  'currency', 'email', 'transactional_ref', 'phone_number', 'created_date', 'modified_date',)


    
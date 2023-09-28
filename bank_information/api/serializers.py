from rest_framework import serializers


class Accoount_number_Serializer (serializers.Serializer):

    account_number = serializers.CharField()
    bank_code = serializers.CharField()
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
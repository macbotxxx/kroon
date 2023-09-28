from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from drf_writable_nested.serializers import WritableNestedModelSerializer

from kiosk_agreements.models import Business_Agreements , Agreements_Info , Shares_Signatures , Shares_Agreements, Goods_And_Services_Agreement , Loan_Agreement



class BusinessAgreementsSerializer (serializers.ModelSerializer):
    
    class Meta:
        model = Business_Agreements
        exclude = ['modified_date',]


class AgreementsInfoSerializer (serializers.ModelSerializer):
    
    
    class Meta:
      model = Agreements_Info
      exclude = ['user','modified_date',]
      read_only_fields = ['id','created_date']


class SharesSignaturesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Shares_Signatures
        exclude = ['modified_date',]
        read_only_fields = ['id','agreements','created_date']


class SharesAgreementSerializer(serializers.ModelSerializer):
    share_holders = SharesSignaturesSerializer( many = True  , required = False )
    class Meta:
        model = Shares_Agreements
        exclude = ['user','modified_date',]
        read_only_fields = ['id','created_date']



class GoodsAndServicesAgreementSerailizer (serializers.ModelSerializer):
    class Meta:
        model = Goods_And_Services_Agreement
        exclude = ['user','modified_date',]
        read_only_fields = ['id','created_date']


class Loan_AgreementSerailizer (serializers.ModelSerializer):
    class Meta:
        model = Loan_Agreement
        exclude = ['user','modified_date',]
        read_only_fields = ['id','created_date']








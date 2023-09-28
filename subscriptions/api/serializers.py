from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from subscriptions.models import Subscription_Plan ,Merchant_Subcribers

class Gov_Promo_Code_Serializer(serializers.Serializer): 
    promo_code = serializers.CharField()



class In_App_Sub_check (serializers.Serializer):
    DEVICE_TYPE = (
        ('apple', _('apple')),
        ('google', _('google')),
        ('huawei', _('huawei')),
    )

    device_type = serializers.ChoiceField(
        choices=DEVICE_TYPE,
        required=True,
        help_text=_('this indicates the merchants device type , ether its an apple or google device type')
    )

    receipt_data = serializers.CharField( required = True,
        help_text=_('the users receipt data is required for verification')
                                         
         )
    
    subcription_id = serializers.CharField( 
        help_text=_('the users receipt data is required for verification')
                                         
         )
    
    
    # def get_cleaned_data(self):
    #     return {
    #         'device_type': self.validated_data.get('device_type'),
    #         'receipt_data': self.validated_data.get('receipt_data'),
    #     }
    

class In_App_Sub_Migrate (serializers.Serializer):
    DEVICE_TYPE = (
        ('apple', _('apple')),
        ('google', _('google')),
        ('huawei', _('huawei')),
    )

    device_type = serializers.ChoiceField(
        choices=DEVICE_TYPE,
        required=True,
        help_text=_('this indicates the merchants device type , ether its an apple or google device type')
    )

    receipt_data = serializers.CharField( required = True,
        help_text=_('the users receipt data is required for verification')
                                         
         )
    
    subcription_id = serializers.CharField( 
        help_text=_('the users receipt data is required for verification')
                                         
         )
    
    exp_date = serializers.DateTimeField( 
        help_text=_('this indicate when the plan is meant to expire')
                                         
         )
    
    product_id = serializers.CharField( 
        help_text=_('the users receipt data is required for verification')
                                         
         )
    
    yearly_product_id = serializers.CharField( 
        help_text=_('the users receipt data is required for verification')
                                         
         )



class MerchantSubSerializer(serializers.ModelSerializer):
    class Meta:
        model = Merchant_Subcribers
        fields = ['sub_plan_id']

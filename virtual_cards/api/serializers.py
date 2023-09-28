from dataclasses import field
from locale import currency
from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from virtual_cards.models import Virtual_Cards_Details , All_Cards_Transactions


PAYMENT_METHOD = (
    ("card" , _("card")),
    ("kroon" , _("kroon")),
)

CURRENCY_CHOICES = (
    ("USD" , _("USD")),
    ("NGN" , _("NGN")),
)

CARD_DESIGN = (
    ("Design_1" , _("Design_1")),
    ("Design_2" , _("Design_2")),
    ("Design_3" , _("Design_3")),
    ("Design_4" , _("Design_4")),
)



class Create_Virtual_Cards_Serializers (serializers.Serializer):

    payment_method = serializers.ChoiceField( choices=PAYMENT_METHOD )
    currency = serializers.ChoiceField( choices=CURRENCY_CHOICES)
    payment_ref = serializers.CharField( required=False )
    card_design = serializers.ChoiceField( choices=CARD_DESIGN )


class User_Virtual_Cards (serializers.ModelSerializer):
    
    class Meta:
        model = Virtual_Cards_Details
        fields = ('card_id', 'account_id', 'amount', 'currency', 'card_hash','card_design', 'card_pan','card_design', 'masked_pan',  'cvv', 'expiration',  'card_type', 'name_on_card', 'block','is_active', 'created_date')



class Initiate_Payment_Serializer (serializers.Serializer):
    
    amount = serializers.DecimalField(max_digits= 300, decimal_places = 2)
    currency = serializers.ChoiceField( choices=CURRENCY_CHOICES)


class Fund_Virtual_Card_Serializer (serializers.Serializer):

    payment_method = serializers.ChoiceField( 
        choices=PAYMENT_METHOD,
        help_text=_("the set the payment method that will be used to fund the virtual card")

     )
     
    amount = serializers.DecimalField(
        max_digits= 300, decimal_places = 2,
        help_text=_("the amount to fund the virtual card with.")
        )

    payment_ref = serializers.CharField( 
        required=False,
        help_text=_("this is optional but also required if the payment_method is selected to be card ")
        
         )


class Card_Transaction_Serializer (serializers.ModelSerializer):

    class Meta:
        model = All_Cards_Transactions
        fields = ( 'card_id','gateway_reference', 'currency', 'debited_amount', 'credited_amount', 'payment_type', 'narration', 'transactional_date', 'action', 'status', 'created_date')
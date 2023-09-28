from django.db import models
from django.utils.translation import gettext_lazy as _
from helpers.common.basemodel import BaseModel

from locations.models import Country



class TokenRate (BaseModel):

    currency = models.OneToOneField(
        Country, on_delete = models.CASCADE,
        verbose_name=_('currency'),
        null=True, unique = True,
        help_text=_("currency of which the country rate should be calculated.")
    )

    token_rate = models.PositiveIntegerField(
        verbose_name=_('Token Rate'),
        null=True,
        help_text=_("The token rate for each currency")
    )

    class Meta:
        ordering = ('created_date',)
        verbose_name = _('Token Rate')
        verbose_name_plural = _('Token Rate')

    def __str__(self):
        return str(self.currency)

OPERATORS = (
    ('card topup', _('Card Topup')),
    ('agent topup', _('Agent TopUp')),
)

WITHDRAW_OPERATORS = (
    ('bank withdrawal', _('Bank Withdrawal')),
    ('agent cashout', _('Agent Cashout')),
    ('mobile money cashout', _('Mobile Money Cashout')),
)



class PurchaseTokenFees (BaseModel):

    operator = models.CharField(
        choices=OPERATORS,
        verbose_name=_('Operators'),
        null=True,
        max_length=300,
        help_text=_("this section hold the operator which the current fees should be applied to.")
        )
    
    application_fee = models.DecimalField(
        verbose_name=_("Application Fees"),
        null=True, max_length=3,
        default=0.00,
        max_digits = 300, decimal_places = 2,
        help_text=_("identify the application fees for the current rate.")
    )

    vat_fee = models.DecimalField(
        verbose_name=_("Vat Fees"),
        null=True, max_length=3,
        default=0.00,
        max_digits = 300, decimal_places = 2,
        help_text=_("the vat fee for any transaction which will be calculated with the kroon token amount and application fees.")
    )

    kroon_transfer_rate = models.DecimalField(
        verbose_name=_("Kroon Transfer Rate"),
        null=True, max_length=3,
        default=0.00,
        max_digits = 300, decimal_places = 2,
        help_text=_("this is the transfer rate for any transaction which will be calculated with the kroon token amount ")
    )

    virtual_card_fees = models.DecimalField(
        verbose_name=_("Virtual Card Fees"),
        null=True, max_length=3,
        default=0.00,
        max_digits = 300, decimal_places = 2,
        help_text=_("this is the virtual card fees for creating a virtual card for the merchant user, this fees is meant to the be set in the a trading currency i:e USD or AUD and many more  ")
    )

    agent_fee = models.CharField(
        verbose_name=_("Agent Fees"),
        null=True,blank=True, max_length=3,
        help_text=_("the agent fee should take place when ever an agent is meant to handle kroon token request. which will be added along side with vat fees  and application fees.")
    )

    top_up_limit = models.CharField(
        verbose_name=_("Top Up Limit"),
        null = True, blank=True,
        max_length=10,
        help_text=_("this holds the topup limitation for the each country.")
    )

    country = models.ForeignKey(
        Country,
        verbose_name=_("Country of Residence"),
        blank=True, null=True,
        on_delete=models.CASCADE,
        help_text=_("The country residence of the customer. KYC verification will be applied to this country and customer must provide proof of such residence as relevant in the country of jurisdiction.")
    )

    active = models.BooleanField(
        verbose_name=_("Active"),
        default=False,null=True,
        help_text=_("active status determines whether fees and vat fees are active or not.")
        )

    def __str__(self):
        return str(self.operator)

    class Meta:
        ordering = ('-created_date',)
        verbose_name = _("Purchase Kroon Token Fee")
        verbose_name_plural = _("Purchase Kroon Token Fee")

    

class WithDrawTokenFees (BaseModel):

    operator = models.CharField(
        choices=WITHDRAW_OPERATORS,
        verbose_name=_('Withdraw Operators'),
        null=True,
        max_length=300,
        help_text=_("this section hold the withdrawal operator which the current fees should be applied to.")
        )
    
    application_fee = models.DecimalField(
        verbose_name=_("Application Fees"),
        null=True,max_length=4,
        default=0.00,
        max_digits = 300, decimal_places = 2,
        help_text=_("identify the application fees for the current rate, this is also known as the CASHOUT FEES.")
    )

    vat_fee = models.DecimalField(
        verbose_name=_("Vat Fees"),
        null=True,max_length=4,
        default=0.00,
        max_digits = 300, decimal_places = 2,
        help_text=_("the vat fee for any transaction which will be calculated with the kroon token amount and application fees.")
    )

    withdrawal_fee = models.DecimalField(
        verbose_name=_("Withdrawal Fee"),
        null=True,max_length=4,
        default=0.00,
        max_digits = 300, decimal_places = 2,
        help_text=_("the withdrawal fee for any transaction which will be calculated with the initial amount fee before the withdrawal process.")
    )

    agent_fee = models.CharField(
        verbose_name=_("Agent Fees"),
        null=True,blank=True,max_length=4,
        help_text=_("the agent fee should take place when ever an agent is meant to handle kroon token request. which will be added along side with vat fees  and application fees.")
    )

    withdrawal_limit = models.DecimalField(
        verbose_name=_("Withdrawal Limit"),
        null = True, blank=True,
        default=0.00,
        max_digits = 300, decimal_places = 2,
        help_text=_("this holds the Withdrawal limitation for the each country.")
    )

    country = models.ForeignKey(
        Country,
        verbose_name=_("Country of Residence"),
        blank=True, null=True,
        on_delete=models.CASCADE,
        help_text=_("The country residence of the customer. KYC verification will be applied to this country and customer must provide proof of such residence as relevant in the country of jurisdiction.")
    )

    active = models.BooleanField(
        verbose_name=_("Active"),
        default=False,null=True,
        help_text=_("active status determines whether fees and vat fees are active or not.")
        )
    def __str__(self):
        return str(self.operator)

    class Meta:
        ordering = ('-created_date',)
        verbose_name = _("Withdraw Kroon Token Fee")
        verbose_name_plural = _("Withdraw Kroon Token Fee")



class Currency_Convertion (BaseModel):
    """
    Currencies convertion rate store the rate of a given currency
    for not it is set to use ZAR as default....
    """

    default_currency = models.CharField(
        verbose_name=_("Default Currency"),
        null=True,blank=True,max_length=4,
        help_text=_("this is set to be the default currency which will be converted using the conversion currency")
    )

    converted_currency = models.CharField(
        verbose_name=_("Converted Currency"),
        null=True,blank=True,max_length=4,
        default="USD",
        help_text=_("the converted currency will be set to the default currency which will be converted to")
    )

    convertion_amount = models.DecimalField(
        verbose_name=_("Convertion Amount"),
        null = True, blank=True,
        default=1.00,
        max_digits = 300, decimal_places = 2,
        help_text=_("this holds the convertion amount for each country.")
    )

    convertion_rate = models.DecimalField(
        verbose_name=_("Convertion Rate"),
        null = True, blank=True,
        default=0.00,
        max_digits = 300, decimal_places = 3,
        help_text=_("this holds the convertion rate for each country.")
    )

    def __str__(self):
        return str(f'{self.default_currency} converted to {self.converted_currency}')
    
    class Meta:
        ordering = ('-created_date',)
        verbose_name = _('Currencies Convertion') 
        verbose_name_plural = _('Currencies Convertion') 


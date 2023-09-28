from datetime import timezone
from datetime import timedelta, datetime
from locale import currency
from django.utils import timezone
from django.db import models
from kroon.users.models import User, UserBankDetails
from django.utils.translation import gettext_lazy as _
from helpers.common.basemodel import BaseModel
from django.core.files import File
from PIL import Image, ImageDraw

from helpers.common.payment import PayStack, FlutterWave
from transactions.models import Transactions

import secrets
# import qrcode
# import qrcode.image.svg
from io import BytesIO

TRANSACTION_STATUS = (
        ('pending', _('Pending')),
        ('sent', _('Sent')),
        ('cancelled', _('Cancelled')),
        ('declined', _('Declined')),
        ('rejected', _('Rejected/Refused')), 
        ('received', _('Received')), 
        ('successful', _('Successful')),
        ('failed', _('failed')),
    )


class Payment_Topup (BaseModel):
    """
    Payement model for accepting orders.
    """

    user = models.ForeignKey(
        User,
        verbose_name=_("User Profile"),
        on_delete=models.CASCADE, null=True,
        related_name = "topup_users",
        help_text=_("The user for whom account belongs to")
    )

    payment_ref = models.CharField(
        verbose_name = _("Payment Ref No"),
        max_length = 50,
        null=True,
        help_text=_("The payment identification number sent from the payment gateway.")
    )

    payment_method = models.CharField(
        verbose_name = _("Payment Method"),
        default = "ONLINE PAYMENT",
        max_length = 150,
        null=True,
        help_text=_("The payment method used while paying for an order.")
    )

    # etransac functionality
    payment_link = models.URLField(
        verbose_name=_("Payment Link"),
        null=True,
        blank=True,
        help_text=_("this shows the payment url link ,if only the client is set to use the etransac functionalities.")
    )

    etransac_ref = models.CharField(
        verbose_name = _("Etransac Payment Ref "),
        max_length = 100,
        null=True,
        blank=True,
        help_text=_("this shows the payment ref that is will returned by the payment gateway.")
    )

    # etransac functionality end

  
    amount_paid = models.DecimalField(
        verbose_name = _("Amount Paid"),
        null=True,
        max_digits = 300, decimal_places = 2,
        help_text=_("Amount paid for the above order by the customer.")
    )

    amount_in_kroon = models.DecimalField(
        verbose_name = _("Kroon Amount Paid"),
        null=True,
        max_digits = 300, decimal_places = 2,
        help_text=_("Amount paid for the above order by the customer.")
    )

    currency = models.CharField(
        verbose_name = _("Payment Currency"),
        max_length=4, null =True,
        help_text = _("payment currency is the currency code for the user while making payment")
        
    )

    verified = models.BooleanField(
        verbose_name = _("Payment Verification"),
        default = False,
        null=True,blank=True,
        help_text=_("Verified payment status to identify if the payment is been verified by the payment gateway or not.")
    )

    action = models.CharField(
        verbose_name = _("Payment Method"),
        default = "KROON WALLET TOPUP",
        max_length = 150,
        null=True,
        help_text=_("The payment action for the current transaction.")
    )

    status = models.CharField(
        choices = TRANSACTION_STATUS,
        verbose_name = _("Payment Status"),
        max_length = 255, default = "pending", 
        null=True,
        help_text=_("payment status to identify if the payment is been verified by the payment gateway or not.")
    )

    pending_duration =  models.DateTimeField(
        verbose_name=_("Pending Topup Duration"),
        null=True,
        default=timezone.now,
        help_text = _("duration of which the pending topup will be expired if no action is not been take.")
    )

    settled = models.BooleanField(
        verbose_name = _("Payment Settled"),
        null = True, default = False,
        help_text = _("this indicates whether the payment is been settled or not.")
    )


    def __str__(self):
        return str(self.payment_ref)

    
    def save(self, *args, **kwargs) -> None:
        while not self.payment_ref:
            payment_ref = self.payment_ref
            object_with_similar_ref = Payment_Topup.objects.filter(payment_ref=payment_ref)
            if not object_with_similar_ref:
                payment_ref = secrets.token_urlsafe(30)
                self.payment_ref = payment_ref

        self.pending_duration += timedelta(minutes=2)
        super().save(*args, **kwargs)

    def amount_value(self) -> int:
        return self.amount_paid * 100 

    # def verify_payment_paystack(self):
    #     paystack = PayStack()
    #     status, result = paystack.verify_payment_paystack(self.payment_ref, self.amount_paid)
       
    #     if status:
    #         if result['amount'] / 100 == self.amount_paid:
    #             self.verified = True
    #             self.status = 'successful'
                
    #         self.save()
    #         amount = result['amount'] / 100
            

    #         transaction_record = Transactions.objects.get( transactional_id = result['reference'] )

    #         # inputting the records for identification
    #         # transaction_record.device_fingerprint = result['device_fingerprint']
    #         transaction_record.ip_address = result['ip_address']
    #         transaction_record.payment_type = result['channel']
    #         transaction_record.transactional_date = result['created_at']
    #         transaction_record.amount_settled = amount
    #         transaction_record.status = "successful"
    #         transaction_record.billing_id = result['customer']['id']
    #         if result['customer']['first_name'] is not None:
    #             transaction_record.billing_name = result['customer']['first_name'] + "  "+ result['customer']['last_name']
    #             transaction_record.billing_mobile_number = result['customer']['phone']
    #         transaction_record.billing_email = result['customer']['email']
    #         transaction_record.billing_date = result['createdAt']
    #         transaction_record.service_providers = "Paystack"
            
    #         if result['channel'] == 'card':
    #             """
    #             this section saves the card read only information
    #             """
    #             transaction_record.card = True
    #             transaction_record.card_first_6digits = result['authorization']['bin']
    #             transaction_record.card_last_4digits = result['authorization']['last4']
    #             transaction_record.card_issuer = result['authorization']['bank']
    #             transaction_record.card_country = result['authorization']['country_code']
    #             transaction_record.card_type = result['authorization']['card_type']
    #             transaction_record.card_expiry = result['authorization']['exp_month'] + ' ' + result['authorization']['exp_year']
    #         transaction_record.save()

    #     if self.verified:
    #         return True
    #     return False 


    def verify_payment_flutterwave (self):
        # paystack = PayStack()
        platform = None
        flutterwave = FlutterWave()
        status, result = flutterwave.verify_payment_flutterwave( self.payment_ref, self.amount_paid )
        if status == 'success':
            self.verified = True
            self.status = result['status']
            self.amount_paid = result['amount']
            try:
                transaction_record = Transactions.objects.get( transactional_id = result['tx_ref'] )
                # inputting the records for identification
                transaction_record.flw_ref = result['flw_ref']
                transaction_record.device_fingerprint = result['device_fingerprint']
                transaction_record.ip_address = result['ip']
                transaction_record.payment_type = result['payment_type']
                transaction_record.transactional_date = result['created_at']
                transaction_record.amount_settled = result['amount_settled']
                transaction_record.status = result['status']
                transaction_record.billing_id = result['customer']['id']
                transaction_record.billing_name = result['customer']['name']
                transaction_record.billing_mobile_number = result['customer']['phone_number']
                transaction_record.billing_email = result['customer']['email']
                transaction_record.billing_date = result['customer']['created_at']
                transaction_record.service_providers = "flutterwave"
                
                if result['payment_type'] == 'card':
                    """
                    this section saves the card read only information
                    """
                    transaction_record.card = True
                    transaction_record.card_first_6digits = result['card']['first_6digits']
                    transaction_record.card_last_4digits = result['card']['last_4digits']
                    transaction_record.card_issuer = result['card']['issuer']
                    transaction_record.card_country = result['card']['country']
                    transaction_record.card_type = result['card']['type']
                    transaction_record.card_expiry = result['card']['expiry']
                transaction_record.save()

            except Transactions.DoesNotExist:
                platform = 'virtual_card'
                pass

        self.save()
        if self.verified:
            if platform == 'virtual_card':
                response={'verified':self.verified , 'amount':result['amount'] , 'currency':result['currency']}
                return response
            else:
                return True
        return False 


    class Meta:
        ordering = ('-created_date',)
        verbose_name = _("All TopUp Payment")
        verbose_name_plural = _("All TopUp Payment")
from django.db import models

# Create your models here.
from django.db import models
from django.utils.translation import gettext_lazy as _
from helpers.common.basemodel import BaseModel
from kroon.users.models import  User



# Create your models here.

class Recipient_Record (BaseModel):
    """
    This recipient record stores the neccessary imformation that is used
    for withdrawal process which is been carried out by our third party
    providers and thats PAYSTACK
    the recipient record is meant to be a one time saved record , the models
    shows the required information for the withdrawal process.
    this record is required by PAYSTACK
    """

    user = models.ForeignKey(
        User,
        verbose_name=_("User Profile"),
        on_delete=models.CASCADE,null=True,
        related_name = "recipient_user",
        help_text=_("The user for whom account belongs to")
    )

    integration_id = models.CharField(
        verbose_name=_("Integration ID"),
        max_length=255,
        null=True, blank=True,
        help_text=_("this is the integration ID which is stored for reference purpose")
    )

    recipient_code =  models.CharField(
        verbose_name=_("Recipient Code"),
        max_length=255,
        null=True, blank=True,
        help_text=_("the recipient code is stored and used for withdrawal purpose. which is meant to be unique to per user and also its an auto generated code from the third party.")
    )

    def __str__(self):
        return str(self.user)

    class Meta:

        ordering = ('-created_date',)
        verbose_name = _("Recipient Record")
        verbose_name_plural = _("Recipient Record")
    


class Kroon_Withdrawal_Record (BaseModel):

    """
    FLUTTERWAVE WITHDRAWAL METHOD
    Flutterwave allows you to initiate single and bulk transfers to bank accounts and make transfers to vendors all from your Flutterwave account. 
    the transfer record models is ocnsist of local bank withdrawal and mobile money transfer 

    this is withdrawal method is also set for PAYSTACK and flutterwave
    """
    user = models.ForeignKey(
        User,
        verbose_name=_("User Profile"),
        on_delete=models.CASCADE,null=True,
        help_text=_("The user for whom account belongs to")
    )

    full_name = models.CharField(
        verbose_name=_("Full Name"),
        max_length=255,
        null=True, blank=True,
        help_text=_("full name of the current user used for transfer.")
    )

    account_number = models.CharField(
        verbose_name=_("Account Number"),
        max_length=255,
        null=True, blank=True,
        help_text=_("Account number is been used to identify the users account, which can be the bank issued number to the user for local bank withdrawal and when it comes to mobile money withdrawl the account number field will be replace by the mobile number.")
    )

    beneficiary_name = models.CharField(
        verbose_name=_("Beneficiary Name"),
        max_length=255,
        null=True, blank=True,
        help_text=_("the beneficary name of the user that want to perform the withdrawal note this will only be inputted if the user has stored his or her account details for withdrawal")
    )

    recipient_code = models.CharField(
        verbose_name=_("Recipient code Record"),
        max_length=150,
        null=True, blank=True,
        help_text=_("the recipent ref noumber is provided by the third party providers , which will be used to initiate the local bank or mobile money transfer.")
    )

    transaction_id = models.CharField(
        verbose_name=_("transaction ID"),
        max_length=255,
        null=True, blank=True,
        help_text=_("transactional id is the unique identifier of the transaction which will be provided by the payment gateway for easy verification and comfirmation of a transaction.")
    )

    bank_name = models.CharField(
        verbose_name=_("Moble Money - Bank Name"),
        max_length=255,
        null=True, blank=True,
        help_text=_("Bank name used for mobile money accounts and local bank withdrawal bank name")
    )

    bank_code = models.CharField(
        verbose_name=_("Bank Name Code"),
        max_length=255,
        null=True, blank=True,
        help_text=_("Bank name used for mobile money accounts")
    )

    amount = models.DecimalField(
        max_digits = 300, decimal_places = 2,
        verbose_name=_("Amount"),
        max_length=255,null=True,
        help_text=_("amount of withdrawal which the user initiated to be withdrawed to his or her account.")
    )

    amount_in_kroon = models.DecimalField(
        max_digits = 300, decimal_places = 2,
        verbose_name=_("Amount In Kroon"),
        max_length=255,null=True,
        help_text=_("amount in kroon of withdrawal which the user initiated to be withdrawed to his or her account.")
    )

    fee = models.DecimalField(
        max_digits = 300, decimal_places = 2,
        verbose_name=_("Fees Amount"),
        max_length=255,null=True,
        blank=True,
        help_text=_("the initial fees for that transaction which the user initiated to be withdrawed to his or her account.")
    )

    currency = models.CharField(
        verbose_name=_("Currency"),
        max_length=255,null=True,
        help_text=_("currency of withdrawal request by the user defualt currency type.")
    )

    debit_currency = models.CharField(
        verbose_name=_("Debit Currency"),
        max_length=255,null=True,
        blank=True,
        help_text=_("currency of withdrawal request by the user defualt currency type.")
    )

    reference = models.CharField(
        verbose_name=_("Reference"),
        max_length=255,null=True,
        help_text=_("this holds the reference to the current transaction request.")
    )

    paystack_reference = models.CharField(
        verbose_name=_("Paystack Reference"),
        max_length=255,null=True,
        blank=True,
        help_text=_("this holds the reference issued from paystack to the current transaction request by the customer.")
    )

    billing_full_name = models.CharField(
        verbose_name=_("Billing Full Name"),
        max_length=255,null=True,blank=True,
        help_text=_("Billing full name of the user.")
    )

    billing_email = models.EmailField(
        verbose_name=_("Billing Email"),
        max_length=255,null=True,blank=True,
        help_text=_("This is the email address of the transfer recipient")
    )

    billing_mobile_number = models.CharField(
        verbose_name=_("Billing Phone Number"),
        max_length=255,null=True,blank=True,
        help_text=_("This is the mobile number of the recipient. If the recipient's email address is passed, this becomes an optional parameter.")
    )

    billing_recipient_address = models.TextField(
        verbose_name=_("Billing Address"),
        null=True,blank=True,
        help_text=_("This is the address of the transfer recipient.")
    )

    action = models.CharField(
        verbose_name=_("Action"),
        max_length=255, null=True,
        help_text=_("this indicate which transfer was taken place ether with card or mobile")
    )

    is_approved = models.BooleanField(
        verbose_name=_("Withdrawal Approved"),
        null=True, default=False,
        help_text=_("indicates if the withdrawal has been approved or not .")
    )


    status = models.CharField(
        verbose_name=_("Status"),
        null=True, 
        max_length =50,
        help_text=_("initiate a withdraw which indicates if it is true or false.")
    )

    withdrawal_type = models.CharField(
        verbose_name=_("Withdrawal Type"),
        max_length = 300,
        null=True, blank=True,
        help_text=_("this indicates the withdrawal type the user initiated to use.")
    )

    date_requested = models.DateField(
        verbose_name=_("Date Requested"),
        null=True, blank=True,
        help_text=_("this indicates the actual date the user initiated the withdrawal.")
    )

    estimated_delivery = models.DateField(
        verbose_name=_("Estimated Delivery Date"),
        null=True, blank=True,
        help_text=_("this indicates the actual date the user  withdrawal was suubmitted.")
    )

    narration = models.CharField(
        verbose_name=_("Narration"),
        max_length=255,null=True,
        blank=True,
        help_text=_("transactional narration which is used to pass the message to the third party, reasons for the withdrawal.")
    )

    settled = models.BooleanField(
        verbose_name=_("Settled"),
        default=False, null =True,
        blank=True,
        help_text=_("this helps in indicating if the transaction is been settled or not.")
    )

    
   
    def __str__(self):
        return str(self.user)

    class Meta:

        ordering = ('-created_date',)
        verbose_name = _("All Withdrawals")
        verbose_name_plural = _("All Withdrawals")




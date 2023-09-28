from django.db import models
from django.utils.translation import gettext_lazy as _
from helpers.common.basemodel import BaseModel
# from kroon.users.models import User

from django.conf import settings
User = settings.AUTH_USER_MODEL

# Create your models here.

TRANSACTION_STATUS = (
        ('pending', _('Pending')),
        ('sent', _('Sent')),
        ('cancelled', _('Cancelled')),
        ('declined', _('Declined')),
        ('rejected', _('Rejected/Refused')), 
        ('received', _('Received')), 
        ('successful', _('Successful')),
        ('processing', _('Processing')),
        ('failed', _('failed')),
    )

TITLE = (
        ("Mr" , _("Mr")),
        ("Mrs" , _("Mrs")),
    )

GENDER = (
    ("M" , _("M")),
    ("F" , _("F")),
)


CARD_DESIGN = (
    ("Design_1" , _("Design_1")),
    ("Design_2" , _("Design_2")),
    ("Design_3" , _("Design_3")),
    ("Design_4" , _("Design_4")),
)



class Virtual_Cards_Details ( BaseModel ):
    """
    this stores the details of a virtual card created by the user
    """


    user = models.ForeignKey(
        User,
        verbose_name=_("User Profile"),
        on_delete=models.CASCADE, related_name=('user_virtual_card'),
        null =True,blank=True,
        help_text=_("The user for whom account belongs to")
    )

    card_id = models.CharField(
        verbose_name=_('Card ID'),
        max_length=50,
        null=True, blank=True,
        help_text=_(""" This is the card identification number which is unique for each user virtual card  """)
    )

    card_design = models.CharField(
        choices = CARD_DESIGN,
        verbose_name=_('Card Design'),
        max_length=50,
        null=True, blank=True,
        help_text=_(""" This is the card design selected by the user   """)
    )

    account_id = models.CharField(
        verbose_name=_('Account ID'),
        max_length=50,
        null=True, blank=True,
        help_text=_(""" This is the account identification number which is unique for each user virtual card  """)
    )

    amount = models.DecimalField(
        verbose_name = _("Amount"),
        null=True,
        max_digits = 300, decimal_places = 2,
        default=0.00,
        help_text=_(""" The total amount associated with the virtual card """)
    )

    currency = models.CharField(
        verbose_name=_('Currency'),
        max_length=10,
        null=True, blank=True,
        help_text=_(""" This is the currency the card would be denominated in. Expected values include NGN and USD. """)
    )

    card_hash = models.CharField(
        verbose_name=_('Card Hash'),
        max_length=50,
        null=True, blank=True,
        help_text=_(""" Cryptographic hash functions seem to be an ideal method for protecting and securely storing credit card numbers in ecommerce and payment applications.  """)
    )

    card_pan = models.CharField(
        verbose_name=_('Card Pan'),
        max_length=50,
        null=True, blank=True,
        help_text=_(""" A payment card number, primary account number (PAN), or simply a card number, is the card identifier found on payment cards, such as credit cards and debit  """)
    )

    masked_pan = models.CharField(
        verbose_name=_('Masked Card Pan'),
        max_length=50,
        null=True, blank=True,
        help_text=_(""" Card Pan masking hides a portion of the long card number, or PAN, on a credit or debit card, protecting the card account numbers when displayed or printed  """)
    )

    address = models.CharField(
        verbose_name=_('Address'),
        max_length=250,
        null=True, blank=True,
        help_text=_(""" This is the registered address for the card. e.g. Your house address where you would receive your card statements. """)
    )

    city = models.CharField(
        verbose_name=_('City'),
        max_length=250,
        null=True, blank=True,
        help_text=_(""" This is the city registered with the card, it makes up part of the address the customer used for their card. """)
    )

    state = models.CharField(
        verbose_name=_('State'),
        max_length=50,
        null=True, blank=True,
        help_text=_(""" This is the State/County/Province/Region registered with the card. It is a two letter word representing the state in the billing country e.g CA, NY  """)
    )

    postal_code = models.CharField(
        verbose_name=_('Postal Code'),
        max_length=7,
        null=True, blank=True,
        help_text=_(""" This is the zip code or postal card registered with the card.  """)
    )

    cvv = models.CharField(
        verbose_name=_('Cvv'),
        max_length=3,
        null=True, blank=True,
        help_text=_(""" A card security code is a series of numbers that, in addition to the bank card number, is printed on a card. The CSC is used as a security feature for card not present transactions, where a personal identification number cannot be manually entered by the cardholder.  """)
    )

    expiration = models.CharField(
        verbose_name=_('expiration'),
        max_length=20,
        null=True, blank=True,
        help_text=_(""" Expiration dates appear on the front or back of a credit card in a two-digit month/year format. Credit cards expire at the end of the month written on the card. For example, a credit card's expiration date may read as 11/24, which means the card is active through the last day of November 2024  """)
    )

    send_to = models.CharField(
        verbose_name=_('Send To'),
        max_length=100,
        null=True, 
        blank=True,
        help_text=_(""" this indicates who the card will be shipped to from the company card issuer """),
    )

    bin_check_name = models.CharField(
        verbose_name=_('Bin Check Name'),
        max_length=200,
        null=True, 
        blank=True,
        help_text=_(""" BIN Checker is designed to instantly verify, validate & check the BIN (Bank Identification Number) on the updated free BIN database. The tool fetches the card issuer details and facilitates in identifying the issuing bank by the card. It tells which bank and its branch issued that card. """),
    )

    card_type = models.CharField(
        verbose_name=_('Card Type'),
        max_length=100,
        null=True, 
        blank=True,
        help_text=_(""" Card Type means any card we issue under the Visa, MasterCard, or any other card acceptance scheme """),
    )

    name_on_card = models.CharField(
        verbose_name=_('Name On Card'),
        max_length=200,
        null=True, 
        blank=True,
        help_text=_(""" Refers to the person who owns a credit or debit card. The cardholder name is the name of the owner, printed on the front of the card. """),
    )

    block = models.BooleanField(
        verbose_name = _("Card Block"),
        default = False,
        null = True,
        blank = True,
        help_text = _(""" This indicates if the card is block or not """),

    )

    is_active = models.BooleanField(
        verbose_name = _("Card Active"),
        default = False,
        null = True,
        blank = True,
        help_text = _(""" This indicates if the card is still active or not """),

    )

    def __str__(self):
        return str(self.user)

    class Meta:
        ordering = ('-created_date',)
        verbose_name=_(" User Virtual Cards Details ")
        verbose_name_plural =_(" User Virtual Cards Details ")




class All_Cards_Transactions (BaseModel):
    """
    model list of transactions that currently took place 
    """

    user = models.ForeignKey(
        User,
        verbose_name=_("User Profile"),
        on_delete=models.CASCADE, related_name='user_virtual_card_transactions',
        null =True,blank=True,
        help_text=_("The user for whom account belongs to")
    )

    # saving the transactional reference here 
    transactional_id = models.CharField(
        verbose_name= _("Transactional ID"),
        null=True, max_length=355,
        editable=False,
        help_text = _("Transaction identifier that belongs to the customer")
    )

    card_id = models.CharField(
        verbose_name=_('Card ID'),
        max_length=50,
        null=True, blank=True,
        help_text=_(""" This is the card identification number which is unique for each user virtual card  """)
    )

    flw_ref = models.CharField(
        verbose_name= _("Third Party Ref"),
        null=True, max_length=355,
        editable=False, blank=True,
        help_text = _("the theird party ref is the transactional ref which is generated by kroon topup third party.")
    )

    gateway_reference = models.CharField(
        verbose_name= _("Gateway Reference"),
        null=True, max_length=355,
        editable=False, blank=True,
        help_text = _("the transaction gateway reference , which is provided to specify the card transactions ")
    )

    # having the amount both on kroon and user local currency
    # note this hold the amount credited and debited as well 
    balance = models.DecimalField(
        verbose_name = _("Amount "),
        null=True,
        max_digits = 300, decimal_places = 2,
        default=0.00,
        help_text=_("the total amount of the virtual card ")
    )

    currency =  models.CharField (
        verbose_name = _("Kroon Currency"),
        max_length = 300, 
        null=True,
        help_text=_("Transactional currency message that was taken by the customer.")
    )

    debited_amount = models.DecimalField(
        verbose_name = _("Debited Amount"),
        null=True, blank=True,
        max_digits = 300, decimal_places = 2,
        default=0.00,
        help_text=_("debited amount taken by the customer.")
    )

    credited_amount = models.DecimalField(
        verbose_name = _("Credited Amount"),
        null=True, blank=True,
        max_digits = 300, decimal_places = 2,
        default=0.00,
        help_text=_("created amount taken by the customer.")
    )

    payment_type = models.CharField (
        verbose_name = _("Payment Type"),
        max_length = 300, 
        null=True,blank=True,
        help_text=_("the payment type which will be provided by the third party after the transaction has been approved.")
    )

    narration = models.CharField (
        verbose_name = _("Transaction Message"),
        max_length = 300, 
        null=True,
        help_text=_("Transactions message that was taken by the customer.")
    )

    transactional_date = models.DateTimeField (
        verbose_name = _("Transactional Date"),
        null=True, blank=True,
        help_text=_("the transactional date which holds the date the transaction was taken by our third party providers.")
    )

    action = models.CharField(
        verbose_name = _("Action"),
        max_length = 300,
        null=True, 
        help_text=_("action status for the current transaction.")
    )

    status = models.CharField(
        choices = TRANSACTION_STATUS,
        verbose_name = _("Transaction Status"),
        default='pending', max_length = 20,
        null=True,
        help_text=_("action status for the current transaction, which determines if it successful or not.")
    )


    def __str__(self):
        return str(self.user)

    class Meta:
        ordering = ['-created_date']
        verbose_name = _("All Transactions")
        verbose_name_plural = _("All Transactions")
        













from django.db import models
from kroon.users.models import User, UserBankDetails
from django.utils.translation import gettext_lazy as _
from helpers.common.basemodel import BaseModel
from locations.models import Country


# Create your models here.

class NetworkProvider(BaseModel):
    network_provider = models.CharField(
        verbose_name= _("Network Provider"),
        max_length= 70, null =True,
        help_text=_("this input receives network provider allowed in the users country.")
    )

    country = models.ForeignKey(
        Country, on_delete=models.CASCADE,
        null = True, 
        help_text=_("country that this network provider is allowed in")
        )

    active = models.BooleanField(
        verbose_name = _("Active"),
        null = True, default = False,
        help_text = _("this indicates whether the network provider is active or not")
    )

    def __str__(self):
        return str(self.network_provider)

    class Meta:
        ordering = ('-created_date',)
        verbose_name = _("Mobile Money Network Provider")
        verbose_name_plural = _("Mobile Money Network Provider")


class MobileMoneyAccount (BaseModel):
    
    user = models.ForeignKey(
        User,
        verbose_name=_("User Profile"),
        on_delete=models.CASCADE, null=True,
        help_text=_("The user for whom account belongs to")
    )

    
    currency = models.CharField(
        verbose_name=_("Currency"),
        max_length = 255,null=True,
        help_text=_("this is the defualt currency for the user mobile money account.")
    )

    email = models.EmailField(
        verbose_name= _("Email Address"),
        null = True,
        help_text=_("email address for the current user") 
    )

    phone_number = models.CharField(
        verbose_name= _("UserPhone Number"),
        max_length=25,null=True,
        help_text=_("the user phone number which is registered for the mobile money service.")

    )

    network = models.ForeignKey(
        NetworkProvider, on_delete = models.CASCADE, 
        null=True, blank=True,
        help_text=_("mobile money network providers which is only accepted for countries like Ghana, Zambia.")
    )

    withdrawal_code = models.CharField(
        verbose_name= _("Account Code"),
        max_length=255,
        null=True, blank=True,
        default = "MPS",
        editable=False,
        help_text=_("The withdrawal code is used when the user requested for a mobile money withdrawal, for countries like Uganda, Zambia and Rwanda , while making use of the network providers during mobile money withdrawal for Ghana.")
    )

    
    def __str__(self):
        return str(self.user)

    class Meta:
        ordering = ('-created_date',)
        verbose_name = _("Mobile Money Users Account")
        verbose_name_plural = _("Mobile Money Users Account")



class MobileMoneyTopUp (BaseModel):
    user = models.ForeignKey(
        User,
        verbose_name=_("User Profile"),
        on_delete=models.CASCADE, null=True,
        help_text=_("The user for whom account belongs to")
    )

    amount = models.FloatField(
        verbose_name=_("Amount"),
        null=True,
        help_text=_("The amount funded by the user using mobile money")
    )

    currency = models.CharField(
        verbose_name=_("Currency"),
        null=True, max_length = 255,
        help_text=_("Currency used for mobile money topup by the user")
    )

    email = models.EmailField(
        verbose_name=_("Email"),
        null=True, max_length = 255,
        help_text=_("Email used for mobile money topup by the user")
    )

    transactional_ref = models.CharField(
        verbose_name=_("Transactional Reference"),
        null=True, max_length = 255,
        help_text=_("Transactional refrence for the current payment initiated by the user")
    )

    phone_number = models.CharField(
        verbose_name= _("Phone Number"),
        null=True, max_length=255, 
        help_text=_("the current phone number used to initiate the mobile money transaction")
    )

    network = models.CharField(
        verbose_name= _("Network Provider"),
        null=True, max_length=255,
        blank=True,
        help_text=_("mobile money network provider used")
    )

    def __str__(self):
        return str(self.user)

    class Meta:
        ordering = ('-created_date',)
        verbose_name = _("Mobile Money TopUp")
        verbose_name_plural = _("Mobile Money TopUp")
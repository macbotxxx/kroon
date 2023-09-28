from django.db import models

# Create your models here.
from django.utils.translation import gettext_lazy as _
from helpers.common.basemodel import BaseModel
from locations.models import Country
from kroon.users.models import User


class KroonGift(BaseModel):
    user = models.ForeignKey(
        User,
        verbose_name=_("User Profile"),
        on_delete=models.CASCADE, null=True,
        related_name=_("kroon_gift_sender"),
        help_text=_("The user for whom account belongs to")
    )

    country = models.ForeignKey(
        Country,
        verbose_name=_("Gift Country"),
        blank=True, null=True,
        on_delete=models.CASCADE,
        help_text=_("The country residence of the customer. kroon gift can only be accepted by a user from the same country with the sender")
    )
    
    email = models.EmailField(
        verbose_name=_("Email"),
        null=True,
        help_text=_("this email field hold the users email address which will be verified during registration so note user can only gift kroon token to unregistered users.")
    )

    amount = models.DecimalField(
        verbose_name=_("Amount In Kroon"),
        null=True,
        max_digits = 300, decimal_places = 2,
        help_text=_("the amount in kroon token to be sent the user.")
    )

    redeem_pin = models.CharField(
        verbose_name=_("Redeem Pin"),
        max_length=255,
        null=True,
        help_text=_("the redeem pin is set to be used when verifying a gift token which on successful operation the amount will be sent to the user.")
    )

    settled = models.BooleanField(
        verbose_name=_("Kroon Gift Settled"),
        default=False, null =True,
        help_text=_("this indicates whether the gift token is used by the user or not")
    )

    transactional_id = models.CharField(
        verbose_name= _("Transactional ID"),
        null=True, max_length=355,
        editable=False,
        help_text = _("Transaction identifier that belongs to the customer")
    )

    def __str__(self):
        return str(self.email)

    class Meta:
        ordering = ('-created_date',)
        verbose_name = _("Gift Kroon")
        verbose_name_plural = _("Gift Kroon")
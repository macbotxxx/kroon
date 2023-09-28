from django.db import models
from django.utils.translation import gettext_lazy as _

from helpers.common.basemodel import BaseModel
from subscriptions.models import Subscription_Plan
from kroon.users.models import User

# Create your models here.


class Government_Promo_Code (BaseModel):
    
    user = models.ForeignKey(
        User,
        verbose_name=_("User Profile"),
        on_delete=models.CASCADE, null=True,
        blank=True,
        related_name="promotinoal_code_user",
        help_text=_("The user for whom account belongs to")
    )

    code_plan = models.ForeignKey(
        Subscription_Plan, on_delete = models.PROTECT,
        null=True, blank=True,
        related_name = 'code_plans',
        help_text=_("the code plans represents the plan in which the promotional code will be linked to")
    )

    promo_code = models.CharField(
        verbose_name = _("Promo Code"),
        max_length = 255,
        null=True, blank=True,
        help_text=_("the promotional code which represents the code for the given plan , this code activates the plan when is not used.")
    )

    yearly_code = models.BooleanField(
        verbose_name = _("Yearly Code"),
        null=True,
        blank=True,
        default=False,
        help_text=_("the indicates if the promo code is a yearly code or not")
    )

    used_code = models.BooleanField(
        verbose_name = _("Used Code"),
        null = True,
        default = False,
        help_text = _("this hsows if the code is been used by another customer or already expired.")
    )

   

    def __str__(self):
        return str(self.code_plan)

    class Meta:
        ordering = ('-created_date',)
        verbose_name = _("Government Promo Code")
        verbose_name_plural = _("Government Promo Code")




class Discount_Code (BaseModel):
    
    user = models.ForeignKey(
        User,
        verbose_name=_("User Profile"),
        on_delete=models.CASCADE, null=True,
        blank=True,
        related_name="gov_discount_code_user",
        help_text=_("The user for whom account belongs to")
    )

    discount_code = models.CharField(
        verbose_name = _("Discount Code"),
        max_length = 255,
        null=True, blank=True,
        help_text=_("the discount code which applies a discount price to the  actual subscription")
    )

    used_code = models.BooleanField(
        verbose_name = _("Used Code"),
        null = True,
        default = False,
        help_text = _("this hsows if the code is been used by another customer or already expired.")
    )


    def __str__(self):
        return str(self.discount_code)

    class Meta:
        ordering = ('-created_date',)
        verbose_name = _("Discount Code")
        verbose_name_plural = _("Discount Code")


        
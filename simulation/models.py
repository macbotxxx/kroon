from django.db import models
from django.utils.translation import gettext_lazy as _

from helpers.common.basemodel import BaseModel
from kroon.users.models import User
# Create your models here.

class Simulate_Account (BaseModel):
    
    user = models.ForeignKey(
        User,
        verbose_name=_("User Profile"),
        on_delete=models.CASCADE, null=True,
        related_name="simuator_onboarding_user",
        help_text=_("The user for whom account belongs to")
    )
    
    country_iso2 = models.CharField(
        verbose_name = _("Country ISO2"),
        max_length = 2,
        null = True,
        help_text=_("this stores the country iso2 value for identification for the onboarding process")
    )

    number_of_merchants = models.IntegerField(
        verbose_name=_("Number of Merchants"),
        null=True,
        help_text=_('this holds the number of merchants that will be onboarded for that particular country using the above iso2 value for identification for the onboarding process.')
    )

    action_count = models.IntegerField(
        verbose_name=_("Action Count"),
        null=True,
        default=0,
        help_text=_('this stores the account creation count.')
    )


    submitted = models.BooleanField(
        verbose_name=_('submitted'),
        null=True,
        default=False,
        help_text=_('this indicates whether the action is submitted successfully')
    )

    processing_status = models.BooleanField(
        verbose_name=_('processing status'),
        null=True,
        default=False,
        help_text=_('this indicates whether the action is processing status successfully')
    )

    completed = models.BooleanField(
        verbose_name=_('completed'),
        null=True,
        default=False,
        help_text=_('this indicates whether the action is completed successfully')
    )

    def __str__(self):
        return f"{self.number_of_merchants} of merchants in the {self.country_iso2}"
    
    class Meta:
        ordering = ('-created_date',)
        verbose_name = _('simulated merchants')
        verbose_name_plural = _('simulated merchants')
    

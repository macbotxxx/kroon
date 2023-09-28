import os

from django.db import models
from django.utils.translation import gettext_lazy as _

from helpers.common.basemodel import BaseModel
from kroon.users.models import User




# Create your models here.

class Mask_Statement_Of_Account (BaseModel):

    """
    masking statement of account, having the original informaton been masked.
    """

    user = models.ForeignKey(
        User,
        verbose_name=_("User Profile"),
        on_delete=models.CASCADE, null=True,
        help_text=_("The user for whom account belongs to")
    )

    masked_id = models.CharField(
        verbose_name=_("Masked User Profile"),
        max_length=255, null=True,
        help_text=_("this masked the user information to the public, to prevent crosssite scripting, note this is will be temporal.")  
    )

    start_date = models.DateField(
        verbose_name=_("Start Date"),
        null=True, 
        help_text=_("this specified the start date of the statement of account")
    )

    end_date = models.DateField(
        verbose_name=_("End Date"),
        null=True, 
        help_text=_("this specified the end date of the statement of account")
    )

    def __str__(self):
        return str(self.user)

    class Meta:
        ordering = ('-created_date',)
        verbose_name = _("Masked Statement Of Account")
        verbose_name_plural = _("Masked Statement Of Account")



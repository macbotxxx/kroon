from django.db import models
from django.utils.translation import gettext_lazy as _
from helpers.common.basemodel import BaseModel
from kroon.users.models import User


class Generate_Pin (BaseModel):
    user = models.ForeignKey(
        User,
        verbose_name=_("Generator Profile"),
        on_delete=models.CASCADE,
        help_text=_("The user that is currently sending kroon token.")
    ) 

    pin = models.CharField(
        verbose_name=_("Pin"),
        max_length = 4,
        null=True,
        help_text=_("this is the generated pin for the user to enable the user to recieve token request offers which is a one time pin.")
    )

    def __str__(self):
        return str(self.pin)

    class Meta:
        ordering = ('-created_date',)
        verbose_name = _("Generated Pin")
        verbose_name_plural = _("Generated Pin")



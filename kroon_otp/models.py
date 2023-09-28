from django.db import models
from django.utils.translation import gettext_lazy as _
from helpers.common.basemodel import BaseModel
import string
import datetime
from datetime import timedelta, datetime
from django.utils import timezone

from kroon.users.models import User
# Create your models here.

class OPTs (BaseModel):

    email = models.EmailField(
        verbose_name= _("Email Address"),
        null=True, blank=True,
        help_text=_("The email address of the requester")
    )

    otp_code = models.CharField(
        verbose_name = _("Opt Code"),
        max_length = 255, null = True,
        help_text = _("opt code that will be sent to the user for validation and resting of transactional pin.")
    )

    duration = models.DateTimeField(
        verbose_name=_("Opt Duration"),
        null=True, default=timezone.now,
        help_text = _("duration of which the opt will be expired from been used ny the user , which a new opt will be sent to the user to obtain a new opt token.")
    )

    active = models.BooleanField(
        verbose_name = _("OTP Active"),
        default = True, null=True,
        help_text = _("This status indicates whether otp is still active or not")
    )

    def __str__(self):
        return str(self.email)

    # adding 5 mins to thw otp section 
    def save(self, *args, **kwargs):
        self.duration += timedelta(minutes=5)
        super(OPTs, self).save(*args, **kwargs)

    class Meta:
        ordering = ('-created_date',)
        verbose_name = _("Otp Token")
        verbose_name_plural = _("Otp Token")



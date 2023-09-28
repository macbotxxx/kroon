from django.db import models
from django.utils.translation import gettext_lazy as _
from helpers.common.basemodel import BaseModel
from kroon.users.models import User

# Create your models here.
class Workers_Logs (BaseModel):
    """
    this store the logs for the workers this is only access by the machants of the company.
    """

    merchant_account  = models.ForeignKey(
        User,
        verbose_name=_("Merchant Profile"),
        on_delete=models.CASCADE, null=True,
        related_name="merchant_account",
        help_text=_("The user for whom the business belongs to , in other words the merchant profile")
    )

    worker_account = models.ForeignKey(
        User,
        verbose_name=_("Worker Profile"),
        on_delete=models.CASCADE, null=True,
        related_name='worker_account',
        help_text=_("this have the worker profile associated with the current merchant profile")
    )

    login_time = models.DateTimeField(
        verbose_name=_("Login Time Record"),
        blank=True, null=True,
        help_text=_("The time at which the account will be logged in.")
    )

    logout_time = models.DateTimeField(
        verbose_name=_("Logout Time Record"),
        blank=True, null=True,
        help_text=_("The time at which the account will be logged out.")
    )

    def __str__(self):
        return str(self.merchant_account)

    class Meta:
        ordering = ('-created_date',)
        verbose_name = _('Workers Logs')
        verbose_name_plural = _('Workers Logs')


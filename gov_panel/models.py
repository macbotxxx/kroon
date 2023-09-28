import os
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import pre_delete
from django.dispatch.dispatcher import receiver
from django.core.files.storage import default_storage as storage 

from helpers.common.basemodel import BaseModel
from subscriptions.models import Subscription_Plan
from django.conf import settings

User = settings.AUTH_USER_MODEL


class Onboarding_Users_CSV(BaseModel):

    on_boarding_user = models.ForeignKey(
        User,
        verbose_name=_("Gov Profile"),
        on_delete=models.CASCADE,
        related_name = "gov_users",
        null=True , blank=True,
        help_text=_("this is the gov user account that provides the current user information for on boarding")
    )

    on_boarding_user_file = models.FileField(
        verbose_name=_("Onboarding User File"),
        upload_to='onboarding_users/',
        null=True, blank=False,
        help_text=_("csv format file which is used for the onboarding of uses by the gov user profile ")
    )

    on_boarding_complete = models.BooleanField(
        verbose_name=_("Completed Onboarding"),
        default=False,
        help_text=_("Flag to determine if customer has completed onboarding process.")
    )

    on_boarding_complete_date = models.DateTimeField(
        verbose_name=_("Onboarding Complete Date"),
        blank=True, null=True,
        help_text=_("Timestamp when customer completed onboarding process.")
    )


    def __str__(self):
        return str(self.on_boarding_user)

    class Meta:
        ordering = ('-created_date',)
        verbose_name = _("Onboarding CSV Format")
        verbose_name_plural = _("Onboarding CSV Format")


# Delete the CSV file  

def _delete_file(path):
    # Deletes file from filesystem.
    if os.path.isfile(path):
        os.remove(path)

@receiver(pre_delete, sender=Onboarding_Users_CSV)
def delete_img_pre_delete_post(sender, instance, *args, **kwargs):
    if instance.on_boarding_user_file:
        _delete_file(instance.on_boarding_user_file.name)

# Delete the CSV file  


class Action_logs ( BaseModel ):
    """
    The action log for gov workers is set to record every 
    action that is taken by the gov worker.
    """
    user = models.ForeignKey(
        User,
        verbose_name=_("Gov Worker Profile"),
        on_delete=models.CASCADE,
        related_name = "gov_worker_profile",
        null=True , blank=True,
        help_text=_("this is the gov user account that provides the current user information for on boarding")
    )

    action = models.CharField(
        verbose_name=_('Actions'),
        max_length=255,
        null=True,
        blank=True,
        help_text=_("Actions holds the current user intractions with the gov dashboard.")
    )

    def __str__(self):
        return str(self.action)
    
    class Meta:
        ordering = ('-created_date',)
        verbose_name = _('Worker Action Log')
        verbose_name_plural = _('Worker Action Log')


class Government_Organizations ( BaseModel ):
    """
    This features is only activated for Nigerian merchants only.
    this helps the system to identify if the merchant is
    running a registered government business or not.
    """

    government_organization = models.CharField(
        verbose_name = _("Government Organization Name"),
        max_length=100,
        null = True,
        blank = True,
        unique=True,
        help_text = _("The government organization name holds the title name of the organisation that the merchant business is registered under")
    )

    def __str__(self):
        return str( self.government_organization ) 
    
    class Meta:
        ordering = ('-created_date',)
        verbose_name = _('Government Organizations')
        verbose_name_plural = _('Government Organizations')


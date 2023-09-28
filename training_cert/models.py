import random
import string

from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

from helpers.common.basemodel import BaseModel
from kroon.users.models import User
from locations.models import Country
# Create your models here.

def ref_code():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))


class Training_Cert (BaseModel):
    """
    this store the training certificate for the given user
    """

    PLATFORMS = (
        ('kroon_app', _('Kroon app')),
        ('Kroon_kiosk', _('Kroon kiosk')),
    )

    user = models.ForeignKey(
        User,
        verbose_name=_("User Profile"),
        on_delete=models.CASCADE, null=True,
        related_name="training_cert_worker",
        help_text=_("The user for whom account belongs to")
    ) 

    cert_number = models.CharField(
        verbose_name= _("Certificate Number"),
        max_length=255,
        null = True,
        blank=True,
        help_text=_("Cert number holds the id given to deactivating and activating a recurring payment")
    )

    cert_bearer_first_name = models.CharField(
        verbose_name= _("Cert Bearer First Name"),
        max_length=255,
        null = True,
        help_text=_("this indicates the name of the certificate owner ")
    )

    cert_bearer_last_name = models.CharField(
        verbose_name= _("Cert Bearer Last Name"),
        max_length=255,
        null = True,
        help_text=_("this indicates the name of the certificate owner ")
    )

    cert_bearer_country = models.ForeignKey(
        Country , on_delete=models.CASCADE,
        verbose_name=_('Cert Bearer Country'),
        null=True,
        help_text=_('this shows the country in which the certificate is issued')
    )  

    date_of_completion = models.DateTimeField(
        verbose_name = _('Date Of Completion'),
        null = True,
        help_text=_('this indicates the date in which the user completes he or her training process')
    )

    traning_platform = models.CharField(
        choices=PLATFORMS,
        verbose_name=_('Traning Platform'),
        max_length=30,
        null=True,
        help_text=_("this indicates the platform that the user completed his or her training process")
    )

    def __str__(self):
        return str(self.user)
    

    def save(self, *args, **kwargs) -> None:
        while not self.cert_number:
            cert_number = ref_code()
            object_with_similar_ref = Training_Cert.objects.filter(cert_number=cert_number)
            if not object_with_similar_ref:
                self.cert_number = cert_number
        super().save(*args, **kwargs)

    
    class Meta:
        ordering = ('-created_date',)
        verbose_name = _('Training Cert Info')
        verbose_name_plural = _('Training Cert Info')


from email.policy import default
from django.db import models
from django.utils.translation import gettext_lazy as _
from helpers.common.basemodel import BaseModel
from locations.models import Country
# Create your models here.

GENDER = (
        ('male', _('Male')),
        ('female', _('Female')),
    )

PLATFORM = (
        ('all_the_above', _('all_the_above')),
        ('kroon', _('kroon')),
        ('kroon_kiosk', _('kroon_kiosk')),
    )

class Ads (BaseModel):

    ad_country = models.ManyToManyField(
        Country,
        verbose_name=_('Ad Country'),
        help_text = _(" this is the country that will be able to see this ad image")
    )

    ad_name = models.CharField(
        verbose_name= _("Ad Name"),
        max_length = 250, null = True, 
        help_text = _("this hold the name of the current ad")
        )

    ad_image = models.ImageField(
        verbose_name = _("Ad Image"),
        max_length = 250, null = True,
        upload_to = "ads_images/",
        help_text = _("input ad image which will be JPEG, PNG, or GIF")
    )

    ad_url = models.URLField(
        verbose_name = _("Ad URL"),
        null = True,blank=True,
        help_text = _("link that redirect the user to the ad page, its optional.")
    )

    platform = models.CharField(
        choices = PLATFORM,
        verbose_name = _("Ad Platform"),
        max_length=30, null = True,
        default = "all_the_above",
        help_text = _("the gender that is allowed to view this ad")
    )

    active = models.BooleanField (
        verbose_name = _("Active Ad"),
        default = False, null = True,
        blank=True,
        help_text = _("this status determines whether the ad is active or not to be viewed by users")
    )

    def __str__(self):
        return str(self.ad_name)

    class Meta:
        ordering = ('-created_date',)
        verbose_name = _("Kroon Ads")
        verbose_name_plural = _("Kroon Ads")

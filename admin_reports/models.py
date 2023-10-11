from platform import platform
from django.db import models
from django.utils.translation import gettext_lazy as _
from helpers.common.basemodel import BaseModel
from locations.models import Country
from kroon.users.models import User
from .choices import ModelChoices

NULL_AND_BLANK = {'null': True, 'blank': False}


class AdminPushNotifications (BaseModel):

    PLATFORM = (
        ('all_the_above', _('all_the_above')),
        ('kroon', _('kroon')),
        ('kroon kiosk', _('kroon_kiosk')),
    )
    
    title = models.CharField(
        verbose_name=_("Title"),
        max_length=255,
        **NULL_AND_BLANK,
        help_text=_("The notification title that will be displayed to the user mobile device.")
    )

    body_message = models.TextField(
        verbose_name = _("Body Message"),
        **NULL_AND_BLANK,
        help_text=_("this holds the content of the push notification")
    )

    news_feed_country = models.ManyToManyField(
        Country,
        verbose_name = _("Country"),
        help_text =_("The country that is only valid to view this ")
    )

    platform = models.CharField(
        choices=ModelChoices.APP_TYPES,
        default= ModelChoices.APP_TYPE_ALL,
        max_length=30,
        **NULL_AND_BLANK,
        help_text=_("This holds the platform that is only valid to recieve the push notification, which can also be identified as the 'all the above' which shows the contents for devices and platforms that is registered under kroon network.")
    )

    device_type = models.CharField(
        verbose_name=_("Device Type"),
        max_length=25,
        null=True, 
        help_text=_("this storess the device type in which the push notifications is been sent to")
    )

    # This section is used by the gov workers 

    publisher = models.ForeignKey(
        User, on_delete=models.SET_NULL,
        verbose_name=_("Publisher"),
        max_length=255,
        null=True,
        blank=True,
        help_text=_("This holds the publisher name ")
    )

    notification_type =  models.CharField(
        verbose_name=_("Notification Type"),
        max_length=25,
        null=True, 
        help_text=_("the notification type is the type of notification that is been sent by the admin")
    )
    # This section is used by the gov workers - ends here 

    status = models.BooleanField(
        verbose_name = _("Notification Status"),
        default = False,
        null =True,
        help_text = _("notification status which determines whether the feed should be shown or not")
    )

    def __str__(self):
        return str(self.title)

    class Meta:
        ordering = ('-created_date',)
        verbose_name = _("Push Notification")
        verbose_name_plural = _("Push Notification")

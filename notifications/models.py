from platform import platform
from django.db import models
from django.utils.translation import gettext_lazy as _
from helpers.common.basemodel import BaseModel
from locations.models import Country

class NewsFeed (BaseModel):

    PLATFORM = (
        ('all_the_above', _('all_the_above')),
        ('kroon', _('kroon')),
        ('kroon kiosk', _('kroon_kiosk')),
    )
    
    title = models.CharField(
        verbose_name=_("News Feed Title"),
        max_length=255,
        null=True, 
        help_text=_("The title of the new feed that will be displayed to the user")
    )

    image = models.ImageField(
        verbose_name = _("News Feed Image"),
        null=True, blank=True,
        upload_to="news_feed/",
        help_text=_("news feed image that will be displayed to the user")
    )

    content = models.TextField(
        verbose_name = _("News Feed Content"),
        null=True,
        help_text=_("this holds the content of the news feed")
    )

    news_feed_country = models.ManyToManyField(
        Country,
        verbose_name = _("News Feed Country"),
        help_text =_("The country that is only valid to view this news feed ")
    )

    platform = models.CharField(
        choices=PLATFORM,
        default= "all_the_above",
        max_length=255,
        null=True, blank=True,
        help_text=_("The platform that is only valid to view this news feed specified for the paltform only , which can also be identified as the 'all the above' which shows all the contents for kroon and kroon kiosk to the users")
    )

    # This section is used by the gov workers 

    approved_date = models.DateTimeField(
        verbose_name=_("Approved Date"),
        max_length=20,
        null=True,
        blank=True, 
        help_text=_("Approved date is when the record is been approved by the gov super admin.")
        )
    
    publishing_time = models.DateTimeField(
        verbose_name=_("Publishing Date"),
        max_length=20, 
        null=True,
        blank=True, 
        help_text=_("Publishing Date will be calculated automatically adding 3 mins to the current time , which will automatically be published when it up to the published time.")
        )
    
    publisher = models.CharField(
        verbose_name=_("Publisher"),
        max_length=255,
        null=True,
        blank=True,
        help_text=_("This holds the publisher name ")
    )

    gov_post =  models.BooleanField(
        verbose_name = _("Gov Post Status"),
        default = False,
        null =True,
        blank=True,
        help_text = _("this is to indicate that the current post or news feed is a government news feed")
    )

    # This section is used by the gov workers - ends here 

    status = models.BooleanField(
        verbose_name = _("News Feed Status"),
        default = False,
        null =True,
        help_text = _("news feed status which determines whether the feed should be shown or not")
    )

    def __str__(self):
        return str(self.title)

    class Meta:
        ordering = ('-created_date',)
        verbose_name = _("News Feed")
        verbose_name_plural = _("News Feed")

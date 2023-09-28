from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

 
 
class Country(models.Model):
    """Represents a country"""
    # region Fields
    name = models.CharField(
        max_length=255,
        verbose_name=_('Country Name'),
        help_text=_('English name of country'))
 
    phone_code = models.CharField(
        max_length=100,
        blank=True, null=True,
        verbose_name=_('Phone Code'),
        help_text=_('Countries International dialing phone code.'))
 
    currency = models.CharField(
        max_length=50,
        blank=True, null=True,
        verbose_name=_('Currency'),
        help_text=_('Official country currency.'))
 
    iso2 = models.CharField(
        max_length=2,
        blank=True, null=True,
        verbose_name=_('ISO2'),
        help_text=_('Two-letter country code'))
  
    native = models.CharField(
        max_length=255,
        blank=True, null=True,
        help_text=_('Localized or native language of country.'))
 
    accept_signup = models.BooleanField(
        default=True,
        verbose_name=_('Accept Registration'),
        help_text=_('Allow users from country to register.'))

    accept_kroon = models.BooleanField(
        default=False,
        verbose_name=_('Accept Kroon Users'),
        help_text=_('Allow users from country to register.'))
 
    banned = models.BooleanField(
        default=False,
        verbose_name=_('Banned'),
        help_text=_('Indicate if country is banned or not'))

    created_date = models.DateTimeField(
        default=timezone.now,
        blank=True, editable=False,
        verbose_name=_('Created Date'),
        help_text=_('Timestamp when the record was created'))
 
    modified_date = models.DateTimeField(
        default=timezone.now,
        blank=True, editable=False,
        verbose_name=_('Modified Date'),
        help_text=_('Timestamp when the record was modified.'))
 
    # endregion

     # region Methods
    def __str__(self):
        return str(self.name)
    # endregion
 
    # region Metadata
    class Meta:
        verbose_name = _("Country")
        verbose_name_plural = _("Countries")
        db_table = 'countries'
    # endregion



class Country_Province(models.Model):
    """ this hold the record for country province """
    # country province fields 
    country = models.ForeignKey(
        Country , on_delete=models.SET_NULL,
        null=True ,
        help_text = """ this holds the record for the country which the province belongs to """
    )

    province = models.CharField(
        max_length= 40,
        null= True , 
        blank=True,
        help_text=""" this is the name of the province"""
    )

    active = models.BooleanField(
        default=False,
        verbose_name=_('Active'),
        help_text=_('Indicate if province is active or not'))


    created_date = models.DateTimeField(
        default=timezone.now,
        blank=True, editable=False,
        verbose_name=_('Created Date'),
        help_text=_('Timestamp when the record was created'))
 
    modified_date = models.DateTimeField(
        default=timezone.now,
        blank=True, editable=False,
        verbose_name=_('Modified Date'),
        help_text=_('Timestamp when the record was modified.'))
    
    # end country provience fields

    def __str__(self):
        return str(self.province)

    # country provience Metadata
    class Meta:
        verbose_name = _("Country Province")
        verbose_name_plural = _("Country Province")
        db_table = 'countries_province'
    # end country province
    


 
   
class Language(models.Model):
    """Represents a country language"""

    language_name = models.CharField(
        verbose_name=_("Language name"),
        max_length=255, null=True,
        blank=True,
        help_text=_('this represents the language name')
    )

    language_ISO2 = models.CharField(
        verbose_name=_("Language ISO 2 code"),
        max_length=2, null=True,
        blank=True,
        help_text=_('the language iso 2 ')
    )

    def __str__(self):
        return str(self.language_name)


    class Meta:
        verbose_name = _("Language")
        verbose_name_plural = _("Language")
        db_table = 'countries_language'


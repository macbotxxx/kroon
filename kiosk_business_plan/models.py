from django.db import models
from django.utils.translation import gettext_lazy as _
from helpers.common.basemodel import BaseModel
from kroon.users.models import User
from kiosk_categories.models import Category 


# Create your models here.


class Business_Plan (BaseModel):

    BUSINESS_TYPE = (
        ('registered business', _('Registered Business')),
        ('sole trade', _('Sole Trade')),
    )

    PERIOD_OF_REPORT = (

        ('12', _('1 Year')),
        ('24', _('2 Year')),
        ('36', _('3 Year')),
        # ('48', _('4 Year')),
        # ('60', _('5 Year')),
        # ('72', _('6 Year')),
        # ('84', _('7 Year')),
        # ('96', _('8 Year')),
       
    )

    user = models.ForeignKey(
        User,
        verbose_name=_("User Profile"),
        on_delete=models.CASCADE, null=True,
        related_name="merchant_business_plan",
        help_text=_("The user for whom the business plan will be created for.")
    )

    business_name = models.CharField(
        verbose_name=_("Business Name"),
        max_length=255,
        null=True,
        help_text=_('the business name for the merchant user.')
    )

    business_logo = models.ImageField(
        verbose_name=_("Business Logo"),
        null=True,
        blank=True,
        help_text=_('Here goes your business logo if any ( Optional ).')
    )

    business_registration_number = models.CharField(
        verbose_name=_("Business Registeration Number"),
        max_length=255,
        null=True,blank=True,
        help_text=_('the business registration number for the merchant user ( Optional ).')
    )

    business_contact = models.CharField(
        verbose_name=_("Business Contact"),
        max_length=255,
        null=True,
        help_text=_('the business contact number that belong to the merchant business account')
    )

    business_address = models.CharField(
        verbose_name=_("Business Address"),
        max_length=255,
        null=True,
        help_text=_('the business address for the registered merchant business account.')
    )

    business_owner_name = models.CharField(
        verbose_name=_("Business Owner Name"),
        max_length=255,
        null=True,
        help_text=_('the section store the business owner name for the registered merchant business account')
    )

    business_owner_contact = models.CharField(
        verbose_name=_("Business Owner Contact Number"),
        max_length=255,
        null=True,
        help_text=_('the section store the business owner contact number for the registered merchant business account')
    )

    business_owner_email = models.EmailField(
        verbose_name=_("Business Owner Email"),
        max_length=255,
        null=True, 
        help_text=_('the business owners email address')
    )

    business_type = models.CharField(
        verbose_name=_("Business Type"),
        max_length=255,
        null=True,
        help_text=_('gthe merchant need to select the business type on which their business runs on.')
    )


    business_category = models.ManyToManyField(
        Category, 
        verbose_name = _("Business category"),
        help_text= _('Business category will refrence the  category  which your business falls into.')
    )

    year_of_operation = models.CharField(
      verbose_name=_("Years Of Operation"),
        null=True, 
        max_length=255,
        help_text=_('this show how many years on which the business has been running.')
    )

    number_of_employees = models.IntegerField(
        verbose_name=_("Numbers Of Employee"),
        null=True,
        default = 0,
        help_text=_('the total number of employees that are currently working with')
    )

    business_expenses = models.ManyToManyField(
        'BusinessPlanExpenses',
        verbose_name=_("Business Expenses"),
        related_name="merchant_business_Expenses_profile",
        help_text=_("this is the business Expenses that is link to the expenses .")
    )
   
    salaries = models.DecimalField(
        verbose_name=_("Salaries"),
        null=True,
        max_digits = 300, decimal_places = 2,
        default=0.00,
        help_text=_('the amount of salary that a worker is been paid monthly')
    )

    electricity = models.DecimalField(
        verbose_name=_("Electricity Bills"),
        null=True,
        max_digits = 300, decimal_places = 2,
        default=0.00,
        help_text=_('the initiated amount you paid for electricity bill monthly.')
    )

    data = models.DecimalField(
        verbose_name=_("Internet Data Bill"),
        null=True,
        max_digits = 300, decimal_places = 2,
        default=0.00,
        help_text=_('the initiated amount you paid for internet data bills monthly.')
    )

    fuel = models.DecimalField(
        verbose_name=_("Fuel Bill"),
        null=True,
        max_digits = 300, decimal_places = 2,
        default=0.00,
        help_text=_('the initiated amount you paid for fuel monthly.')
    )

    period_of_report = models.CharField(
        choices = PERIOD_OF_REPORT,
        verbose_name=_("Period Of Report"),
        max_length=255,
        null=True,
        help_text=_('Select the how mnay months report you want to generate for your business')
    )

    def __str__(self):
        return str(self.user)

    class Meta:

        ordering = ('-created_date',)
        verbose_name = _("Merchant Business Plan")
        verbose_name_plural = _("Merchant Business Plan")



class BusinessPlanExpenses(BaseModel):
    user = models.ForeignKey(
        User,
        verbose_name=_("User Profile"),
        on_delete=models.CASCADE, null=True,
        related_name="merchant_business_plan_expenses",
        help_text=_("The user for whom the business plan will be created for.")
    )

    business_plan = models.ForeignKey(
        Business_Plan,
        verbose_name=_("Business Plan"),
        on_delete=models.CASCADE, null=True,
        related_name="merchant_business_plan_profile",
        help_text=_("this is the business plan that is link to the expenses .")
    )

    expenses = models.CharField(
        verbose_name=_("Expenses"),
        max_length=255,
        null=True,
        help_text=_('this input nneeds to have the expenses title ')
    )

    expenses_amount = models.DecimalField(
        verbose_name=_("Expenses Amount"),
        null=True,
        max_digits = 300, decimal_places = 2,
        default=0.00,
        help_text=_('the initiated amount you paid for Expenses Amount monthly.')
    )

    def __str__(self):
        return str(self.user)

    class Meta:

        ordering = ('-created_date',)
        verbose_name = _("Merchant Business Plan Expenses")
        verbose_name_plural = _("Merchant Business Plan Expenses")







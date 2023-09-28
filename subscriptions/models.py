from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

from helpers.common.basemodel import BaseModel
from tinymce.models import HTMLField
from django.conf import settings

User = settings.AUTH_USER_MODEL


class Subscription_Plan (BaseModel):

    # KIOSK_PLANS = (
    #     ('basic', _('Basic')),
    #     ('starter', _("Starter")),
    #     ('Kiosk Pro', _("Kiosk Pro")),
    # )

    plan_name = models.CharField(
        verbose_name=_('Plan Name'),
        null=True, blank=True,
        max_length =50,
        help_text=_("the will be the subscription plan, provided by the admin ")
        )
    
    slug_plan_name = models.CharField(
        verbose_name=_('Slug Plan Name'),
        null=True, blank=True,
        max_length =50,
        help_text=_("the will be the subscription plan, provided by the admin ")
        )
    
    plan_fee = models.DecimalField(
        verbose_name = _("Plan Fee"),
        null=True,
        max_digits = 300, decimal_places = 2,
        default=0.00,
        help_text=_("transactional amount taken by the customer.")
    )

    plan_duration = models.IntegerField(
        verbose_name = _("Plan Duration"),
        null=True, blank=True,
        help_text = _("this holds the plan duration in days")
    )

    plan_default_currency = models.CharField(
        verbose_name = _("Default Plan Currency"),
        max_length =20, default = "USD",
        null = True, blank=True,
        help_text = _("the plan default currency is used to identify which currency should the plan payment be made with.")
    )

    yearly_plan = models.BooleanField(
        verbose_name = _("Year Plan"),
        null = True,blank=True,
        default = False,
        help_text = _("this indicates that this current plan is meant to be a yearly plan or not ")
    )

    yearly_plan_duration = models.IntegerField(
        verbose_name = _("Yearly Plan Duration"),
        null=True, blank=True,
        help_text = _("this holds the plan duration in days")
    )

    yearly_plan_fee = models.DecimalField(
        verbose_name = _("Yearly Plan Fee"),
        null=True,
        max_digits = 300, decimal_places = 2,
        default=0.00,
        help_text=_("yearly plan amount to be charged to the subscripers in a year.")
    )


    monthly_plan_id = models.CharField(
        verbose_name = _("Monthly Plan ID"),
        max_length=200, null=True,
        blank=True,
        help_text=_("this hold the plan recurring id , which is been requested for subscription recurring payment")
    )

    yearly_plan_id = models.CharField(
        verbose_name = _("Yearly Plan ID"),
        max_length=200, null=True,
        blank=True,
        help_text=_("this hold the plan recurring id , which is been requested for subscription recurring payment")
    )

    plan_content = HTMLField()

    default_plan = models.BooleanField(
        verbose_name = _("Defualt Plan"),
        null = True,blank=True,
        default = False,
        help_text = _("this indicates that this current plan is meant to be the defualt plan for merchant users.")
    )

    active = models.BooleanField(
        verbose_name = _("Status"),
        null = True,
        default = True,
        help_text = _("this indicates whether the promotional code is active or not.")
    )


    def __str__(self):
        return str(self.plan_name)
        
    class Meta:
        ordering = ('-created_date',)
        verbose_name = _("Subcription Plans")
        verbose_name_plural = _("Subscription Plan")



class Merchant_Subcribers (BaseModel):

    user = models.ForeignKey(
        User,
        verbose_name=_("User Profile"),
        on_delete=models.CASCADE, null=True,
        related_name="merchant_subcribers",
        help_text=_("The user for whom account belongs to")
    )

    plan = models.ForeignKey(
        Subscription_Plan, on_delete = models.PROTECT,
        null=True, blank=True,
        related_name = 'plans',
        help_text=_("the will be the subscription plan, provided by the admin ")
    )

    yearly_plan = models.BooleanField(
        verbose_name = _("Year Plan"),
        null = True,blank=True,
        default = False,
        help_text = _("this indicates that this current plan is meant to be a yearly plan or not ")
    )

    start_date = models.DateTimeField(
        verbose_name=_("Start Date"),
        default=timezone.now,
        max_length=20, 
        help_text=_("Timestamp when the subscription was created.")

    )

    end_date = models.DateTimeField(
        verbose_name=_("End Date"),
        max_length=20, 
        help_text=_("Timestamp when the subscription was expire.")
    )

    device_type = models.CharField(
        verbose_name= _("Device Type"),
        max_length=25,
        null = True,
        blank=True,
        help_text=_("this indicates the merchants device type , ether its an apple or google device type")
    )

    subscription_id = models.CharField(
        verbose_name= _("Subscription ID"),
        max_length=255,
        null = True,
        blank=True,
        help_text=_("subscription id holds the id given to deactivating and activating a recurring payment")
    )

    receipt_data = models.TextField(
        verbose_name= _(" Receipt Data "),
        null = True,
        blank=True,
        help_text=_("The token provided to the user's device when the subscription was purchased.")
    )
    
    sub_plan_id = models.CharField(
        verbose_name= _("Sub Plan ID"),
        max_length=255,
        null = True,
        blank=True,
        help_text=_("this plan id holds the id given to identify the subscription plan of the user which cna be the yearly plan id or the monthly plan id")
    )

    recurring_payment = models.BooleanField(
        verbose_name = _("Recurring Payment"),
        null = True,
        default = True,
        blank=True,
        help_text = _("this indicates if the subscription payment is recurring or not, which can also be deactivated by the user.")
    )

    active = models.BooleanField(
        verbose_name = _("Status"),
        null = True,
        default = False,
        help_text = _("this indicates whether the promotional code is active or not.")
    )

    def __str__(self):
        return str(self.user) 

    class Meta:
        ordering = ('-created_date',)
        verbose_name = _("Merchant Subscribers")
        verbose_name_plural = _("Merchant Subscribers")


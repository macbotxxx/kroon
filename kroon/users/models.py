import uuid
import random
import string

from allauth.account.signals import user_signed_up
from django.dispatch import receiver
# django email settings
from django.core import mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings

from django.contrib.auth.models import User
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db.models import CharField
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.db import models
from django.dispatch import receiver

# test editor .....
from ckeditor.fields import RichTextField
from tinymce.models import HTMLField

from helpers.common.basemodel import BaseModel
from kiosk_categories.models import Category
from locations.models import Country , Country_Province
from virtual_cards.models import Virtual_Cards_Details
from gov_panel.models import Government_Organizations

# for JWT token





def ref_code():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=9))

def business_id_():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))


#  SENDING WELCOME EMAIL MESSAGE TO NEW USERS 
@receiver(user_signed_up)
def user_signed_up_(request, user, **kwargs):
    # user signed up now send email
    # send email part - do your self
    # sending email to the user about to be giftted kroon token 
    subject = f'Kroon Welcomes You To Community'
    html_message = render_to_string(
        'emails/welcome.html',
        {
        'user': user.first_name,
        } 
    )
    plain_message = strip_tags(html_message)
    from_email = f"{settings.EMAIL_HOST_USER}" 
    to = user.email
    mail.send_mail(subject, plain_message, from_email, [to], html_message = html_message)



class UserAddress(BaseModel):

     # CHOICES
    ADDRESS_TYPE = (
        ('current', _('Current Address')),
        ('permanent', _("Permanent Address"))
    )

    type = models.CharField(
        choices=ADDRESS_TYPE,
        max_length=9,
        help_text=_("The type of address."),
        default='current',
        verbose_name=_("Address Type")
    )

    user = models.ForeignKey(
        'User',
        verbose_name=_("User Profile"),
        on_delete=models.CASCADE,
        help_text=_("The user for whom address belongs to")
    )

    street_or_flat_number = models.CharField(
        verbose_name=_("Street or Flat Number"),
        null=True, blank=True,
        max_length=50,
        help_text='Street or Flat Number"), of the user')

    street_name = models.CharField(
        verbose_name=_("Street Name"),
        null=True, blank=True,
        max_length=50,
        help_text='Street Name of the user')

    building_name = models.CharField(
        verbose_name=_("Building Name"),
        null=True, blank=True,
        max_length=50,
        help_text='Building Name of the user')

    state = models.CharField(
        verbose_name=_("State or Region"),
        null=True, blank=True,
        max_length=50,
        help_text='State or Region of the user')

    city = models.CharField(
        verbose_name=_("City"),
        max_length=50,
        null=True, blank=True,
        help_text=_("The city of the address of the user."))

    zip_post_code = models.CharField(
        verbose_name=_("Zip Post Code"),
        max_length=50,
        null=True, blank=True,
        help_text='Zip post code of the user address')

 
    #Metadata
    class Meta :
        verbose_name = _("Customers  Address")
        verbose_name_plural = _("Customers  Address")


    def __str__(self):
       return str(self.user.name)


class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError(_('The given email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))

        return self._create_user(email, password, **extra_fields)



class User(AbstractUser):
    """
    # Each `User` needs a human-readable unique identifier that we can use to
    # represent the `User` in the UI. We want to index this column in the
    # database to improve lookup performance.
    username = models.CharField(db_index=True, max_length=255, unique=True)

    # We also need a way to contact the user and a way for the user to identify
    # themselves when logging in. Since we need an email address for contacting
    # the user anyways, we will use it for logging in because it is
    # the most common form of login credential at the time of writing.
    email = models.EmailField(db_index=True, unique=True)

    # When a user no longer wishes to use our platform, they may try to delete
    # there account. That's a problem for us because the data we collect is
    # valuable to us and we don't want to delete it. To solve this problem, we
    # will simply offer users a way to deactivate their account.
    # That way they won't show up on the site anymore,
    # but we can still analyze the data.
    is_active = models.BooleanField(default=True)

    # The `is_staff` flag is expected by Django to determine who can and cannot
    # log into the Django admin site. For most users this flag will always be
    # falsed.
    is_staff = models.BooleanField(default=False)
    """
    
    objects = UserManager()

    KYC_STATUS = (
        ('unverified', _('Unverified')),
        ('pending', _('Pending')),
        ('verified', _('Verified')),
        ('action_required', _('Action_required')),
        ('cancelled', _('Cancelled')),
        ('rejected', _('Rejected/Refused'))
    )

    ACCOUNT_TYPE = (
        ('personal', _('Personal')),
        ('merchant', _('Merchant')),
    )

    GENDER = (
        ('male', _('Male')),
        ('female', _('Female')),
    )

    GOV_ORGANIZATION = (
        ('nasme_org1', _('NASME_ORG1')),
        ('nasme_org2', _('NASME_ORG2')),
    )

    id = models.UUIDField(
        default = uuid.uuid4,
        editable=False,
        primary_key=True,
        help_text=_("The unique identifier of the customer.")
    )

    account_type = CharField(
        verbose_name=_("Account Type"),
        choices=ACCOUNT_TYPE,
        default='personal',
        blank=True,null=True,
        max_length=15,
        help_text=_("Account type")
        )

    #: First and last name do not cover name patterns around the globe
    name = CharField(_("Name of User"), blank=True, max_length=255)

    email = models.EmailField(
        max_length=150,
        null=True,
        unique=True,
        verbose_name=_("Email Address"),
        help_text=_("The email address of the customer.")
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']
    username = None


    first_name = models.CharField(
        verbose_name=_("First names"),
        max_length=50,
        null=True,
        help_text=_("The first nammes of the customer.")
    )

    last_name = models.CharField(
        max_length=50,
        verbose_name=_("Last names"),
        null=True,
        help_text=_("The last nammes of the customer.")
    )

    date_of_birth = models.DateField(
        verbose_name=_("Date of birth"),
        blank=True,
        null=True,
        help_text=_("The date of birth of the customer.")
    )

    gender = models.CharField(
        choices = GENDER, 
        verbose_name=_("Gender"),
        max_length=7,null=True,
        help_text=_("users gender should be input.")
    )

    kyc_complete = models.BooleanField(
        verbose_name=_("KYC complete"),
        null=True,
        blank=True,
        default=False,
        help_text=_("Flag to determine if a cutomer have completed KYC verification")
    )

    kyc_complete_date = models.DateTimeField(
        verbose_name=_("KYC complete date"),
        blank=True,
        null=True,
        help_text=_("Timestamp when customer completed KYC verifiction process.")
    )

    kyc_status = models.CharField(
        max_length=15,
        verbose_name=_("KYC status"),
        choices=KYC_STATUS,
        default='Unverified',
        blank=True,
        null=True,
        help_text=_("The .")
    )

    kyc_submitted = models.BooleanField(
        verbose_name=_("KYC submitted"),
        blank=True,null=True, default = False,
        help_text=_("Flag to determine if customer has submitted a KYC verification.")
    )

    country_of_residence = models.ForeignKey(
        Country,
        verbose_name=_("Country of Residence"),
        blank=True, null=True,
        on_delete=models.CASCADE,
        help_text=_("The country residence of the customer. KYC verification will be applied to this country and customer must provide proof of such residence as relevant in the country of jurisdiction.")
    )

    country_province = models.ForeignKey(
        Country_Province, on_delete=models.SET_NULL,
        verbose_name=_("Country Province"),
        blank=True,
        null=True,
        help_text=_("The users country province")
    )

    default_currency_id = models.CharField(
        max_length=3,
        verbose_name=_("Default Currency ID"),
        blank=True, null=True,
        default='NGN',
        help_text=_("The default currency of the customer. Currency will be sent against customers country of residence.")
    )

    contact_number = models.CharField(
        max_length=13,
        verbose_name=_("Contact number"),
        unique=True,
        null=True,blank=True,
        help_text=_("The contact number of the customer.")
    )

    contact_number_verified = models.BooleanField(
        verbose_name=_("Contact Number Verification"),
        null=True,
        blank=True,
        default=False,
        help_text=_("Flag to determine if a cutomer have completed Contact number verification")
    )

    merchant_business_name = models.CharField(
        verbose_name=_("Merchant Business Profile"),
        max_length=255, null=True,
        blank=True,
        help_text = _("merchant business name which will be saved when the merchant update or register their business account")
    )

    # Kroon Balance and Wallet ID 
    kroon_token = models.DecimalField(
        verbose_name=_("Available Kroon Token"),
        null =True, blank=True, default=0.00,
        max_digits = 300, decimal_places = 2,
        help_text=_("The customers available kroon token for the account")
    )

    wallet_id = models.CharField(
        verbose_name=_("Kroon Wallet ID"),
        unique=True, null=True, blank=True,
        max_length=20,
        help_text=_("User kroon wallet id is unique to every user, the wallet id contains information about the customer")
    )

    # Kroon Balance and Wallet ID 

    # Onboarding Process 

    on_boarding_complete = models.BooleanField(
        verbose_name=_("Completed Onboarding"),
        default=False,
        help_text=_("Flag to determine if customer has completed onboarding process.")
    )

    on_boarding_complete_date = models.DateTimeField(
        default=timezone.now,
        verbose_name=_("Onboarding Complete Date"),
        blank=True, null=True,
        help_text=_("Timestamp when customer completed onboarding process.")
    )

    on_boarding_user = models.ForeignKey(
        'User',
        verbose_name=_("Gov Profile"),
        on_delete=models.CASCADE,
        related_name = "gov_on_boarding_user",
        null=True , blank=True,
        help_text=_("this is the gov user account that provides the current user information for on boarding")
    )

    generated_password = models.CharField(
        verbose_name=_("Generated Password"),
        max_length=455,
        null=True,
        blank=True,
        help_text=_("this generated password is set to be the default password when an onboarding process is been taken place. its advisable to change the generated password")
    )

    email_details = models.BooleanField(
        verbose_name= _("Email Details"),
        default=False,
        null =True,
        help_text = _("email details section indicates if the email coontaining the user default details has been set or not . this operation is only taken place when an onboarding process is been completed")
    )

    #"""
    #this features is only activated for Nigerian merchants only.
    #this helps the system to identify if the merchant is 
    #running a registered government business or not.
    #"""
    government_registered = models.BooleanField(
        verbose_name= _("Government Registered"),
        default=False,
        null =True,
        blank=True,
        help_text = _("This indicates if the merchant is a registered government organization")
    )

    government_organization_name = models.ForeignKey(
        Government_Organizations, 
        on_delete=models.CASCADE,
        verbose_name = _("Government Organization Name"),
        null = True,
        blank = True,
        help_text = _("The government organization name holds the title name of the organisation that the merchant business is registered under")
    )

    #"""
    #ends here 
    #"""


    # Onboarding Process 
    registered_ip_address = models.GenericIPAddressField(
        verbose_name=_("Registered Ip Address"),
        blank=True, null=True,
        editable=False,
        help_text=_("The Ip address recorded at the time if registeration.")
    )

    submitted_bank_details = models.BooleanField(
        verbose_name= _("Submitted Bank Details"),
        default=False, null =True,
        help_text = _("this indicates whether the user has submitted his or har bank detail or not ,")
    )

    mobile_money_details_submitted = models.BooleanField(
        verbose_name= _("Submitted Mobile Money Details"),
        default=False, null =True,
        help_text = _("this indicates whether the user has submitted his or har mobile money detail or not ,")
    )

    accept_terms = models.BooleanField(
        verbose_name= _("Accept Terms"),
        default=False, null =True,
        help_text = _("this indicates whether the user accepted kroon terms and conditions.")
    )

    agreed_to_data_usage = models.BooleanField(
        verbose_name= _("Agree To Data Usage"),
        default=False, null =True,
        help_text = _("this indicates whether the user accepted kroon to data usage or not.")
    )

    email_verification = models.BooleanField(
        verbose_name= _("Email Verification"),
        default=False, null =True,
        help_text = _("this indicates whether the users email verification is been verified or not")
    )
    
    address = models.ManyToManyField(
        UserAddress,
        blank=True,
        verbose_name=_("User Address"),
        related_name="address",
        help_text=_("The users address which can be business address or home address,")

    )

    virtual_cards = models.ManyToManyField(
        Virtual_Cards_Details,
        blank=True,
        verbose_name=_("User Virtual Cards"),
        related_name="customer_virtual_cards",
        help_text=_("This show the list of virtual card owned ny this user ")

    )

    bank_details = models.ForeignKey(
        'UserBankDetails', on_delete = models.CASCADE,
        blank=True, null=True,
        verbose_name=_("User Bank Details"),
        related_name="bank_details",
        help_text=_("The users bank details associated for the user local bank withdrawal")

    )

    device_id = models.CharField(
        verbose_name=_("Device ID"),
        max_length=455,
        null=True,blank=True,
        help_text=_("the device id is meant to be unique across all platform to identify for security reasons")
    )

    device_fingerprint = models.CharField(
        verbose_name=_("Device Finger Print"),
        max_length=455, default='null',
        null=True,blank=True,
        help_text=_("the device finger print is meant to be unique across all platform to identify the user login device for security purpose")
    )

    device_type = models.CharField( 
        verbose_name=_("Device Type"), 
        max_length= 300,
        null=True, blank = True,
        help_text=_("the hold the users device type which is meant to updated when the user logs in.")
     )

    app_version = models.CharField( 
        verbose_name=_("Users App Version"),
        max_length=255,
        null=True, blank=True,
        help_text = _("this indicates which version of app the user is using , so to determine which when to pop up and update for the app.")
     )

    simulate_account = models.BooleanField(
        verbose_name= _("Simulated Account"),
        default=False, null =True,
        help_text = _("this indicates that the current account is a simulated account which is not meant to be used for any live transaction")
    )

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

    class Meta:
        ordering = ('-created_date',)
        verbose_name = _("All Registered customers")
        verbose_name_plural = _("All Registered customers")

    def save(self, *args, **kwargs) -> None:
        while not self.wallet_id:
            wallet_id = ref_code()
            object_with_similar_ref = User.objects.filter(wallet_id=wallet_id)
            if not object_with_similar_ref:
                self.wallet_id = wallet_id
        super().save(*args, **kwargs)

        
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"



# class UserSession(models.Model):
#     """
#     Account session created 
#     """
#     user_acc = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     session_maneger = models.OneToOneField(Session, on_delete=models.CASCADE)
  

class UserActivity (BaseModel):
    """ 
    An Activity Log (also known as an Activity Diary ) is a written record of how a user spend time. 
    you can then change the way that you work to eliminate them.
    """

    user = models.ForeignKey(
        'User',
        verbose_name=_("User Profile"),
        on_delete=models.CASCADE,
        help_text=_("The user for whom account belongs to")
    )

    hostname = models.CharField(
        verbose_name=_("Host Name"),
        max_length=355,
        null=True,blank=True,
        help_text=_("The Host Name of the logged in user system")
    )

    ip_address = models.GenericIPAddressField(
        verbose_name=_("System IP Address"),
        null=True, blank=True, 
        editable=False,
        help_text=_(" The system IP address to current login user")
    )

    class Meta:
        ordering = ('-created_date',)
        verbose_name = _("All Users Activity")
        verbose_name_plural = _("All Users Activity")

    def __str__(self):
        return str(self.user)



class UserBankDetails (BaseModel):
    user = models.ForeignKey(
        'User',
        verbose_name=_("User Profile"),
        on_delete=models.CASCADE,
        help_text=_("The user for whom account belongs to")
    )

    account_name = models.CharField(
        verbose_name = _("Account Name"),
        max_length=70, null =True,
        blank=True,
        help_text = _("the customers bank account name.")
        )

    account_number = models.CharField(
        verbose_name = _("Account Number"),
        max_length=20,null =True,
        blank=True,
        help_text = _("the customers bank account number for the bank")
    )

    bank_name = models.CharField(
        verbose_name = _("Bank Name"), 
        max_length=60,
        null=True,blank=True,
        help_text=_("The bank name of the customer.")
        )

    bank_code = models.CharField(
        verbose_name = _("Bank Code"), 
        max_length=25,
        null=True,blank=True,
        help_text = _("The bankinig code which is required for the withdrawal.")
        )

    bank_id = models.CharField(
        verbose_name = _("Bank ID"),
        max_length=3,
         null=True,blank=True,
        help_text = _("The bankinig ID which is required for the withdrawal.")
        )

    """
    This recipient record stores the neccessary imformation that is used
    for withdrawal process which is been carried out by our third party
    providers and thats PAYSTACK
    the recipient record is meant to be a one time saved record , the models
    shows the required information for the withdrawal process.
    this record is required by PAYSTACK
    """
    integration_id = models.CharField(
        verbose_name=_("Integration ID"),
        max_length=255,
        null=True, blank=True,
        help_text=_("this is the integration ID which is stored for reference purpose")
    )

    recipient_code =  models.CharField(
        verbose_name=_("Recipient Code"),
        max_length=255,
        null=True, blank=True,
        help_text=_("the recipient code is stored and used for withdrawal purpose. which is meant to be unique to per user and also its an auto generated code from the third party.")
    )


    verified = models.BooleanField(
        verbose_name = _("Account Verified"),
        default=False, 
        null=True,blank=True,
        help_text = _("customers account verification status which determines whether the account number is verified or not .")
    )

    def __str__(self):
        return str(self.user)

    class Meta:
        ordering = ('-created_date',)
        verbose_name = _("Customer Bank Details")
        verbose_name_plural = _("Customer Bank Details")


class UserWrongPinValidate (BaseModel):
    user = models.ForeignKey(
        'User',
        verbose_name=_("User Profile"),
        on_delete=models.CASCADE,
        help_text=_("The user for whom account belongs to")
    )

    failed_password = models.PositiveIntegerField(
        verbose_name = _("Password Failed Count"),
        default = 0, null=True,
        help_text = _("the user password fialed count which store the count for a user when ever the password fails.")
        )

    banned = models.BooleanField(
        verbose_name = _("Password Banned"),
        default = False,
        )

    def __str__(self):
        return str(self.user)


    class Meta:
        ordering = ('-created_date',)
        verbose_name = _("Password Fialed Count")
        verbose_name_plural = _("Password Fialed Count")


PLATFORM = (
        ('kroon', _('kroon')),
        ('kiosk', _("kiosk"))
    )



class KroonTermsAndConditions (BaseModel):

    content = models.TextField(
        verbose_name = _("Content"),
        null=True,
        help_text = _("here goes the content for kroon terms and conditions")
    )

    platform = models.CharField(
        verbose_name = _("Platform"),
        max_length = 255,
        choices = PLATFORM, null=True,
        blank=True,
        help_text = _("this indicates the platform which the teams and conditions is been generated for.")
    )
    
    active = models.BooleanField(
        verbose_name = _("Content Active"),
        default = False, null =True,
        help_text = _("this indicates whether the content should available for display or not ")
    )

    def __str__(self):
        return str(self.id)

    class Meta:
        ordering = ('-created_date',)
        verbose_name = _("Kroon terms and conditions")
        verbose_name_plural = _("Kroon terms and conditions")


class PolicyAndCondition (BaseModel):
    
    content = models.TextField(
        verbose_name = _("Content"),
        null=True,
        help_text = _("here goes the content for kroon terms and conditions")
    )

    platform = models.CharField(
        verbose_name = _("Platform"),
        max_length = 255,
        choices = PLATFORM, null=True,
        blank=True,
        help_text = _("this indicates the platform which the policy is been generated for.")
    )
    
    active = models.BooleanField(
        verbose_name = _("Content Active"),
        default = False, null =True,
        help_text = _("this indicates whether the content should available for display or not ")
    )

    def __str__(self):
        return str(self.id)

    class Meta:
        ordering = ('-created_date',)
        verbose_name = _("Kroon Policy")
        verbose_name_plural = _("Kroon Policy")


class KroonFQA (BaseModel):
    question = models.CharField(
        verbose_name=_("Question"),
        max_length=255, null=True,
        help_text = _("the questions which customers are likely to ask or know about.")
    )

    answer = models.TextField(
        verbose_name=_("Answer"),
        null=True,
        help_text = _("The answer to the question been provided for the customer satisfaction")
    )

    def __str__(self):
        return str(self.question)

    class Meta:
        ordering = ('-created_date',)
        verbose_name = _("Kroon FAQs")    
        verbose_name_plural = _("Kroon FAQs")


class KioskFAQ (BaseModel):
    question = models.CharField(
        verbose_name=_("Question"),
        max_length=255, null=True,
        help_text = _("the questions which customers are likely to ask or know about.")
    )

    answer = models.TextField(
        verbose_name=_("Answer"),
        null=True,
        help_text = _("The answer to the question been provided for the customer satisfaction")
    )

    def __str__(self):
        return str(self.question)

    class Meta:
        ordering = ('-created_date',)
        verbose_name = _("Kiosk FAQs")    
        verbose_name_plural = _("Kiosk FAQs")     


class BusinessProfile (BaseModel):
    """
    business profile is used only for kroon merchant users 
    """

    BUSINESS_TYPE = (
        ('Retail Store', _('Retail Store')),
        ('Grocery Store', _("Grocery Store")),
        ('Convenient Store', _("Convenient Store")),
        ('Beauty and Fashion', _("Beauty and Fashion")),
        ('Electronics', _("Electronics")),
        ('Services', _("Services")),
        ('Others', _("Others")),
    )

    user = models.ForeignKey(
        'User',
        verbose_name=_("User Profile"),
        on_delete=models.CASCADE,
        help_text=_("The user for whom account belongs to")
    )

    business_id = models.CharField(
        verbose_name=_("Business ID"),
        max_length=255, null=True,
        help_text = _("business id is used as a special indicator to identify the user business.")
    )

    business_registration_number = models.CharField(
        verbose_name=_("Business Registration Number"),
        max_length=255, null=True,
        blank=True,
        help_text = _("business registration number is used to identify the user business.")
    )

    business_logo = models.ImageField(
        verbose_name=_("Business Logo"),
        upload_to = "images/business/logo",
        null=True, blank=True,
        help_text = _("business logo for the merchant business account.")
    )

    business_name = models.CharField(
        verbose_name=_("Business Name"),
        max_length=255, null=True,
        help_text = _("the merchant user business name.")
    )

    business_contact_number = models.CharField(
        verbose_name=_("Business Contact Number"),
        max_length=255, null=True,
        help_text = _("the merchant user business contact number")
    )

    business_address = models.CharField(
        verbose_name=_("Business Address"),
        max_length=255, null=True,
        help_text = _("the merchant user business address")
    )

    workers = models.ManyToManyField(
        'User',
        verbose_name=_("Worker Profile"),
        related_name = "worker_profile",
        blank=True,
        help_text=_("this field holds the company workers profile account which will automatically be associated with the user profile account.") 
    )

    business_category = models.ManyToManyField(
        Category, 
        blank=True,
        help_text = _("this shows the business category which the user will select from ")
        )

    business_type = models.CharField(
        choices = BUSINESS_TYPE,
        verbose_name=_("Business Type"),
        blank=True,
        max_length = 255,
        null=True,
        help_text = _("this shows the business type which the user will select from ")
        )

    business_default_language = models.CharField(
        verbose_name=_("Business Default Language"),
        max_length=255, null=True,
        help_text = _("the merchant default langauge for his business profile")
    )

    web_light_mode = models.BooleanField(
        verbose_name=_("Web Light Mode"),
        default=True, null=True,
        help_text = _("the active status bar indicates if the merchant business is on light mode or not ")
    )

    accept_email_notifications = models.BooleanField(
        verbose_name=_("Email Notification"),
        default=True, null=True,
        help_text = _("the active status bar indicates if the merchant business is on light mode or not ")
    )

    accept_mobile_notifications = models.BooleanField(
        verbose_name=_("Mobile Nofication"),
        default=True, null=True,
        help_text = _("the active status bar indicates if the merchant business is on light mode or not ")
    )

    active = models.BooleanField(
        verbose_name=_("Active"),
        default=False, null=True,
        help_text = _("the active status bar indicates if the merchant business is active or not")
    )

    def __str__(self):
        return str(self.user)

    def save(self, *args, **kwargs) -> None:
        while not self.business_id:
            business_id = f'KMID_{business_id_()}'
            object_with_similar_ref = BusinessProfile.objects.filter(business_id=business_id)
            if not object_with_similar_ref:
                self.business_id = business_id
        super().save(*args, **kwargs)

    class Meta:
        ordering = ('-created_date',)
        verbose_name = _("Merchant Business Profile")
        verbose_name_plural = _("Merchant Business Profile")


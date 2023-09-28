# Returns a JWT that can be used to authenticate the user.from decimal import Decimal
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth import password_validation
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.tokens import default_token_generator
from django.core import exceptions

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers, exceptions

from datetime import timedelta, datetime
from subscriptions.models import Subscription_Plan ,Merchant_Subcribers
from promotional_codes.models import Government_Promo_Code
from kiosk_categories.models import Category 
from kroon_gift.models import KroonGift
from kroon.users.models import User, UserAddress, UserBankDetails, KroonTermsAndConditions, BusinessProfile, PolicyAndCondition, KroonFQA, KioskFAQ
from locations.models import Country, Country_Province
from gov_panel.models import Government_Organizations
from kiosk_stores.models import Merchant_Product
from virtual_cards.api.serializers import User_Virtual_Cards

from rest_framework_simplejwt.token_blacklist.models import OutstandingToken,BlacklistedToken




# Get the UserModel
UserModel = get_user_model()



class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        total = 0
        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)

        # Add extra responses here
        # data['user_details'] = User.objects.filter ( email = self.user.email ).values()
        data['device_fingerprint'] = self.user.device_fingerprint
        data['device_type'] = self.user.device_type
        data['accept_kroon'] = Country.objects.filter( name = self.user.country_of_residence ).values('accept_kroon','currency')
        business_currency = None
        merchant_wallet_id = None
        merchant_country = None
        user_plan = None
        # try:
        #     BusinessProfile.objects.get( user = self.user)
        #     merchant_role = 'merchant'
        #     merchant_wallet_id = self.user.wallet_id
        #     business_currency = self.user.default_currency_id
        #     merchant_country = self.user.country_of_residence
        # except:
        #     worker_roles = BusinessProfile.objects.filter( workers = self.user)
        #     for c in worker_roles:
        #         business_currencys = c.user.default_currency_id
        #         wallet_id = c.user.wallet_id
        #         business_currency = business_currencys
        #         merchant_wallet_id = wallet_id
        #         merchant_country = c.user.country_of_residence

        #     if worker_roles:
        #         merchant_role = 'worker'
        #     else:
        #         merchant_role = None

        try:
            Country.objects.get( name = merchant_country , accept_kroon = True )
            merchant_accept_kroon = True
        except Country.DoesNotExist:
            merchant_accept_kroon = False

        # try:
        #     user_plans = Merchant_Subcribers.objects.get( user = self.user , active = True)
        #     if user_plans:
        #         user_plan = user_plans.plan.plan_name
        #     merchant_subcription = user_plan
            
        # except Merchant_Subcribers.DoesNotExist :
        #     merchant_subcription = "Expired"

        data['merchant_accept_kroon'] = merchant_accept_kroon
        # data['merchant_subscription'] = merchant_subcription

        data['account_type'] = self.user.account_type
        # data['merchant_wallet_id'] = merchant_wallet_id
        # data['business_currency'] = business_currency
        data['gift_kroon_details'] = KroonGift.objects.filter( email = self.user.email, settled = False ).values()
        
        return data



class KroonKioskToken ( TokenObtainPairSerializer ):
    
    def validate(self, attrs):
        # delete the previous token
        # try:
        #     toeks = OutstandingToken.objects.all()
        #     print(toeks)
        # except OutstandingToken.DoesNotExist:
        #     pass

        total = 0
        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)

        # getting the merchant business information
        business_currency = None
        merchant_wallet_id = None
        merchant_country = None
        user_plan = None
        merchant_business_profle = None
        try:
            my_business = BusinessProfile.objects.get( user = self.user , active = True )
            merchant_role = 'merchant'
            merchant_wallet_id = self.user.wallet_id
            business_currency = self.user.default_currency_id
            merchant_country = self.user.country_of_residence

            # Getting merchant registered business accounts 
            merchant_business_profle = BusinessProfile.objects.select_related('user').filter( user = self.user ).values('id', 'business_name','business_logo','business_registration_number','business_contact_number','business_type','business_address','active')

        except:

            worker_roles = BusinessProfile.objects.select_related('user').filter( workers = self.user)
            for c in worker_roles:
                business_currencys = c.user.default_currency_id
                wallet_id = c.user.wallet_id
                business_currency = business_currencys
                merchant_wallet_id = wallet_id
                merchant_country = c.user.country_of_residence

            if worker_roles:
                merchant_role = 'worker'
            else:
                merchant_role = self.user.account_type

        try:
            Country.objects.get( name = merchant_country , accept_kroon = True )
            merchant_accept_kroon = True
        except Country.DoesNotExist:
            merchant_accept_kroon = False

        try:
            user_plans = Merchant_Subcribers.objects.get( user = self.user , active = True)
            if user_plans:
                user_plan = user_plans.sub_plan_id
            merchant_subcription = user_plan
            
        except Merchant_Subcribers.DoesNotExist :
            merchant_subcription = "basic"

        
        user_promo_code = Government_Promo_Code.objects.filter( user = self.user )
        if user_promo_code.exists():
            promo_code = True
        else:
            promo_code = False

       
        # sending security email 
        # security_email = Login_Security_Email()
        # security_email.security_kiosk_email( self.user , self.user.full_name )
        # ends here
        # push products users
        
        if merchant_role == 'merchant':
            data['merchant_business_profle'] = merchant_business_profle

            merchant_products = Merchant_Product.objects.select_related('user', 'business_profile').filter(user=self.user)
            for i in merchant_products:
                if i.business_profile is None:
                    i.business_profile = my_business
                    i.save()
            
        data['merchant_accept_kroon'] = merchant_accept_kroon
        data['merchant_subscription'] = merchant_subcription
        data['merchant_role'] = merchant_role
        data['promo_code'] = promo_code
        data['merchant_wallet_id'] = merchant_wallet_id
        data['business_currency'] = business_currency

        return data


class SignupSerializer(serializers.ModelSerializer):

    PLATFROM = (
        ('kroon', _('kroon')),
        ('kiosk', _("kiosk")),
    )

    password = serializers.CharField(write_only=True)

    country_of_residence = serializers.CharField(
        source='country_of_residence.iso2',
        help_text=_('The ISO2 of the country.'))
    
    government_organization = serializers.BooleanField(
    )
    
    government_organization_name = serializers.CharField(
        source = 'government_organization_name.government_organization',
        min_length=1,
        max_length=250,
        required = False,
        allow_null=True,
    )

    country_province = serializers.IntegerField(
        required = False,
        allow_null=True,
    )

    email = serializers.EmailField(
        help_text=_("The primary email address of the user. An Email verification will be required upon successful registration."))

    contact_number = serializers.CharField(
        min_length=1,
        max_length=50,
        help_text=_('The contact number of the user.'))
    
    platform = serializers.ChoiceField( choices = PLATFROM )
        
    class Meta:
        model = User
        fields = [ 'first_name', 'last_name','email','gender','date_of_birth', 'contact_number','country_of_residence','country_province','account_type','accept_terms','agreed_to_data_usage','email_verification','government_organization','government_organization_name','device_id', 'password','device_fingerprint', 'platform' ]
   
    def get_cleaned_data(self):
            return {
                'name': self.validated_data.get('first_name') + " " + self.validated_data.get('last_name'),
                'first_name': self.validated_data.get('first_name'),
                'last_name': self.validated_data.get('last_name'),
                'email': self.validated_data.get('email'),
                'contact_number': self.validated_data.get('contact_number'),
                'account_type': self.validated_data.get('account_type'),
                'date_of_birth': self.validated_data.get('date_of_birth'),
                'gender': self.validated_data.get('gender'),
                'agreed_to_data_usage': self.validated_data.get('agreed_to_data_usage'),
                'email_verification': self.validated_data.get('email_verification'),
                'accept_terms': self.validated_data.get('accept_terms'),
                'government_registered': self.validated_data.get('government_organization'),
                'device_id': self.validated_data.get('device_id'),
                'password': self.validated_data.get('password'),
                'device_fingerprint': self.validated_data.get('device_fingerprint'),          
            }
            

    def validate_email(self, value):
        user_exist= User.objects.filter(email=value).exists()
        if user_exist:
            raise serializers.ValidationError("This email address used is already taken. Please login!")
        return value

    def validate_accept_terms(self,value):
        if not value:
            raise serializers.ValidationError("Terms and conditions cannot be blank")
        return value

    def validate_agreed_to_data_usage(self,value):
        if not value:
            raise serializers.ValidationError("use of data usage cannot be blank")
        return value


    def validate_device_fingerprint(self,value):
        if not value:
            raise serializers.ValidationError("device fingerprint cannot be blank")
        return value

    def validate_email_verification(self,value):
        if not value:
            raise serializers.ValidationError("email verification is required")
        return value

    def platform_verification(self,value):
        if not value:
            raise serializers.ValidationError("platform is required")
        return value

    def validate_email_verification_check(self,value):
        if value != True:
            raise serializers.ValidationError("email verification is required")    
        return value

    def validate_device_id(self,value):
        if not value :
            raise serializers.ValidationError("device id is required")    
        return value

    def validate_contact_number(self, value):
        contact_number= User.objects.filter(contact_number=value).exists()
        if contact_number:
            raise serializers.ValidationError("The contact number already exist.")    
        return value
    
    def validate_country_province(self, value):
        if value is not None:
            state_valid = Country_Province.objects.filter( id = value )
            if not state_valid:
                raise serializers.ValidationError("The state or province code provided is invalid or unavailable in our database.") 
        return value 

    def validate_country_of_residence(self, value):
        country_valid = Country.objects.filter(iso2=value.upper())
        if not country_valid:
            raise serializers.ValidationError("The country code provided is invalid or unavailable in our database.")    
        allowed_country = Country.objects.filter(iso2=value.upper(), accept_signup=True)
        if not allowed_country:
            raise serializers.ValidationError("Sorry we cant proceed , kroon is working to approve your country.")    
        return value
    
    def validate_government_organization_name(self, value):
        if value is not None:
            gov_org = Government_Organizations.objects.filter( government_organization = value)
            if not gov_org:
                raise serializers.ValidationError("The government organization id or name  provided is invalid or unavailable in our database.")    
        return value


    def save(self, request):
        country_of_residence = Country.objects.get(iso2=self.validated_data.get('country_of_residence')['iso2'])
        # group = Group.objects.get(name=self.validated_data.get('account_type').title())
        cleaned_data = self.get_cleaned_data()
        user = User(**cleaned_data)
        user.set_password(cleaned_data["password"])
        user.country_of_residence = country_of_residence
        user.default_currency_id = country_of_residence.currency

        government_organization = str(self.validated_data.get('government_organization_name')['government_organization'])

        if self.validated_data.get('government_organization'):
            gov_org_obj = Government_Organizations.objects.get( government_organization = government_organization )
            user.government_organization_name = gov_org_obj

        if self.validated_data.get('country_province') is not None:
            state_id = Country_Province.objects.get( id = self.validated_data.get('country_province') )
            user.country_province = state_id

        user.save()
        
        # automatically assigining the basic plan to the user 
        if self.validated_data.get('platform') == 'kiosk':
            default_plan = Subscription_Plan.objects.get( default_plan = True )
            try:
                Merchant_Subcribers.objects.get( user = user )
                pass
            except Merchant_Subcribers.DoesNotExist:
                days = default_plan.plan_duration
                end_date = datetime.now()+timedelta( days = days )
                Merchant_Subcribers.objects.create( user = user, plan = default_plan , end_date = end_date , active = True )


        if self.validated_data.get('government_organization'):
            try:
                # deactivating the old plan
                old_plan = Merchant_Subcribers.objects.get( user = user , active = True )
                old_plan.active = False
                old_plan.end_date = datetime.now()
                old_plan.save()
            except Merchant_Subcribers.DoesNotExist:
                pass
            # activating the plan
            code = Government_Promo_Code.objects.filter ( code_plan__slug_plan_name ="kiosk_plus" , used_code = False  ).first()
            plan = code.code_plan
            days = code.code_plan.plan_duration
            end_date = datetime.now()+timedelta( days = days )
            
            # activating the new plans
            Merchant_Subcribers.objects.create( user = user , active = True , plan = plan , end_date = end_date , sub_plan_id = plan.slug_plan_name )
           
            # expiring the promo code 
            code.used_code = True
            code.user = user
            code.save()

        return user

    
class LoginUserSerializer( serializers.Serializer):
    email = serializers.EmailField(required=False, allow_blank=True)
    password = serializers.CharField(style={'input_type': 'password'})

    def authenticate(self, **kwargs):
        return authenticate(self.context['request'], **kwargs)

    def _validate_email(self, email, password):
        user = None

        if email and password:
            user = self.authenticate(email=email, password=password)
        else:
            msg = _('Must include "email" and "password".')
            raise exceptions.ValidationError(msg)

        return user

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        user = None

        if 'allauth' in settings.INSTALLED_APPS:
            from allauth.account import app_settings

            # Authentication through email
            if app_settings.AUTHENTICATION_METHOD == app_settings.AuthenticationMethod.EMAIL:
                user = self._validate_email(email, password)

        # Did we get back an active user?
        if user:
            if not user.is_active:
                msg = _('User account is disabled.')
                raise exceptions.ValidationError(msg)
        else:
            msg = _('Unable to log in with provided credentials.')
            raise exceptions.ValidationError(msg)

        # If required, is the email verified?
        if 'rest_auth.registration' in settings.INSTALLED_APPS:
            from allauth.account import app_settings
            if app_settings.EMAIL_VERIFICATION == app_settings.EmailVerificationMethod.MANDATORY:
                email = user.emailaddress_set.get(email=user.email)
                if not email.verified:
                    raise serializers.ValidationError(_('E-mail is not verified.'))

        attrs['user'] = user
        return attrs


# Serialize UserAddress model.
class UserAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAddress
        fields = ('id','type', 'street_or_flat_number', 'street_name', 'building_name', 'state', 'city', 'zip_post_code')
        


class UserBankDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserBankDetails
        fields = "__all__"
        read_only_fields = ('user','integration_id','recipient_code','verified','bank_id','created_date', 'modified_date', )



class UserDetailsSerializer(serializers.ModelSerializer):
    address = UserAddressSerializer( read_only = True, many=True )
    bank_details = UserBankDetailsSerializer( read_only = True )
    virtual_cards = User_Virtual_Cards( read_only = True, many=True )
    class Meta:
        model = User
        fields = ('name','first_name', 'last_name', 'kyc_complete', 'kyc_complete_date', 'kyc_status', 'kyc_submitted', 'country_of_residence', 'default_currency_id', 'contact_number',  'merchant_business_name', 'kroon_token', 'wallet_id',  'submitted_bank_details', 'mobile_money_details_submitted','address', 'bank_details', 'email','app_version', 'account_type', 'date_of_birth' , 'virtual_cards','government_registered','government_organization_name',)
       

class UserOnlyInfo(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('name', 'wallet_id', 'email', 'contact_number')
        ref_name = "user_info"
       

class KroonTermsAndConditionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = KroonTermsAndConditions
        fields = "__all__"


class PolicyAndConditionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PolicyAndCondition
        fields = "__all__"

class PasswordChangeSerializer( serializers.Serializer):
    old_password = serializers.CharField(max_length=128, write_only=True, required=True)
    new_password1 = serializers.CharField(max_length=128, write_only=True, required=True)
    new_password2 = serializers.CharField(max_length=128, write_only=True, required=True)

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("old password is incorrect")
        return value

    def validate(self, data):
        if data['new_password1'] != data['new_password2']:
            raise serializers.ValidationError("the two password fields do not match")
            
        password_validation.validate_password(data['new_password1'], self.context['request'].user)
        return data

    def save(self, **kwargs):
        password = self.validated_data['new_password1']
        user = self.context['request'].user
        user.set_password(password)
        user.save()
        return user

class ForgetPasswordEmailNotification(serializers.Serializer):
    email = serializers.EmailField()


class ForgotPasswordSerilizer(serializers.Serializer):
    email = serializers.EmailField()
    new_password1 = serializers.CharField(max_length=128, write_only=True, required=True)
    new_password2 = serializers.CharField(max_length=128, write_only=True, required=True)

DEVICE_TYPE = (
    ('phone',_("Phone")),
    ('tab',_("Tap")),
)

class UpdateDeviceIdSerilizer (serializers.Serializer):
    device_id = serializers.CharField()
    device_type = serializers.ChoiceField( choices=DEVICE_TYPE )



class CategoriesSerilizer(serializers.ModelSerializer):
    class Meta:
        model = Category
        ref_name = 'business_category'
        fields = ['id','category']

class BusinessProfileSerilizer(serializers.ModelSerializer):
    business_category = CategoriesSerilizer( many = True )
    class Meta:
        model = BusinessProfile
        fields =  ['id', 'business_logo', 'business_registration_number','business_name', 'business_contact_number', 'business_address','business_category', 'business_type','business_id','created_date','workers',]
        read_only_fields = ('id','business_id','created_date','workers',)



class KroonFQASerializer(serializers.ModelSerializer):
    class Meta:
        model = KroonFQA
        fields = "__all__"
        read_only_fields = ('id','question','answer', 'created_date', 'modified_date',)


# Create a Kiosk FQA serializer.
class KioskFQASerializer(serializers.ModelSerializer):
    class Meta:
        model = KioskFAQ
        fields = "__all__"
        read_only_fields = ('id','question','answer', 'created_date', 'modified_date',)


class UpdateUserDeviceInfoSerializer(serializers.Serializer):
    device_fingerprint = serializers.CharField()
    device_type = serializers.CharField( required = False )
    app_version = serializers.CharField( required = False )
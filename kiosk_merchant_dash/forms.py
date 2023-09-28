from django import forms
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.forms import UserCreationForm
from requests import request
from datetime import timedelta, datetime
from django.utils import timezone
from kiosk_categories.models import Category

from locations.models import Country, Language
from kroon.users.models import User, BusinessProfile
from subscriptions.models import Subscription_Plan ,Merchant_Subcribers



class Email_VerificationForm(forms.Form):
    email = forms.EmailField(label="Your Email")

    def __init__(self, *args, **kwargs):
        super(Email_VerificationForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs['placeholder'] = _('your active email')
        
        self.fields['email'].help_text = _('So we can send you confirmation of your registration by sending you an OTP')


class OTPVerificationForm (forms.Form):
    otp = forms.IntegerField(label='Verification Number')

    def __init__(self, *args, **kwargs):
        super(OTPVerificationForm, self).__init__(*args, **kwargs)
        self.fields['otp'].widget.attrs['placeholder'] = _('your activation code')
        
        self.fields['otp'].help_text = _('Kindly input the activation code sent to you email.')


class MerchantSignupForm(UserCreationForm):
    
    first_name = forms.CharField(max_length=50, label='First name')
 
    last_name = forms.CharField(max_length=30, label='Last name')
 
    country_of_residence = forms.ModelChoiceField(
        queryset=Country.objects.filter(accept_signup=True).order_by('name'),
        empty_label=_('Country of Residence'),
        help_text=_('A proof of residence will be required.'))

    contact_number = forms.IntegerField(label='Contact number')

  
 
    def __init__(self, *args, **kwargs):
        super(MerchantSignupForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['placeholder'] = _('legal first & middle names')
        self.fields['last_name'].widget.attrs['placeholder'] = _('legal last Names')
        self.fields['contact_number'].widget.attrs['placeholder'] = _('your contact number')
        # self.fields['password'].widget.attrs['placeholder'] = _('input your security password')
        
        # help test
        self.fields['first_name'].help_text = _('As show in your documents')
        self.fields['last_name'].help_text = _('As show in your documents')
        self.fields['contact_number'].help_text = _('Your mobile number is needed to clearify your account.')

    class Meta:
        model = User
        fields = [ 'first_name', 'last_name', 'contact_number','country_of_residence',]
    

    def save(self,request, commit=True):
        user_currency = Country.objects.get( name = self.cleaned_data['country_of_residence'] )
        user = super(MerchantSignupForm, self).save(commit=False)
        user.email = request.session['email']
        user.email_verification = True
        user.accept_terms = True
        user.agreed_to_data_usage = True
        user.account_type = 'merchant'
        user.default_currency_id = user_currency.currency
        user.name = self.cleaned_data['first_name'] + " " + self.cleaned_data['last_name']
        if commit:
            user.save()
            # automatically assigining the basic plan to the user 
            default_plan = Subscription_Plan.objects.get( default_plan = True )
            try:
                Merchant_Subcribers.objects.get( user = user )
                pass
            except Merchant_Subcribers.DoesNotExist:
                days = default_plan.plan_duration
                end_date = datetime.now()+timedelta( days = days )
                Merchant_Subcribers.objects.create( user = user, plan = default_plan , end_date = end_date , active = True )
        return user


class KYC_Form (forms.ModelForm):
    
    business_name = forms.CharField()
    business_registration_number = forms.CharField( required = False , label = "Business Registration Number ( optional )")
    business_logo = forms.ImageField( required = False , label = "Business Logo ( optional )" )
    business_contact_number = forms.IntegerField()
    business_address = forms.CharField()
    business_category = forms.ModelMultipleChoiceField(
        queryset=Category.objects.filter( parent = None ),
        # empty_label=_('Country of Residence'),
        help_text=_('this shows the business category '))
    default = forms.BooleanField( label="Set As Default" )
    subscription_code = forms.CharField( required = False )

    class Meta:
        model = BusinessProfile
        fields = ('business_registration_number', 'business_logo', 'business_name', 'business_contact_number', 'business_address', 'business_category','business_type','subscription_code')

    def __init__(self, *args, **kwargs):
        super(KYC_Form, self).__init__(*args, **kwargs)
        self.fields['business_name'].widget.attrs['placeholder'] = _('your business name')
        self.fields['business_registration_number'].widget.attrs['placeholder'] = _('your business registration number')
        self.fields['business_contact_number'].widget.attrs['placeholder'] = _('your business contact number')
        self.fields['business_address'].widget.attrs['placeholder'] = _('your business address')
        self.fields['default'].widget.attrs['placeholder'] = _('make default')
        self.fields['subscription_code'].widget.attrs['placeholder'] = _('your subscription code')

        # help test
        self.fields['business_name'].help_text = _('kindly input your business name in the above form.')
        self.fields['business_contact_number'].help_text = _('your business contact number is needed')
        self.fields['business_address'].help_text = _('your business current address is needed.')
        self.fields['subscription_code'].help_text = _('kindly input your subscription code issued by the government, note this is optional.')
        self.fields['default'].help_text = _('This selects the business profile to be your default business profile')




class Edit_Business_Profile (forms.ModelForm):
    class Meta:
        model = BusinessProfile
        fields = ('business_registration_number', 'business_logo', 'business_name', 'business_contact_number', 'business_address', 'business_category', 'business_type')


class Business_Language_Form (forms.Form):
    language = forms.ModelChoiceField(
        queryset=Language.objects.all(),
        empty_label=_('Select your preferred language'),
        help_text=_('This is the default language for your merchant web dashboard.'))
from django import forms
from django.utils.translation import gettext_lazy as _
from kroon.users.models import User, UserAddress
from locations.models import Country, Country_Province
from django.contrib.auth.forms import UserCreationForm



class VerifyEmail(forms.Form):
    email = forms.EmailField()

    def __init__(self, *args, **kwargs):
        super(VerifyEmail, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs['placeholder'] = _('your workers email')
        
        self.fields['email'].help_text = _('Kindly input the workers email for verification , if the worker is already a kroon app user their inforomation will automatically be inputted')


class WorkerVerifyOtp(forms.Form):
    code = forms.IntegerField()

    def __init__(self, *args, **kwargs):
        super(WorkerVerifyOtp, self).__init__(*args, **kwargs)
        self.fields['code'].widget.attrs['placeholder'] = _('your workers verification code')
        
        self.fields['code'].help_text = _('Kindly input the workers verification code sent to their email, if the worker is already a kroon app user their inforomation will automatically be inputted on successful code verification.')



class WorkerSignupForm(UserCreationForm):
   
    first_name = forms.CharField(max_length=50, label='First name')
 
    last_name = forms.CharField(max_length=30, label='Last name')
 
    country_of_residence = forms.ModelChoiceField(
        queryset=Country.objects.filter(accept_signup=True).order_by('name'),
        empty_label=_('Country of Residence'),
        help_text=_('A proof of residence will be required.'))

    contact_number = forms.IntegerField(label='Contact number')

  
 
    def __init__(self, *args, **kwargs):
        super(WorkerSignupForm, self).__init__(*args, **kwargs)
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
        user = super(WorkerSignupForm, self).save(commit=False)
        user.email = request.session['email']
        user.email_verification = True
        user.accept_terms = True
        user.agreed_to_data_usage = True
        user.account_type = 'personal'
        user.name = self.cleaned_data['first_name'] + " " + self.cleaned_data['last_name']
        if commit:
            user.save()
        return user
    



class Gov_Worker_SignupForm(UserCreationForm):
   
    first_name = forms.CharField(max_length=50, label='First name')
 
    last_name = forms.CharField(max_length=30, label='Last name')
    
    province = forms.ModelChoiceField(
        queryset=Country_Province.objects.all(),
        empty_label=_('Province'),
        help_text=_('A province record is required '))

    country_of_residence = forms.ModelChoiceField(
        queryset=Country.objects.filter(accept_signup=True).order_by('name'),
        empty_label=_('Country of Residence'),
        help_text=_('A proof of residence will be required.'))

    contact_number = forms.IntegerField(label='Contact number')

  
 
    def __init__(self, *args, **kwargs):
        super(Gov_Worker_SignupForm, self).__init__(*args, **kwargs)
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
        fields = [ 'first_name', 'last_name', 'contact_number','country_of_residence','province',]
    

    def save(self,request, commit=True):
        user = super(Gov_Worker_SignupForm, self).save(commit=False)
        user.email = request.session['email']
        user.email_verification = True
        user.accept_terms = True
        user.agreed_to_data_usage = True
        user.account_type = 'personal'
        user.name = self.cleaned_data['first_name'] + " " + self.cleaned_data['last_name']
        if commit:
            user.save()
        return user
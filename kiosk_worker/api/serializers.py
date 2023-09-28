from rest_framework import serializers
from kroon.users.models import User, UserAddress
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth import password_validation
from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from locations.models import Country
from locations.api.serializers import CountryDetails


class WorkerAdress (serializers.ModelSerializer):

    class Meta:
        model = UserAddress
        fields = ('type','street_or_flat_number', 'street_name', 'building_name', 'state', 'city', 'zip_post_code')


class WorkerProfileSerializer(serializers.ModelSerializer):
    address = WorkerAdress( many=True, read_only=True )
    country_of_residence = CountryDetails(read_only=True)
    class Meta:
        model = User
        fields = ['name', 'email', 'contact_number', 'date_of_birth', 'gender', 'country_of_residence','address', 'created_date']


class CreateWorkersAccount( serializers.ModelSerializer):
    """
    this serializer is responsible for workers account creation.
    """
    password = serializers.CharField(write_only=True)
    country_of_residence = serializers.CharField(
        source='country_of_residence.iso2',
        help_text=_('The ISO2 of the country. '))

    email = serializers.EmailField(
        help_text=_("The primary email address of the user. An Email verification will be required upon successful registration."))

    contact_number = serializers.CharField(
        min_length=1,
        max_length=50,
        help_text=_('The contact number of the user.'))
        
    class Meta:
        model = User
        fields = [ 'first_name', 'last_name','email','gender', 'contact_number','country_of_residence','password']
   
    def get_cleaned_data(self):
            
            return {
                'name': self.validated_data.get('first_name') + " " + self.validated_data.get('last_name'),
                'first_name': self.validated_data.get('first_name'),
                'last_name': self.validated_data.get('last_name'),
                'email': self.validated_data.get('email'),
                'contact_number': self.validated_data.get('contact_number'),
                'date_of_birth': self.validated_data.get('date_of_birth'),
                'gender': self.validated_data.get('gender'),               
                'password': self.validated_data.get('password'),
            }
            

    def validate_email(self, value):
        user_exist= User.objects.filter(email=value).exists()
        if user_exist:
            raise serializers.ValidationError("This email address used is already taken. Please login!")    
        
        return value

    
    def validate_contact_number(self, value):
        contact_number= User.objects.filter(contact_number=value).exists()
        if contact_number:
            raise serializers.ValidationError("The contact number already exist.")    
            
        return value

    def validate_country_of_residence(self, value):
        country_valid = Country.objects.filter(iso2=value.upper())
        if not country_valid:
            raise serializers.ValidationError("The country code provided is Invalid or unavailable in our database.")    
            
        allowed_country = Country.objects.filter(iso2=value.upper(), accept_signup=True)
        if not allowed_country:
            raise serializers.ValidationError("Sorry we cant proceed , kroon is working to approve your country.")    
            
        return value

    def save(self, request):
        country_of_residence = Country.objects.get(iso2=self.validated_data.get('country_of_residence')['iso2'])
        # group = Group.objects.get(name=self.validated_data.get('account_type').title())
        cleaned_data = self.get_cleaned_data()
        user = User(**cleaned_data)
        user.set_password(cleaned_data["password"])
        user.country_of_residence = country_of_residence
        user.email_verification = True
        user.accept_terms = True
        user.agreed_to_data_usage = True
        user.account_type = 'personal'
        user.default_currency_id = country_of_residence.currency
        user.save()
        
        return user

    
from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from locations.models import Country



class Simulate_Account_Serializer( serializers.Serializer ):
    country_of_residence = serializers.CharField(
        source='country_of_residence.iso2',
        help_text=_('The ISO2 of the country that will be used during the create account simulation. '))
    
    account_limit = serializers.IntegerField(
        help_text=_('This hold the limit of the accounts that will be created'))
    

    def get_cleaned_data(self):
        return {
            'country_of_residence': self.validated_data.get('country_of_residence'),
            'account_limit': self.validated_data.get('account_limit'),
        }
    
    def validate_country_of_residence(self, value):
        """
        Check if the country iso2 is valid or been store in the database
        """
        country_valid = Country.objects.filter(iso2=value.upper())
        if not country_valid:
            raise serializers.ValidationError("The country code provided is Invalid or unavailable in our database.")
        return value
    

class Simulate_Product_Serializer( serializers.Serializer ):
    country_of_residence = serializers.CharField(
        source='country_of_residence.iso2',
        help_text=_('The ISO2 of the country that will be used during the create account simulation. '))
    
    # account_limit = serializers.IntegerField(
    #     help_text=_('This hold the limit of the accounts that will be created'))
    

    def get_cleaned_data(self):
        return {
            'country_of_residence': self.validated_data.get('country_of_residence'),
            # 'account_limit': self.validated_data.get('account_limit'),
        }
    
    def validate_country_of_residence(self, value):
        """
        Check if the country iso2 is valid or been store in the database
        """
        country_valid = Country.objects.filter(iso2=value.upper())
        if not country_valid:
            raise serializers.ValidationError("The country code provided is Invalid or unavailable in our database.")
        return value
import django_filters
from django_filters import DateFilter, CharFilter
from locations.models import Country_Province
from kroon.users.models import User , BusinessProfile



class Merchants_Filters (django_filters.FilterSet):
    email = CharFilter(field_name = 'email', lookup_expr ='icontains')
    name = CharFilter(field_name = 'name', lookup_expr ='icontains')
    class Meta:
        model = User
        fields = ['gender','kyc_complete','email','name',]


class Business_Filters (django_filters.FilterSet):
    business_registration_number = CharFilter(field_name = 'business_registration_number', lookup_expr ='icontains')
    business_name = CharFilter(field_name = 'business_name', lookup_expr ='icontains')
    class Meta:
        model = BusinessProfile
        fields = ['business_registration_number','business_name','business_contact_number','business_type',]
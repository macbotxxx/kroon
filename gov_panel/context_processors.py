
from helpers.common.currency_converter import usd_currency_converter
from kiosk_cart.models import Order
from kroon.users.models import BusinessProfile
from locations.models import Country_Province
from .models import Government_Organizations

# working on context

def gov_province(request):
    if request.user.is_authenticated:
        all_country_province = Country_Province.objects.select_related('country').filter(  country = request.user.country_of_residence ).order_by('created_date')
        # calculating the currency convert 
        merchants_revenue = Order.objects.select_related("user", "payment").filter( user__on_boarding_complete = True , is_ordered = True )
        total_revenue = 0
        for i in merchants_revenue:
            total_revenue += i.order_total
        currency = request.user.default_currency_id
        # currency = "ZAR"
        converted_revenue = usd_currency_converter( currency = currency , amount = total_revenue )

        # changing the context from province to state
        user_country = request.user.country_of_residence
        province_countries = [ 'South Africa' ]
        # validating the government worker country
        if user_country is not province_countries:
            state = True
        else:
            state = False

        # import all Nasme organizations
        nasme_orgs = Government_Organizations.objects.all()

    else:
        all_country_province = None
        total_revenue = 0
        converted_revenue = 0
        state = None
        nasme_orgs = None


    return dict( all_country_province = all_country_province , total_revenue_ZAR = total_revenue ,  total_revenue_USD = converted_revenue , state = state , nasme_orgs = nasme_orgs )



    

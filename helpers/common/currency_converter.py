import requests
from decimal import Decimal
from kroon_token.models import Currency_Convertion


from django.conf import settings
CURRENCY_CONVERT_API_KEY = settings.CURRENCY_CONVERT_API_KEY




def currency_converter( *args, **kwargs ):
    """
    this functions converts a currency to get the market value of the other one
    the defualt currency is USD
    """
    currency = kwargs.get('currency')

    url = f"https://api.currencyapi.com/v3/latest?apikey=8uD32TwvA8W7C0nsuvA3BIptIld9mHrKiorlcrsi&currencies={currency}"
   
    response = requests.request("GET", url).json()
    currency_rate = response['data'][f'{currency}']['value']
    currencyx = float(currency_rate)
    return currencyx



def usd_currency_converter( *args, **kwargs ):
    """
    currency converter function handle the converting of a local currency to usd
    """
    currency = kwargs.get('currency')
    amount = kwargs.get('amount')
    balance = 0
    # converting local currency to USD
    # checking if the conversion is store
    try:
        Currency_Convertion.objects.get( default_currency = currency )
    except Currency_Convertion.DoesNotExist:
        Currency_Convertion.objects.create( default_currency = currency )
        
    converter = Currency_Convertion.objects.get( default_currency = currency )
    balance = converter.convertion_rate * amount
    converted_balance = format(balance , '.2f')
    # returning the converted balance
    return converted_balance
    
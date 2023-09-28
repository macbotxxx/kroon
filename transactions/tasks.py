import pytz
import requests

from django.http import JsonResponse
from datetime import datetime
from decimal import Decimal
from django.conf import settings
# import celery
from config import celery_app
from celery.schedules import crontab

from transactions.models import Transactions
from kroon.users.models import User
from payments.models import Payment_Topup

utc=pytz.UTC



@celery_app.task( name = "cross_border_transfer" )
def cross_border_currency_convertion (*args , **kwargs):
    """
    currency converter function handle the converting of a local currency to usd
    """
    sender_currency = kwargs.get("sender_currency")
    reciepent_currency = kwargs.get("reciepent_currency")
    amount = kwargs.get("amount")

    # converting local currency to USD
    reqUrl = f"https://api.getgeoapi.com/v2/currency/convert?api_key={settings.CURRENCY_CONVERT_API_KEY}&format=json&from={sender_currency}&to={reciepent_currency}&amount={amount}"

    headersList = {
        "Accept": "*/*",
        "User-Agent": "Thunder Client (https://www.thunderclient.com)" 
    }

    payload = ""

    response = requests.request("GET", reqUrl, data=payload,  headers=headersList)

    response_data = response.json()
    print(response_data)
    
    # converted balance to USD decimal
    usd_balance = Decimal( response_data['rates'][f'{reciepent_currency}']['rate_for_amount'] )
    # with out formating 
    # print(response_data['rates']['USD']['rate_for_amount'])
    converted_balance = format(usd_balance, '.3f')

    # record saved 

    return converted_balance
    
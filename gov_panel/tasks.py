import requests
import string
import random
import pytz
import csv
import codecs
from contextlib import closing

# import Django Packages

from django.conf import settings
from django.utils import timezone
from django.conf import settings
from decimal import Decimal
from django.core.files.storage import default_storage as storage 

# import celery
from config import celery_app
from celery.schedules import crontab

# import from applications

from kroon.users.models import User
from subscriptions.models import Merchant_Subcribers
from gov_panel.models import Onboarding_Users_CSV
from locations.models import  Country_Province
from gov_panel.models import Onboarding_Users_CSV
from kroon_token.models import Currency_Convertion
from notifications.models import NewsFeed
from notifications.tasks import mobile_push_notification , send_merchants_datail_email


utc=pytz.UTC

# settings config import 
CURRENCY_CONVERT_API_KEY = settings.CURRENCY_CONVERT_API_KEY
FLUTTERWAVE_SECRET_KEY = settings.FLUTTERWAVE_SECRET_KEY
PAYSTACK_SECRET_KEY = settings.PAYSTACK_SECRET_KEY
# setting config import 


def password_geenrate():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

def ref_code():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=9))


@celery_app.task( name = "expired_merchant_subscriptions" )
def cancel_expired_subscriptions(*args , **kwargs):
    
    current_time = timezone.now()
    plans = Merchant_Subcribers.objects.filter( active = True )
    for i in plans:
        if i.end_date < current_time:
            i.active = False
            i.save()
        else:
            pass
    return 'completed'
        


@celery_app.task( name = "onboarding_action" )
def merchant_onboarding_process(*args , **kwargs):
    """
    this action is been carried out when ever the an onbaording is taking place
    the csv format which is submitted by the super merchant user will be used to gather 
    information about the onboarding process.
    """
    users_csv_file = Onboarding_Users_CSV.objects.select_related('on_boarding_user').filter( on_boarding_complete = False ).order_by('-created_date')[0:1]

    for i in users_csv_file: 
        file_name = i.on_boarding_user_file.name 
        onboarding_user = i.on_boarding_user
        url = f'https://test-server-space.nyc3.digitaloceanspaces.com/kroon-kiosk-test-static/{file_name}'
        
        with closing(requests.get(url, stream=True)) as r:
            f = csv.reader(codecs.iterdecode(r.iter_lines(), 'utf-8'))
            try:
                for id,first_name,last_name,email,business_name,province, *__ in f:
                    # generating unique password 
                    password = password_geenrate()
                    # getting each province ID 
                    user_province = Country_Province.objects.get( id = province )
                    
                    checking_user = User.objects.filter(email=email)
                    if checking_user:
                        pass
                    else:
                        wallet_id = ref_code()

                        user = User(
                            email=email,
                            first_name=first_name, 
                            last_name=last_name,
                            name = first_name + ' ' + last_name,
                            merchant_business_name=business_name,
                            account_type = "merchant",
                            wallet_id = wallet_id,
                            country_of_residence = onboarding_user.country_of_residence,
                            country_province = user_province,
                            default_currency_id = onboarding_user.default_currency_id,
                            on_boarding_user = onboarding_user,
                            on_boarding_complete = True,
                            accept_terms = True,
                            agreed_to_data_usage = True,
                            generated_password = password,
                            )
                        user.set_password(password)
                        # data.append(user)
                        user.save()
                # User.objects.bulk_create(data)
                # updating the onboarding status to True
                i.on_boarding_complete = True
                i.on_boarding_complete_date = timezone.now()
                i.save()
                # max onboarding process ends here 
                return 'users registration is handled'
            except:
                # this exception is taken action if the file is not the initial format
                # users_csv_file.delete()
                return 'users transfer not handled'
    return 'error' 



@celery_app.task( name = "send_account_details" )
def send_account_details( *args, **kwargs ):
    """
    email notification will be sent to the onboarded merchants
    which the email contains the necessary information for registration and 
    completing the onboarding process.
    """
    # Getting the users that has been onboarded
    # but havent been sent their login details
    all_users = User.objects.select_related('country_of_residence', 'country_province', 'on_boarding_user', 'bank_details').filter(email_details = False , on_boarding_complete = True )[:50]
    
    for merchant in all_users:
        email = merchant.email
        name = merchant.name
        default_password = merchant.generated_password
        # update the account detail action
        update_action = User.objects.get(email = email )
        update_action.email_details = True
        update_action.save()
        # sending email with user details
        send_merchants_datail_email( email = email, name = name )
    return 'users registration'



@celery_app.task( name = "publish_newsfeed" )
def publishing_newfeed( *args, **kwargs ):
    """
    this publishing function is called after some mins 
    """ 
    notification_type = "newsfeed"
    # current datetime 
    current_datetime = timezone.now()
    # getting all news feed that the current time is greater than
    # the publishing time ........
    qs = NewsFeed.objects.filter( status = False , gov_post = True )
    for q in qs:
        # if q.publishing_time < current_datetime:
        # send a push notification to the merchants
        merchant_qs = User.objects.select_related( 'country_of_residence', 'country_province', 'on_boarding_user', 'bank_details', ).filter( on_boarding_complete = True )
        for merchants in merchant_qs:
            # pushing mobile notifications 
            platform = "kiosk" # the options are.... kroon or kiosk...
            device_id = f'{merchants.device_id}'
            title = f"{q.title}"
            body = f"{q.content}"
            device_type = f"{merchants.device_type}"
            mobile_push_notification( device_id = device_id, title = title, body = body , platform = platform , device_type = device_type , notification_type = notification_type )
        # updating newsfeed status
        q.status = True
        q.save()
        return "news feed sent"
        # else:
            # return 'no news feed'
            


@celery_app.task( name = "currency_converter" )
def currency_convertion(*args , **kwargs):
    """
    currency converter function handle the converting of a local currency to usd
    this occure to carry out the convertion in real time.
    """
    currency = "ZAR"
    amount = 1
    # converting local currency to USD
    reqUrl = f"https://api.getgeoapi.com/v2/currency/convert?api_key={CURRENCY_CONVERT_API_KEY}&format=json&from={currency}&to=USD&amount={amount}"

    headersList = {
        "Accept": "*/*",
        "User-Agent": "Thunder Client (https://www.thunderclient.com)" 
    }

    payload = ""

    response = requests.request("GET", reqUrl, data=payload,  headers=headersList)

    response_data = response.json()
    
    # converted balance to USD decimal
    usd_balance = Decimal( response_data['rates']['USD']['rate_for_amount'] )
    # with out formating 
    # print(response_data['rates']['USD']['rate_for_amount'])
    converted_balance = format(usd_balance, '.3f')

    # savinig the recordss on our db
    try: 
        # get the previous record and updates it 
        convertion_record = Currency_Convertion.objects.get( default_currency = currency )
        convertion_record.default_currency = currency
        convertion_record.convertion_rate = converted_balance
        convertion_record.save()
    except Currency_Convertion.DoesNotExist:
        # create a new conversion record 
        convertion_record = Currency_Convertion()
        convertion_record.default_currency = currency
        convertion_record.convertion_rate = converted_balance
        convertion_record.save()
    # record saved 

    return 'conversion record created successfully'
            


celery_app.conf.beat_schedule = {
    # Execute the cancelling of expired merchants sub every 1 minute
    'cancel-subscriptions': {
        'task': 'expired_merchant_subscriptions',
        'schedule': crontab(minute='*/1'),
    },
    # This action completes the merchants onbaording
    'merchants-onboarding': {
        'task': 'onboarding_action',
        'schedule': crontab(minute='*/50'),
    },
    # This tasks is carried out to converts currency values once in a day 
    'currency-convertion': {
        'task': 'currency_converter',
        'schedule': crontab(hour='*/9'),
    },
    # This execute the action to complete the newsfeed in 10 mins 
    # 'newsfeed-publisher': {
    #     'task': 'publish_newsfeed',
    #     'schedule': crontab(minute='*/10'),
    # },
    # This execute the process of sending out details by email
    'merchants-account-details': {
        'task': 'send_account_details',
        'schedule': crontab(minute='*/10'),
    },
} 
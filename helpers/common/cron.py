import requests
import json
import string
import random
import datetime
import pytz
import csv

utc=pytz.UTC

from datetime import datetime, timezone
from django.http import JsonResponse
from django.conf import settings
from datetime import timedelta, date
from decimal import Decimal
from django.core.files.storage import default_storage as storage 
from django.core.mail import send_mail


from transactions.models import Transactions
from payments.models import Payment_Topup
from working_tasks.models import TaskTest # importing the test model
from kroon_withdrawal.models import Kroon_Withdrawal_Record
from kroon.users.models import User
from subscriptions.models import Merchant_Subcribers
from gov_panel.models import Onboarding_Users_CSV
from locations.models import Country , Country_Province
from gov_panel.models import Onboarding_Users_CSV
from kroon_token.models import Currency_Convertion


# settings config import 
CURRENCY_CONVERT_API_KEY = settings.CURRENCY_CONVERT_API_KEY
FLUTTERWAVE_SECRET_KEY = settings.FLUTTERWAVE_SECRET_KEY
PAYSTACK_SECRET_KEY = settings.PAYSTACK_SECRET_KEY
# setting config import 


def password_geenrate():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))


def ref_code():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=9))


def my_scheduled_job():
    # getting current date 
    estimated_delivery = date.today() 
    # TaskTest.objects.create(content = estimated_delivery )
    # # loopiing through the table to verify if the job is scheduled
    task_record = Kroon_Withdrawal_Record.objects.filter( estimated_delivery = estimated_delivery , is_approved = False , withdrawal_type = 'local_bank' )

    for i in task_record:
        """
        getting the information for the country that is allowed by paystack
        currently we have only Nigeria
        """

        if str(i.user.country_of_residence) == "Nigeria":
            reqUrl = "https://api.paystack.co/transfer"
            print('he')
            headersList = {
            "Authorization": f"Bearer {PAYSTACK_SECRET_KEY}",
            "Content-Type": "application/json" 
            }

            payload = json.dumps({ 
                "source": "balance", 
                "amount": f"{round(i.amount)}00", 
                "recipient": f"{i.recipient_code}", 
                "reason": f"{i.narration}" 
                })

            response = requests.request("POST", reqUrl, data=payload,  headers=headersList)
            response_data = response.json()
            print(response_data)
          
            if str(response_data["status"]) == "True":
                amount = response_data['data']['amount']
                transfer_code = response_data['data']['transfer_code']
                reference = response_data['data']['reference']
                
                # getting the users currency
                user_currency = i.user.default_currency_id
                user_token = User.objects.get(id = i.user.id)
                
                withdraw_record = Kroon_Withdrawal_Record.objects.get( reference = i.reference )
                withdraw_record.transaction_id = transfer_code
                withdraw_record.paystack_reference = reference
                # withdraw_record.fee = Decimal(fees),

                # withdraw_record.status = "successful"
                withdraw_record.is_approved = True
                withdraw_record.save()
                
                # Recipient Transactional Record History
                Transactions.objects.create( user = i.user , benefactor = i.user,amount = Decimal(i.amount_in_kroon),transactional_id = i.reference, currency = 'KC',local_currency = i.currency,amount_in_localcurrency = Decimal( amount ), narration = f'Local Bank withdrawal has been settled ',action = 'LOCAL BANK WITHDRAWAL', status = "processing", debited_kroon_amount = Decimal(i.amount_in_kroon) , kroon_balance = user_token.kroon_token )

                return JsonResponse ('done handling the transfer', safe = False)

            else:
                return JsonResponse ('transfer not handled', safe = False)

        else:

            """
            Initiating the local bank withdrawal thorugh the third party payment
            this stores and update the transactional history,
            """

            url = "https://api.flutterwave.com/v3/transfers"

            payload = json.dumps({
                "account_bank": f"{i.bank_code}",
                "account_number": f"{i.account_number}",
                "amount": f"{Decimal(i.amount)}",
                "narration": "Withdrawal to local banks",
                "currency": f"{i.currency}",
                "reference": f"{i.reference}",
                "beneficiary_name": f"{i.beneficiary_name}",
                # "callback_url": "https://kroonapp.xyz/webhook/push-webhook/",
                
                "meta": {
                    "first_name": f"{i.user.first_name}",
                    "last_name": f"{i.user.last_name}",
                    "email": f"{i.user.email}",
                    "mobile_number": f"{i.user.contact_number}",
                    "recipient_address": f"{i.billing_recipient_address}",
                    "action": f"{'local_bank'}"
                }
            })

            headers = {
            'Authorization': f'Bearer {FLUTTERWAVE_SECRET_KEY}',
            'Content-Type': 'application/json'
            }

            response = requests.request("POST", url, headers=headers, data=payload)

            response_data = response.json()
            print(response_data)
        
            status_pay = response_data['status']
            
            if status_pay == "success":
                
                amount = response_data['data']['amount']
                # fees = response_data['data']['fee']
                
                # getting the users currency
                user_currency = i.user.default_currency_id
                user_token = User.objects.get(id = i.user.id)
                
                withdraw_record = Kroon_Withdrawal_Record.objects.get( reference = i.reference )

                withdraw_record.transaction_id = response_data['data']['id']
                # withdraw_record.fee = Decimal(fees),

                # withdraw_record.status = 'successful'
                withdraw_record.is_approved = True
                withdraw_record.save()
                
                # Recipient Transactional Record History
                Transactions.objects.create( user = i.user , benefactor = i.user,amount = Decimal(i.amount_in_kroon),transactional_id = i.reference, currency = 'KC',local_currency = i.currency,amount_in_localcurrency = Decimal( i.amount ), narration = f'Local Bank withdrawal has been settled ',action = 'LOCAL BANK WITHDRAWAL', status = 'processing', debited_kroon_amount = Decimal(i.amount_in_kroon) , kroon_balance = user_token.kroon_token )

                return JsonResponse ('done handling the transfer', safe =False)

            else:                
                # amount = response_data['data']['amount']
                # fees = response_data['data']['fee']

                if response_data['status'] == 'failed':
                    status_code = "failed"
                elif response_data['status'] == 'error':
                    status_code = "error"

                withdraw_record = Kroon_Withdrawal_Record.objects.get( reference = i.reference )

                # withdraw_record.transaction_id = response_data['data']['id'],
                # withdraw_record.fee = Decimal(fees),
                withdraw_record.is_approved = True
                withdraw_record.status = "failed"
                withdraw_record.save()
                
                # Recipient Transactional Record History
                Transactions.objects.create(user = i.user , benefactor = i.user,amount = Decimal(i.amount_in_kroon),transactional_id = i.reference, currency = 'KC',local_currency = i.currency,amount_in_localcurrency = i.amount, narration = response_data['data']['complete_message'],action = 'LOCAL BANK WITHDRAWAL', status = status_code, kroon_balance = i.user.kroon_token)

                return JsonResponse ('this transaction is failed', safe =False)


    return JsonResponse ('nothing in the database', safe =False)
        

def cancel_pending_topup ():
    # getting all pending transactions
    pending_transactions = Payment_Topup.objects.filter( status='pending' )
    #checking and verifying if the pin is invalid or expired  
    current_time = datetime.now()
    # check_otp_duration = utc.localize(check_otp.duration)
    current_time = utc.localize(current_time)
    for i in pending_transactions:
        if i.pending_duration is not None:
            if i.pending_duration < current_time:
                # updating the transactional table status to cancelled
                update_transaction = Transactions.objects.get ( transactional_id = i.payment_ref)
                update_transaction.status = 'cancelled'
                update_transaction.save()

                # updating the payment transaction status
                i.status = 'cancelled'
                i.save()

                return JsonResponse ('this transaction status is updated', safe =False)

            else:
                return JsonResponse ('this transaction status is on pending', safe =False)

        else:
            return JsonResponse ('this transaction has no pending', safe =False)

    return JsonResponse ('transaction is not working', safe =False)


def cancel_expired_subscriptions ():
    
    current_time = datetime.now()
    # check_otp_duration = utc.localize(check_otp.duration)
    current_time = utc.localize(current_time) 
    plans = Merchant_Subcribers.objects.filter( active = True )
    for i in plans:
        if i.end_date < current_time:
            i.active = False
            i.save()
            return JsonResponse ('this transaction has no pending', safe =False)
        else:
            pass



def merchant_onboarding_process():
    users_csv_file = Onboarding_Users_CSV.objects.select_related('on_boarding_user').filter( on_boarding_complete = False )
    for i in users_csv_file:
        onboarding_user = i.on_boarding_user
        new_file = i.on_boarding_user_file.name
        with storage.open(new_file, 'r') as f:
            csvf = csv.reader(f)
            data = []
    
            try:
                for id,first_name,last_name,email,business_name,province, *__ in csvf:
                    # generating unique password 
                    password = password_geenrate()
                    print(password)
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
                            )
                        user.set_password(password)
                        data.append(user)
                User.objects.bulk_create(data)
                print(password)
                i.on_boarding_complete = True
                i.on_boarding_complete_date = datetime.now()
                i.save()
                return JsonResponse ('users registration is handled', safe = False)
            except:
                users_csv_file.delete()
                return JsonResponse ('users transfer not handled', safe = False)
    


def currency_convertion ():
    """
    currency converter function handle the converting of a local currency to usd
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

    return JsonResponse ('conversion record created successfully', safe = False)
    




def testemail():

    send_mail(
        'Subject here',
        'Here is the message.',
        'from@example.com',
        ['to@example.com'],
        fail_silently=False,
    )
    return JsonResponse ('users registration', safe = False)



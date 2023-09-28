from django.http import JsonResponse
import requests
import json
import random
import string

from django.conf import settings
from datetime import timedelta, date
from decimal import Decimal

from transactions.models import Transactions

from .models import Test_Models # importing the test model
from kroon_withdrawal.models import Kroon_Withdrawal_Record
from kroon.users.models import User

FLUTTERWAVE_SECRET_KEY = settings.FLUTTERWAVE_SECRET_KEY

def my_scheduled_job():
    # getting current date 
    estimated_delivery = date.today() 
    test_flow = Test_Models.objects.create(content = estimated_delivery )
    # loopiing through the table to verify if the job is scheduled
    task_record = Kroon_Withdrawal_Record.objects.filter( estimated_delivery = estimated_delivery , is_approved = False , withdrawal_type = 'local_bank' )

    for i in task_record:
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

            withdraw_record.transaction_id = response_data['data']['id'],
            # withdraw_record.fee = Decimal(fees),

            withdraw_record.status = "successful",
            withdraw_record.is_approved = True
            withdraw_record.save()
            
            # Recipient Transactional Record History
            Transactions.objects.create( user = i.user , benefactor = i.user,amount = Decimal(i.amount_in_kroon),transactional_id = i.reference, currency = 'KC',local_currency = i.currency,amount_in_localcurrency = Decimal( i.amount ), narration = f'Local Bank withdrawal has been queued ',action = 'LOCAL BANK WITHDRAWAL', status = 'successful', debited_kroon_amount = Decimal(i.amount_in_kroon) , kroon_balance = user_token.kroon_token )

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
            withdraw_record.is_approved = True,
            withdraw_record.status = "failed",
            withdraw_record.save()
            
            # Recipient Transactional Record History
            Transactions.objects.create(user = i.user , benefactor = i.user,amount = Decimal(i.amount_in_kroon),transactional_id = i.reference, currency = 'KC',local_currency = i.currency,amount_in_localcurrency = i.amount, narration = response_data['data']['complete_message'],action = 'LOCAL BANK WITHDRAWAL', status = status_code, kroon_balance = i.user.kroon_token)

            return JsonResponse ('this transaction is failed', safe =False)


    return JsonResponse ('nothing in the database', safe =False)
        

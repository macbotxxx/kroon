import requests
import json

from django.conf import settings
from django.core.mail import send_mail


class PayStack:

    PAYSTACK_SECRET_KEY = settings.PAYSTACK_SECRET_KEY
    base_url = 'https://api.paystack.co'
    verify_bank = 'https://api.paystack.co/bank'

    def verify_payment_paystack(self, payment_ref, *args, **kwargs):
        path = f'/transaction/verify/{payment_ref}'

        headers = {
            "Authorization": f"Bearer {self.PAYSTACK_SECRET_KEY}",
            'Content-Type': 'application/json',
        }

        url = self.base_url + path
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            response_data = response.json()
           
            return response_data['status'],response_data['data']
            
        response_data = response.json()
        
        return response_data['status'],response_data['message']


    def verify_account_number (self, account_number, bank_code, *args, **kwargs):
        path = f'/resolve?account_number={account_number}&bank_code={bank_code}'
        headers = {
            "Authorization": f"Bearer {self.PAYSTACK_SECRET_KEY}",
            'Content-Type': 'application/json',
        }

        url = self.base_url + path
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            response_data = response.json()
            # return response_data['status'],response_data['data']
            print(response_data)
            
        response_data = response.json()
       
        print(response_data)

        # return response_data['status'],response_data['message']
   


class FlutterWave:
    if settings.TEST_PAYMENT:
        FLUTTERWAVE_SECRET_KEY = settings.FLUTTERWAVE_SECRET_KEY_TEST
    else:
        FLUTTERWAVE_SECRET_KEY = settings.FLUTTERWAVE_SECRET_KEY

    base_url = 'https://api.flutterwave.com/v3/transactions/'

    def verify_payment_flutterwave (self, payment_ref, *args, **kwargs):
        path = 'verify_by_reference?tx_ref='f"{payment_ref}"
       
        headers = {
            "Authorization": f"Bearer {self.FLUTTERWAVE_SECRET_KEY}",
            'Content-Type': 'application/json',
        }

        url = self.base_url + path
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            response_data = response.json()
            send_mail(
                'Response',
                f'{response_data}',
                f"{settings.EMAIL_HOST_USER}" ,
                ['assanamamichael@gmail.com'],
                fail_silently=False,
            )
            return response_data['status'],response_data['data']
        response_data = response.json()
        send_mail(
                'Response',
                f'{response_data}',
                f"{settings.EMAIL_HOST_USER}" ,
                ['assanamamichael@gmail.com'],
                fail_silently=False,
            )
        return response_data['status'],response_data['message']
    


class Etransac:
    if settings.TEST_PAYMENT:
        ETRANSAC_PUBLIC_KEY = settings.ETRANSAC_PUBLIC_KEY_TEST
        ETRANSAC_SECRET_KEY = settings.ETRANSAC_SECRET_KEY_TEST
       
    else:
        ETRANSAC_PUBLIC_KEY = settings.ETRANSAC_PUBLIC_KEY
        ETRANSAC_SECRET_KEY = settings.ETRANSAC_SECRET_KEY

    def payment_initialize (self, *args, **kwargs):
        url = "https://api.public.credodemo.com/transaction/initialize/"
        payload = json.dumps({
        "amount": int(kwargs.get('amount')) * 100,
        "bearer": 0,
        "callbackUrl": "https://example.com/verify/938w9u30e9dsuoweds/",
        "channels": [
            "card"
        ],
        "currency": "NGN",
        "customerFirstName": f"{kwargs.get('customer_first_name')}",
        "customerLastName":f"{kwargs.get('customer_last_name')}",
        "customerPhoneNumber": f"{kwargs.get('customer_contact_number')}",
        "email": f"{kwargs.get('customer_email')}",
        "metadata": {
            "bankAccount": "0114877128",
            "customFields": [
            {
                "variable_name": "gender",
                "value": "Male",
                "display_name": "Gender"
            }
            ]
        },
        "reference": f"{kwargs.get('payment_refrence')}"
        })

        headers = {
        'Authorization': f'{self.ETRANSAC_PUBLIC_KEY}',
        'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload)

        if response.status_code == 200:
            response_data = response.json()
            return response_data['data']
        else:
            return 'nothing working'

    
    def verify_payment (self):
        pass



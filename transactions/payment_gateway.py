from django.conf import settings
from django.core.mail import send_mail
<<<<<<< HEAD
# michsel
=======

>>>>>>> 77aede60deec7c5b49e2b4ed733354ee6044c384
import requests


class PayStack:
    PAYSTACK_SECRET_KEY = settings.PAYSTACK_SECRET_KEY
    base_url = 'https://api.paystack.co'
    verify_bank = 'https://api.paystack.co/bank'

    def verify_payment(self, payment_ref, *args, **kwargs):
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
    FLUTTERWAVE_SECRET_KEY = settings.FLUTTERWAVE_SECRET_KEY
    base_url = 'https://api.flutterwave.com/v3/transactions/'

    def verify_payment(self, payment_ref, *args, **kwargs):
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



class Monnify:
    """
    COMING SOON 
    """

    pass
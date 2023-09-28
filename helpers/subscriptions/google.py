import os
import base64
import requests
import json
import pytz
from django.conf import settings
from django.utils import timezone
from pytz import timezone as pytz_timezone
from helpers.common.convert_time import milliseconds_to_local_datetime , convert_timezone_to_localtime
from google.oauth2 import service_account
from google.auth.transport.requests import Request




class Google_Service:
    """
    An App Store receipt is a binary encrypted file signed with an Apple certificate. In order to read the contents of the encrypted file, you need to pass it through the verifyReceipt endpoint. The endpoint’s response includes a readable JSON body. Communication with the App Store is structured as JSON dictionaries, as defined in RFC 4627. Binary data is Base64-encoded, as defined in RFC 4648. Validate receipts with the App Store through a secure server.
    """

    # GOOGLE_PWD = settings.GOOGLE_PWD
    sandbox_url = 'https://sandbox.itunes.apple.com/verifyReceipt'
    base_url = 'https://buy.itunes.apple.com/verifyReceipt'
    
    def obtain_credentials (self):
        service_account_file = settings.BASE_DIR / "kroon/kroonkiosk2cebb3b19a45.json"
        # Define the required scopes
        scopes = ['https://www.googleapis.com/auth/androidpublisher']

        # Load the service account credentials from the JSON key file
        credentials = service_account.Credentials.from_service_account_file(
            service_account_file, scopes=scopes)

        # Check if the credentials have expired
            # Refresh the credentials if they have expired
        credentials.refresh(Request())

        # Obtain the access token from the credentials

        access_token = credentials.token

        return access_token



    def verify_subscription_token(self, subcription_id , receipt_data ):
        
        access_token = self.obtain_credentials()
        print(access_token)
        
        url = f"https://www.googleapis.com/androidpublisher/v3/applications/com.kroon.kiosk/purchases/subscriptions/{subcription_id}/tokens/{receipt_data}"
        # ljolfpgbhajhdeifcgiglkmi.AO-J1OwqAkuWvoChYjhRhLx30QZMe5-K4-4Om35iZXpXUvWcW0JQ911MHnvjVsBOzUoCcJVZv3zwWe_eXV5CWt6PxQI8G_g3gA

        payload = {}
        headers = {
        'Authorization': f'Bearer {access_token}'
        }

        response = requests.request("GET", url, headers=headers, data=payload)
        res = response.json()
        if response.status_code == 200:
            milliseconds = res['expiryTimeMillis']
            exp_date_local = milliseconds_to_local_datetime(milliseconds)
            current_date = timezone.now()
            esp_date = exp_date_local.replace(tzinfo=pytz.utc)

            if current_date > esp_date:
                active = False
            else:
                active = True
           
            action = {'status_action': active , 'exp_date':esp_date }
           
        else:
            action = False

        return action
    

   
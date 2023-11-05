import pytz
import requests
import json
from django.conf import settings
from django.utils import timezone
from datetime import datetime
from pytz import timezone as pytz_timezone
from helpers.common.convert_time import milliseconds_to_local_datetime , convert_timezone_to_localtime




class Apple_Service:
    """
    An App Store receipt is a binary encrypted file signed with an Apple certificate. In order to read the contents of the encrypted file, you need to pass it through the verifyReceipt endpoint. The endpoint’s response includes a readable JSON body. Communication with the App Store is structured as JSON dictionaries, as defined in RFC 4627. Binary data is Base64-encoded, as defined in RFC 4648. Validate receipts with the App Store through a secure server.
    """

    APPLE_PWD = settings.APPLE_PWD
    sandbox_url = 'https://sandbox.itunes.apple.com/verifyReceipt'
    base_url = 'https://buy.itunes.apple.com/verifyReceipt'
    
    def verify_receipt_data (self, receipt_data):
        
        url = f"{self.base_url}"
        payload = json.dumps({
            "exclude-old-transactions": True,
            "password": f"{self.APPLE_PWD}",
            "receipt-data": f"{receipt_data}"
            })
        headers = {
                'Content-Type': 'application/json'
                }

        response = requests.request("POST", url, headers=headers, data=payload)
        res = response.json()
        if res['status'] == 21007:
            url = f"{self.sandbox_url}"
            payload = json.dumps({
                "exclude-old-transactions": True,
                "password": f"{self.APPLE_PWD}",
                "receipt-data": f"{receipt_data}"
                })
            headers = {
                    'Content-Type': 'application/json'
                    }

            response = requests.request("POST", url, headers=headers, data=payload)
            resp = response.json()
            milliseconds = resp["latest_receipt_info"][0]['expires_date_ms']
            esp_date = milliseconds_to_local_datetime(milliseconds)
            current_date = timezone.now()
            converted_datetime = esp_date.replace(tzinfo=pytz.utc)
        
            if current_date > converted_datetime:
                active = False
            else:
                active = True
           
            action = {'status_action': active , 'exp_date':converted_datetime }
        else:
            action = False
            
        return action

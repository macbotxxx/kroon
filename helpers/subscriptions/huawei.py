import base64
import pytz
import requests
import json
from django.conf import settings
from django.utils import timezone
from datetime import datetime
from pytz import timezone as pytz_timezone
from helpers.common.convert_time import milliseconds_to_local_datetime , convert_timezone_to_localtime




class Huawei_Service:
        
        def get_accesss_token(self):
             
            """
            Obtain the app-level access token
            """
          
            url = "https://oauth-login.cloud.huawei.com/oauth2/v3/token"

            payload = 'client_secret=e257b6b6726ed3b3b3dc778bc3bba5179ea2e0885278cfc75f31268e85052054&client_id=108112425&grant_type=client_credentials'
            headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
            }

            response = requests.request("POST", url, headers=headers, data=payload)
            jsonObject = json.loads(response.text)
            accessToken = jsonObject['access_token']
            oriString = "APPAT:%s" % accessToken
            authorization = "Basic %s" % str(base64.b64encode(oriString.encode('utf-8')), 'utf-8')
            return authorization
        


        def subscription_verification(self ,  subcription_id , receipt_data ):
            url = "https://subscr-dre.iap.cloud.huawei.eu/sub/applications/v2/purchases/get"

            payload = json.dumps({
            "purchaseToken": f"{receipt_data}",
            "subscriptionId": f"{subcription_id}"
            })
            headers = {
            'Authorization': f'{self.get_accesss_token()}',
            'Content-Type': 'application/json'
            }

            response = requests.request("POST", url, headers=headers, data=payload)
            res = response.json()
            # Parse the JSON string
            json_data = json.loads(res['inappPurchaseData'])
            # Access the renewStatus parameter
            milliseconds = json_data['expirationDate']
            esp_date = milliseconds_to_local_datetime(milliseconds)
            converted_datetime = esp_date.replace(tzinfo=pytz.utc)
            current_date = timezone.now()
        
            if current_date > converted_datetime:
                active = False
            else:
                active = True
            action = {'status_action': active , 'exp_date':converted_datetime }
            # j_data = json.loads(res['inappPurchaseData'])
            
            return action



    
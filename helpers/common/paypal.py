
import requests
import json

from django.conf import settings

PAYPAL_CID = settings.PAYPAL_CID
PAYPAL_SECRET_ID = settings.PAYPAL_SECRET_ID
PAYPAL_SANDBOX = settings.PAYPAL_SANDBOX


"""
this script hold the function and paypal api calls for merchant
subscriptions actibvate and deactivate subscriptions
"""

if PAYPAL_SANDBOX:
    url = "https://api-m.sandbox.paypal.com/v1/oauth2/token"
    cid =  "Acf-VAuyB6NmUCxEPA4u9Y8Ft_TKXFDQqxDunQW4JZ1ae0oDYPZBE597m58zvSUFkEocqBE2PTWxN1xm"
    secret_id = "EHlwg6Tt7nY5KdJXosLGgiRaiVXY06m4kpASLXBk9cuqiIVrTE5Li-abUZT1H7m0jWrTp-XBk88FI-YD"

    # deactivate subscription plan
    deactivate_url = "https://api-m.sandbox.paypal.com/v1/billing/subscriptions/{ subscription_ids }/cancel"

else:
    url = "https://api-m.paypal.com/v1/oauth2/token"
    cid = PAYPAL_CID
    secret_id = PAYPAL_SECRET_ID

    # deactivate subscription plan
    deactivate_url = "https://api-m.paypal.com/v1/billing/subscriptions/{ subscription_ids }/cancel"



def get_access_token():
    """
    Getting the paypal access token 
    """
    if PAYPAL_SANDBOX:
        url = "https://api-m.sandbox.paypal.com/v1/oauth2/token"
        cid =  "Acf-VAuyB6NmUCxEPA4u9Y8Ft_TKXFDQqxDunQW4JZ1ae0oDYPZBE597m58zvSUFkEocqBE2PTWxN1xm"
        secret_id = "EHlwg6Tt7nY5KdJXosLGgiRaiVXY06m4kpASLXBk9cuqiIVrTE5Li-abUZT1H7m0jWrTp-XBk88FI-YD"
    else:
        url = "https://api-m.paypal.com/v1/oauth2/token"
        cid = PAYPAL_CID
        secret_id = PAYPAL_SECRET_ID

    url = url
    payload='grant_type=client_credentials'
    cid = cid
    secret_id = secret_id

    headers = {
    'Content-Type': 'application/x-www-form-urlencoded'
    }

    response = requests.request("POST", url, auth=( cid , secret_id ),  headers=headers, data=payload).json()
    access_token = response['access_token']
    return access_token



def deactivate_subscription_plan( access_token, subscription_ids ):
    """
    Deactivating merchant subscription plan using the
    plan subscription ID.
    """
    
    access_token_bearer = f'Bearer { access_token }'
    url = f"https://api-m.sandbox.paypal.com/v1/billing/subscriptions/{ subscription_ids }/cancel"

    payload = json.dumps({
    "reason": "plan expired or unable to make payments."
    })

    headers = {
    'Content-Type': 'application/json',
    'Authorization': access_token_bearer
    }

    response = requests.request( "POST" , url, headers=headers, data=payload ).status_code
    response_data = response
    return response_data

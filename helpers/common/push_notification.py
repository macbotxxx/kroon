import requests
import json
from django.conf import settings


FCM_SERVER_KEY_KROON = settings.FCM_SERVER_KEY
FCM_SERVER_KEY_KIOSK = settings.KIOSK_FCM_SERVER_KEY
KIOSK_FCM_SERVER_KEY_TAB = settings.KIOSK_FCM_SERVER_KEY_TAB


def mobile_push_notification ( *args , **kwargs ):
    
    serverToken = None
    # FCM push-notifications
    device_id = kwargs.pop('device_id', None)
    title = kwargs.pop('title', None)
    body_message = kwargs.pop('body', None)
    platform = kwargs.pop('platform', None)
    device_type = kwargs.pop('device_type', None)

    # getting the user through the device id
 
    if platform == 'kroon':
        serverToken = FCM_SERVER_KEY_KROON
    elif platform == 'kiosk':
        # identifing the device type of the user
        if device_type == 'phone':
            serverToken = FCM_SERVER_KEY_KIOSK
        elif device_type == 'tab':
            serverToken = KIOSK_FCM_SERVER_KEY_TAB
        else:
            serverToken = FCM_SERVER_KEY_KIOSK
            
        
        
    deviceToken = device_id
    headers = {
            'Content-Type': 'application/json',
            'Authorization': 'key=' + serverToken,
        }
    body = {
            'notification': {
                            'title': title,
                            'body': body_message ,
                            'sound': 'default',
                            },
            'to':deviceToken,
            'priority': 'high',
            #   'data': dataPayLoad,
            }
    response = requests.post("https://fcm.googleapis.com/fcm/send",headers = headers, data=json.dumps(body))
                


import json
from django.contrib.auth import get_user_model
# import Django Packages
from django.core.mail import send_mail
from django.core import mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from kroon.users.models import User
import requests

# import celery
from config import celery_app
from celery import shared_task

# user model
User = get_user_model()

FCM_SERVER_KEY_KROON = settings.FCM_SERVER_KEY
FCM_SERVER_KEY_KIOSK = settings.KIOSK_FCM_SERVER_KEY
KIOSK_FCM_SERVER_KEY_TAB = settings.KIOSK_FCM_SERVER_KEY_TAB


@celery_app.task()
def mobile_push_notification ( *args , **kwargs ):

    serverToken = None
    # FCM push-notifications
    device_id = kwargs.pop('device_id', None)
    title = kwargs.pop('title', None)
    body_message = kwargs.pop('body_message', None)
    platform = kwargs.pop('platform', None)
    device_type = kwargs.pop('device_type', None)
    notification_type = kwargs.pop('notification_type', None)

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
    else:
        serverToken = FCM_SERVER_KEY_KIOSK
        # TODO: this section needs to be fixed
        #the general push notification which is meant to send 
        # a push notification to all clients
        
    deviceToken = device_id
    headers = {
            'Content-Type': 'application/json',
            'Authorization': 'key=' + serverToken,
        }
    
    # grouping the notification body
    if notification_type == "newsfeed":
        body = {
                    'notification':{
                        'title': title,
                        'body': body_message ,
                        'sound': 'default',
                        'link': 'https://kroonapp.xyz/notifications/api/v1/news-feed/kiosk/'
                    },
                    'to':deviceToken,
                    'priority': 'high',
                    'data': {
                        'link': 'https://kroonapp.xyz/notifications/api/v1/news-feed/kiosk/'
                    },
                }
    else:
        body = {
                'notification':{
                    'title': title,
                    'body': body_message ,
                    'sound': 'default',
                },
                'to':deviceToken,
                'priority': 'high',
                # 'data': {
                #     'link': 'http://www.mykroonapp.com'
                # },
                }
    requests.post("https://fcm.googleapis.com/fcm/send",headers = headers, data=json.dumps(body))
    return "Phone notification is pushed"
                


@celery_app.task()
def service_push_notification ( *args , **kwargs ):

    serverToken = None
    # FCM push-notifications
    body_message = kwargs.pop('body_message', None)

    users_qs = User.objects.select_related('country_of_residence','country_province','on_boarding_user','government_organization_name','government_organization_name').all()
    for i in users_qs:

        message = kwargs.pop('message', None)
        device_id = i.device_id
        title = "System Update"
        platform = 'kiosk'
        device_type = 'phone'

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
        else:
            serverToken = FCM_SERVER_KEY_KIOSK
            # TODO: this section needs to be fixed
            #the general push notification which is meant to send 
            # a push notification to all clients
            
        deviceToken = device_id
        headers = {
                'Content-Type': 'application/json',
                'Authorization': 'key=' + serverToken,
            }
        
        # grouping the notification body
        
        body = {
                'notification':{
                    'title': title,
                    'body': body_message['message'] ,
                    'sound': 'default',
                },
                'to':deviceToken,
                'priority': 'high',
                # 'data': {
                #     'link': 'http://www.mykroonapp.com'
                # },
                }
    
    requests.post("https://fcm.googleapis.com/fcm/send",headers = headers, data=json.dumps(body))
    return "Phone notification is pushed"
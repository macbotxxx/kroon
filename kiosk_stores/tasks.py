# import json
# from django.contrib.auth import get_user_model
# # import Django Packages
# from django.core.mail import send_mail
# from django.core import mail
# from django.template.loader import render_to_string
# from django.utils.html import strip_tags
# from django.conf import settings
# from kroon.users.models import User
# import requests

# # import celery
# from config import celery_app
# from celery.schedules import crontab
# from celery import shared_task

# # user model
# User = get_user_model()

# FCM_SERVER_KEY_KROON = settings.FCM_SERVER_KEY
# FCM_SERVER_KEY_KIOSK = settings.KIOSK_FCM_SERVER_KEY
# KIOSK_FCM_SERVER_KEY_TAB = settings.KIOSK_FCM_SERVER_KEY_TAB



# @celery_app.task( name = "expiry_products" )
# def expiry_products_notifications(*args , **kwargs):
#     pass



# celery_app.conf.beat_schedule = {
#     # Execute the cancelling of expired merchants sub every 1 minute
#     'expire-products-notification': {
#         'task': 'expiry_products',
#         'schedule': crontab(minute='*/1'),
#     },
# } 
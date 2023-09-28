from django.http.response import JsonResponse
from django.shortcuts import render
from django.contrib.auth.hashers import make_password, check_password
import requests
import json
# from firebase_admin.messaging import Message
# from fcm_django.models import FCMDevice

def passmike (request):
    pin = '1234s'
    hashed_pwd = make_password(pin)
    check = check_password(pin,hashed_pwd)  # returns True
    print(pin)
    print(hashed_pwd)
    print(check)


    return JsonResponse(hashed_pwd, safe=False)





from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status, serializers
from rest_framework.generics import ListAPIView, CreateAPIView , GenericAPIView
from django.conf import settings

from locations.models import Country,Country_Province
from helpers.common.security import KOKPermission
from .serializers import CountrySerializer, FireBase , Country_ProvinceSerializers
from kroon.users.models import User

import requests
import json

FCM_SERVER_KEY = settings.FCM_SERVER_KEY
KIOSK_FCM_SERVER_KEY = settings.KIOSK_FCM_SERVER_KEY


class CountryListView(APIView):
    permission_classes = [ AllowAny, KOKPermission ]

    def get(self, request, *args, **kwargs):
        qs = Country.objects.filter( accept_kroon = True )
        serializer = CountrySerializer(qs, many=True)
        return Response({'status':'success','message':'List of countries fetched successfully','data':serializer.data}, status=status.HTTP_202_ACCEPTED)


class KoiskCountryListView(APIView):
    permission_classes = [ AllowAny, KOKPermission ]

    def get(self, request, *args, **kwargs):
        qs = Country.objects.order_by('name')
        serializer = CountrySerializer(qs, many=True)
        return Response({'status':'success','message':'List of countries fetched successfully','data':serializer.data}, status=status.HTTP_202_ACCEPTED)
    

class CountryStates( ListAPIView  ):
    permission_classes = [ AllowAny, KOKPermission ]
    serializer_class = Country_ProvinceSerializers
    queryset = Country_Province.objects.all()

    def list (self, request , *args, **kwargs):
        qs = self.get_queryset().filter( country = kwargs.get('country_id') )
        serializer = self.get_serializer(qs, many = True)
        return Response(serializer.data)



class Notifications (CreateAPIView):
    permission_classes = [ AllowAny, KOKPermission ]
    serializer_class = FireBase

    def post (self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            device_id = serializer.validated_data.get('device_ID')

            serverToken = f'{KIOSK_FCM_SERVER_KEY}'
            deviceToken = f'{device_id}'
            headers = {
                    'Content-Type': 'application/json',
                    'Authorization': 'key=' + serverToken,
                }
            body = {
                    'notification': {
                                    'title': 'Sending push form python script',
                                    'body': 'New Message',
                                    'sound': 'default',
                                    },
                    'to':deviceToken,
                    'priority': 'high',
                    #   'data': dataPayLoad,
                    }
            response = requests.post("https://fcm.googleapis.com/fcm/send",headers = headers, data=json.dumps(body))
          
            return Response({'status':'success','message':'notifications is been pushed successfully','data':'null'}, status=status.HTTP_202_ACCEPTED)


class User_Country_Kroon_verification (APIView):
    
    def get (self, request, *args, **kwargs):
        user_country  =  request.user.country_of_residence
        checking_country_kroon = Country.objects.get(name=user_country)
        
        if checking_country_kroon.accept_kroon == True:
            return Response({'accept_kroon':True}, status=status.HTTP_202_ACCEPTED)
        else:
            return Response({'accept_kroon':False}, status=status.HTTP_401_UNAUTHORIZED)
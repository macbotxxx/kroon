import requests
import json
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status, serializers
from rest_framework.generics import CreateAPIView , GenericAPIView
from rest_framework.views import APIView
from django.conf import settings
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie, vary_on_headers

from helpers.common.security import KOKPermission
from locations.models import Country
from .serializers import Accoount_number_Serializer


PAYSTACK_SECRET_KEY = settings.PAYSTACK_SECRET_KEY
FLUTTERWAVE_SECRET_KEY = settings.FLUTTERWAVE_SECRET_KEY


class List_Of_Banks (APIView):

    permission_classes = [ IsAuthenticated, KOKPermission ]
    # Cache page for the requested url
 
    def get (self, request, *args, **kwargs):
        
        # shedule the user country 
        country = ['Nigeria']

        if not str(request.user.country_of_residence) in country: 
            # TO GET THE USERS DEFAULT BANK
            user_bank = Country.objects.get(name = request.user.country_of_residence)

            url = f"https://api.flutterwave.com/v3/banks/{user_bank.iso2}"

            payload = ""
            
            headers = {
            'Content-Type': 'application/json',
            'Authorization': f"Bearer {FLUTTERWAVE_SECRET_KEY}",
            }

        else:
            url = f"https://api.paystack.co/bank?currency={request.user.default_currency_id}"
            payload = ""

            headers = {
            'Content-Type': 'application/json',
            "Authorization": f"Bearer {PAYSTACK_SECRET_KEY}" 
            }

        
        response = requests.request("GET", url, headers=headers, data=payload)
        new = json.loads(response.text)
       
        response_data = new['data']
        return Response({'status':'success','message':'List of banks has been fetched successfully','data':response_data}, status=status.HTTP_201_CREATED)


class Account_Number_Verification (CreateAPIView):

    permission_classes = [ IsAuthenticated, KOKPermission ]
    serializer_class = Accoount_number_Serializer

    def post (self, request, *args, **kwargs):
        serializer = self.serializer_class (data=request.data)
        if serializer.is_valid():
            account_number = serializer.validated_data.get("account_number")
            bank_code = serializer.validated_data.get('bank_code')
           
            url = f"https://api.paystack.co/bank/resolve?account_number={account_number}&bank_code={bank_code}"
            payload = ""
            headers = {
            'Content-Type': 'application/json',
            "Authorization": f"Bearer sk_test_b5b16f074fc77ad997043a769f7f420e85ffc768" 
            }

            response = requests.request("GET", url, headers=headers, data=payload)
            new = json.loads(response.text)

            if new['status'] == True:
                response_data = new['data']
                status_res = "success"
                message = "Account number details fetched successfully"
                data = response_data
                status_code = status.HTTP_201_CREATED
            else:
                response_data = new
                status_res = "error"
                message = new['message']
                data = "null"
                status_code = status.HTTP_404_NOT_FOUND

            return Response({'status':status_res,'message':message,'data':data}, status=status_code)

        return Response(serializer.errors,  status=status.HTTP_400_BAD_REQUEST)
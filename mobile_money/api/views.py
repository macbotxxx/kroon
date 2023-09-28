import json
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from rest_framework.generics import ListAPIView , CreateAPIView, UpdateAPIView, GenericAPIView
from django.db.models import Q
from helpers.common.security import KOKPermission
from transactions.models import Transactions
from kroon.users.models import UserWrongPinValidate, User
from transactions.models import TransactionalPin, UserRequestToken
from django.contrib.auth.hashers import make_password, check_password
from rest_framework.views import APIView


from locations.models import Country
from kroon_token.models import TokenRate
from django.conf import settings
from rest_framework.response import Response

import string
import random
import requests
from django.conf import settings


from .serializers import MobileAccountDetails, MobileMoneyTopUpSerializer, NetworkProviderSerializer, MobileMoneyAccountSerializer, MobileMoneyTopUpSerializerForm

from mobile_money.models import NetworkProvider, MobileMoneyAccount, MobileMoneyTopUp

def transaction_ref():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=30))

FLUTTERWAVE_SECRET_KEY = settings.FLUTTERWAVE_SECRET_KEY



class NetworkProviderView (ListAPIView):
    permission_classes = [ IsAuthenticated, KOKPermission ]
    serializer_class = NetworkProviderSerializer

    def get (self, request, *args, **kwargs):
        country = ['Ghana', 'Uganda', 'Rwanda', 'Tanzania','Kenya']
        if not str(request.user.country_of_residence) in country:
            return Response({'status':'error', 'message':'Kroon mobile money is not allowed in your country'},  status=status.HTTP_400_BAD_REQUEST)

        try:
            network = NetworkProvider.objects.filter(country = request.user.country_of_residence)
        except NetworkProvider.DoesNotExist:
            return Response({'status':'error', 'message':'the current user country does not support mobile money services or the country is not inputted'},  status=status.HTTP_400_BAD_REQUEST)

        serializer = self.serializer_class(network, many=True)
        return Response({'status':'success', 'message':'list of mobile money network providers', 'data':serializer.data}, status=status.HTTP_200_OK)


class MobileMobileAccountView (CreateAPIView, ListAPIView):
    permission_classes = [ IsAuthenticated, KOKPermission ]
    serializer_class = MobileMoneyAccountSerializer
    serializers_details = MobileAccountDetails

    def get (self, request, *args, **kwargs):
        try:
            user_account = MobileMoneyAccount.objects.get(user=request.user)
            serializer = self.serializers_details(user_account)
            return Response({'status':'success', 'message':'User mobile money account fetched successfully','data':serializer.data}, status=status.HTTP_200_OK)
        except MobileMoneyAccount.DoesNotExist:
            return Response({'status':'error', 'message':'cant find your account or mobile money is not supported in your country.'},  status=status.HTTP_404_NOT_FOUND)


    def post(self, request, *args, **kwargs):

        country = ['Ghana', 'Uganda', 'Rwanda', 'Tanzania','Kenya']
        if not str(request.user.country_of_residence) in country:
            return Response({'status':'error', 'message':'Kroon mobile money is not allowed in your country,'},  status=status.HTTP_400_BAD_REQUEST)

        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user_account = MobileMoneyAccount.objects.filter(user=request.user)
            if user_account:
                return Response({'status':'error', 'message':'User mobile money account already exists'},  status=status.HTTP_400_BAD_REQUEST)

            serializer.save(user=request.user, currency = request.user.default_currency_id)
           
            # Updating the user details record 
            user_mobile_money_record = User.objects.get(id = request.user.id)
            user_mobile_money_record.mobile_money_details_submitted = True
            user_mobile_money_record.save()

            return Response({'status':'success','message':'Mobile money account is created succesfully', 'data':serializer.data}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors,  status=status.HTTP_400_BAD_REQUEST)



class DeleteMobileMoneyDetails(APIView):
    permission_classes = [ IsAuthenticated, KOKPermission ]

    def delete(self, request, *args, **kwargs):
        try:
            user_account = MobileMoneyAccount.objects.get(user=request.user)
        except MobileMoneyAccount.DoesNotExist:
            return Response({'status':'error','message':'user havent inputted his or her mobile money account',}, status=status.HTTP_404_NOT_FOUND)

        user_account.delete()

        # Updating the user details record 
        user_mobile_money_record = User.objects.get(id = request.user.id)
        user_mobile_money_record.mobile_money_details_submitted = False
        user_mobile_money_record.save()

        return Response({'status':'success', 'message':'user mobile money account deleted succesfully'}, status=status.HTTP_201_CREATED)



class MobileMoneyTopUpView(CreateAPIView):
    permission_classes = [ IsAuthenticated, KOKPermission ]
    serializer_class = MobileMoneyTopUpSerializerForm
    serializers_details = MobileMoneyTopUpSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            transactional_pin = serializer.validated_data.get('transactional_pin')
            amount = serializer.validated_data.get('amount')

            try:
                check_pin = TransactionalPin.objects.get(user= request.user)
            except TransactionalPin.DoesNotExist:
                return Response({'status':'error', 'message':'User havent inputed his or her transactional pin.'},status=status.HTTP_404_NOT_FOUND)

           
            pasd = check_pin.password
            verify_pin = check_password(transactional_pin,pasd)
            if not verify_pin:
                try:
                    # checking failed password twice
                    failed_pin = UserWrongPinValidate.objects.get(user=request.user)
                    if failed_pin:
                        if failed_pin.failed_password > 4:
                            # send OTP pin validation to the user 
                            update = UserWrongPinValidate.objects.get(user=request.user)
                            update.failed_password = failed_pin.failed_password
                            update.banned = True
                            update.save()
                           
                            return Response({'status':'error','message':'your transactional pin have been disabled, an opt message has been sent to reset your pin'},  status=status.HTTP_406_NOT_ACCEPTABLE)
                        else:
                            failed_pin.failed_password += 1
                            update = UserWrongPinValidate.objects.get(user=request.user)
                            update.failed_password = failed_pin.failed_password
                            update.save()
                            return Response({'status':'error','message':'Transactional pin is not valid'},  status=status.HTTP_406_NOT_ACCEPTABLE)
                except UserWrongPinValidate.DoesNotExist:
                    UserWrongPinValidate.objects.create(user=request.user)
                    return Response({'status':'error','message':'Transactional pin is not valid'},  status=status.HTTP_406_NOT_ACCEPTABLE)
            else:
                try:
                    UserWrongPinValidate.objects.get(user=request.user).delete()
                except UserWrongPinValidate.DoesNotExist:
                    pass

            # getting the users mobile money record
            try:
                user_record = MobileMoneyAccount.objects.get(user=request.user)
            except MobileMoneyAccount.DoesNotExist:
                return Response({'status':'error', 'message':'user havent inputed his or her mobile money account details'},  status=status.HTTP_404_NOT_FOUND)

            # transactional pin ends here 

            trans_ref = transaction_ref()

            country = str(request.user.country_of_residence).lower()
           
            url = f"https://api.flutterwave.com/v3/charges?type=mobile_money_{country}"
            
            payload = json.dumps({
            "amount": f"{amount}",
            "currency": f"{user_record.currency}",
            "email": f"{user_record.email}",
            "tx_ref": trans_ref,
            "phone_number": f"{user_record.phone_number}",
            "network": f"{user_record.network}"
            })
            headers = {
            'Authorization': f"Bearer {FLUTTERWAVE_SECRET_KEY}",
            'Content-Type': 'application/json'
            }

            response = requests.request("POST", url, headers=headers, data=payload)
            print(response.text)
            response_data = response.json()
            status_pay = response_data['status']
            if status_pay == "success":
                mobile_money_record = MobileMoneyTopUp.objects.create( user=request.user, amount = amount, currency = user_record.currency, email = user_record.email, transactional_ref =trans_ref, phone_number = user_record.phone_number, network = user_record.network, )

                Transactions.objects.create(user = request.user,transactional_id = trans_ref, amount = amount ,currency = user_record.currency, narration = f'kroon wallet topup using MOBILE MONEY',action ='KROON WALLET TOPUP', status = 'initiated')

                return Response({'status':'success','message':'Charge initialized successfully','data':self.serializers_details(mobile_money_record).data}, status=status.HTTP_201_CREATED)
            else:
                return Response({'status':'success','message':response_data,})

        
        return Response(serializer.errors,  status=status.HTTP_400_BAD_REQUEST)

            
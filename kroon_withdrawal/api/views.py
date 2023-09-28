
from datetime import timedelta, date
from decimal import Decimal
from helpers.common.security import KOKPermission
from kroon_token.models import TokenRate
from transactions.models import Transactions
from transactions.models import TransactionalPin
from kroon.users.models import User, UserWrongPinValidate, UserBankDetails, UserAddress
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status, serializers
from rest_framework.generics import ListAPIView , CreateAPIView, get_object_or_404
from django.contrib.auth.hashers import make_password, check_password
from django.core import mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from rest_framework.views import APIView


from django.conf import settings

import requests
import json
import random
import string

from .serializers import UserWithdrawal_RecordSerializer, Withdrawal_RecordDetailsSerializer

from kroon_withdrawal.models import Kroon_Withdrawal_Record, Recipient_Record

from mobile_money.models import MobileMoneyAccount



PAYSTACK_SECRET_KEY = settings.PAYSTACK_SECRET_KEY
FLUTTERWAVE_SECRET_KEY = settings.FLUTTERWAVE_SECRET_KEY



def transaction_ref():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=20))


def add_business_days(date_requested, estimated_delivery):
    to_date = date_requested
    while estimated_delivery:
       to_date += timedelta(1)
       if to_date.weekday() < 5: # i.e. is not saturday or sunday
           estimated_delivery -= 1
    return to_date
   

class FlutterWaveWithdrawal (CreateAPIView):
    
    permission_classes = [ IsAuthenticated, KOKPermission ]
    serializer_class = UserWithdrawal_RecordSerializer
    withdrawRecord = Withdrawal_RecordDetailsSerializer
    

    # def get(self, request, *args, **kwargs):
    #     user_record = Kroon_Withdrawal_Record.objects.filter(user=request.user)
    #     serializer = self.withdrawRecord(user_record, many=True)
    #     return Response({'status':'success', 'message':'User withdrawal record fetched', 'data':serializer.data},status=status.HTTP_200_OK)


    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        
        if serializer.is_valid():
            transactional_pin = serializer.validated_data.get('transactional_pin')
            amount = serializer.validated_data.get('amount')
            withdrawal_type = serializer.validated_data.get('withdrawal_type')
            amount_in_kroon = serializer.validated_data.get('amount_in_kroon')

            transac_ref = transaction_ref()
            # getting the users currency
            user_currency = request.user.default_currency_id
            user_token = User.objects.get(id = request.user.id)
           
            if  user_token.kroon_token < Decimal(amount_in_kroon) :
                return Response({'status':'error', 'message':'cant withdraw more than your initial balance.'},status=status.HTTP_404_NOT_FOUND)

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
            """
            this section holds the validation for withdrawal which determine which action
            should take place , either the local bank or mobile money, 
            this phase of mobile mobile is only valid for countries that support mobile money withdrawal
            such countries are Ghana, Uganda, Rwanda, Zambia.
            to determine which function and and action to call at the time , its been sedmented into two 
            local_bank and mobile_money are the choices.
            """
           
            if withdrawal_type == "local_bank":
                action = "Local Bank Withdrawal"
                
                try:
                    user_bank_details =  UserBankDetails.objects.get(user=request.user)
                except UserBankDetails.DoesNotExist:
                    return Response({'status':'error', 'message':'User havent inputed his or her bank details.'},status=status.HTTP_404_NOT_FOUND)

                user_address = UserAddress.objects.filter(user = request.user).first()
                if not user_address:
                    return Response({'status':'error', 'message':'Input your address so to enable this feature for you.'},status=status.HTTP_404_NOT_FOUND)

                user_address_record = str(user_address.street_or_flat_number) + " "  + str(user_address.street_name ) 
        
                # getting the users currency
                user_currency = request.user.default_currency_id
                user_token = User.objects.get(id = request.user.id)
                
                user_token.kroon_token -= Decimal(amount_in_kroon)
                user_token.save()

                # this feature is only for Nigerians
                # its is used to check for the users recipient record
                # if it exist it wont be registered again else it will be
                # registered for withdrawal process 
                if str(request.user.country_of_residence) == "Nigeria":
    
                    reqUrl = "https://api.paystack.co/transferrecipient"

                    headersList = {
                    "Authorization": f"Bearer {PAYSTACK_SECRET_KEY}",
                    "Content-Type": "application/json" 
                    }

                    payload = json.dumps({
                        "type": "nuban", 
                        "name": f"{user_bank_details.account_name}", 
                        "account_number": f"{user_bank_details.account_number}", 
                        "bank_code": f"{user_bank_details.bank_code}", 
                        "currency": f"{request.user.default_currency_id}"
                    })

                    response = requests.request("POST", reqUrl, data=payload,  headers=headersList)
                    response_data = json.loads(response.text)
                    print(response_data['status'])
                    if str(response_data['status']) == "False":
                        return Response({'status':'error', 'message':response_data['message'] + ' ' + ", kindly check your account details and try again."},status=status.HTTP_404_NOT_FOUND)

                    else:
                        user_bank_details.account_name = response_data['data']['details']['account_name']
                        user_bank_details.account_number = response_data['data']['details']['account_number']
                        user_bank_details.bank_name = response_data['data']['details']['bank_name']
                        user_bank_details.bank_code = response_data['data']['details']['bank_code']
                        user_bank_details.integration_id = response_data['data']['integration']
                        user_bank_details.recipient_code = response_data['data']['recipient_code']
                        user_bank_details.verified = True
                        user_bank_details.save()

                # working on day limit
                country = ['Ghana', 'Nigeria']
                if not str(request.user.country_of_residence) in country: 
                    estimated_delivery = 3
                else:
                    estimated_delivery = 2

                # if str(request.user.country_of_residence) == "Nigeria":
                #     amount = None
                
                # making the reference NONe , paystack will provide it when its set
                if str(request.user.country_of_residence) == "Nigeria":
                    reference = f'KROON_{transac_ref}'
                    recipient_code = user_bank_details.recipient_code
                else:
                    reference = f'KROON_{transac_ref}'
                    recipient_code = " "

                date_requested = date.today()
                estimated_delivery = add_business_days(date_requested, estimated_delivery)

                withdraw_record = Kroon_Withdrawal_Record.objects.create(
                    user = request.user,
                    full_name = request.user.name,
                    account_number = user_bank_details.account_number,
                    beneficiary_name = user_bank_details.account_name,
                    bank_name = user_bank_details.bank_name,
                    bank_code = user_bank_details.bank_code,
                    amount = Decimal(amount),
                    currency = request.user.default_currency_id,
                    reference = reference,
                    billing_full_name = request.user.name,
                    billing_email = request.user.email,
                    billing_mobile_number = request.user.contact_number,
                    billing_recipient_address = user_address_record,
                    action = action,
                    recipient_code = recipient_code,
                    status = 'pending',
                    withdrawal_type = withdrawal_type,
                    narration = "withdrawal performed by Kroon App",
                    date_requested = date_requested,
                    estimated_delivery = estimated_delivery,
                    amount_in_kroon = amount_in_kroon, 
                )

                # # Recipient Transactional Record History
                Transactions.objects.create(user = request.user , benefactor = request.user,amount = Decimal(amount_in_kroon),transactional_id = f'KROON_{transac_ref}', currency = 'KC',local_currency = user_currency,amount_in_localcurrency = amount, narration = f'Local Bank withdrawal has been queued to be initiated on {estimated_delivery} ',action = 'LOCAL BANK WITHDRAWAL', status = 'pending', debited_kroon_amount = Decimal(amount_in_kroon) , kroon_balance = user_token.kroon_token)

                return Response({'status':'success','message': 'Transfer has been queued', 'data': self.withdrawRecord(withdraw_record).data}, status=status.HTTP_201_CREATED)

            
                
            elif withdrawal_type == "mobile_money":
            
                country = ['Ghana', 'Uganda', 'Rwanda', 'Tanzania','Kenya']
                if not str(request.user.country_of_residence) in country:
                    return Response({'status':'error', 'message':'Kroon mobile money withdrawal is not allowed in your country,'},  status=status.HTTP_400_BAD_REQUEST)

                """
                validating the user account checking if the user has inputted his or her 
                mobile money details to the system and if not it will return an error message prompting the 
                user to go and register their mobile money account.
                """

                try:
                    user_bank_details =  MobileMoneyAccount.objects.get(user=request.user)
                except MobileMoneyAccount.DoesNotExist:
                    return Response({'status':'error', 'message':'User havent inputed his or her mobile money details for withdrawal.'},status=status.HTTP_404_NOT_FOUND)

                user_address = UserAddress.objects.filter(user = request.user).first()
                if not user_address:
                    return Response({'status':'error', 'message':'Input your address so to enable this feature for you.'},status=status.HTTP_404_NOT_FOUND)

                if str(request.user.country_of_residence) == "Ghana":
                    account_bank = user_bank_details.network

                elif str(request.user.country_of_residence) == "Kenya":
                    account_bank = user_bank_details.network

                else:
                    account_bank = "MPS"

                url = "https://api.flutterwave.com/v3/transfers"
                user_address_record = str(user_address.street_or_flat_number) + " "  + str(user_address.street_name )

                payload = json.dumps({
                "account_bank": f"{account_bank}",
                "account_number": f"{user_bank_details.phone_number}",
                "amount": f"{Decimal(amount)}",
                "narration": "Withdrawal to local banks using MOBILE MONEY",
                "currency": f"{request.user.default_currency_id}",
                "beneficiary_name": f"{request.user.name}",
                # checking for test accounts
                
                "reference": f"KROON_{transac_ref}",
                # "callback_url": "https://kroonapp.xyz/webhook/push-webhook/",
                
                "meta": {
                    "first_name": f"{request.user.first_name}",
                    "last_name": f"{request.user.last_name}",
                    "email": f"{request.user.email}",
                    "mobile_number": f"{user_bank_details.phone_number}",
                    "recipient_address": f"{user_address_record},{user_address.state},{user_address.city}",
                    "action": f"{'mobile_money'}"
                }
                })

                headers = {
                'Authorization': f'Bearer {FLUTTERWAVE_SECRET_KEY}',
                'Content-Type': 'application/json'
                }

                response = requests.request("POST", url, headers=headers, data=payload)

                response_data = response.json()
                print(response_data)
                status_pay = response_data['status']

    
                # return Response({'status':'error', 'message':response_data['message'], 'data':response_data['data']},  status=status.HTTP_400_BAD_REQUEST)

                if status_pay == "success":
                    country = ['Uganda', 'Rwanda', 'Tanzania']
                    if not str(request.user.country_of_residence) in country:
                        reference = response_data['data']['reference']
                        amount = response_data['data']['amount']
                        currency = response_data['data']['currency']
                        full_name = response_data['data']['meta']['first_name'] + " " + response_data['data']['meta']['last_name']
                        account_number = response_data['data']['account_number']
                        transaction_id = response_data['data']['id']
                        fee = response_data['data']['fee']
                        is_approved = response_data['data']['is_approved']
                        billing_email = response_data['data']['meta']['email']
                        billing_mobile_number = response_data['data']['meta']['mobile_number']
                        billing_recipient_address = response_data['data']['meta']['recipient_address']
                        bank_name = response_data['data']['bank_name']

                    else:
                        reference = response_data['data']['reference']
                        amount = response_data['data']['amount']
                        currency = response_data['data']['currency']
                        full_name = response_data['data']['meta'][0]['FirstName'] + " " + response_data['data']['meta'][0]['LastName']
                        account_number = response_data['data']['account_number']
                        transaction_id = response_data['data']['id']
                        fee = response_data['data']['fee']
                        is_approved = response_data['data']['is_approved']
                        billing_email = response_data['data']['meta'][0]['EmailAddress']
                        billing_mobile_number = response_data['data']['meta'][0]['MobileNumber']
                        billing_recipient_address = response_data['data']['meta'][0]['Address']
                        bank_name = response_data['data']['bank_name']


                    withdraw_record = Kroon_Withdrawal_Record.objects.create(
                        user = request.user,
                        full_name = full_name,
                        account_number = account_number,
                        transaction_id = transaction_id,
                        amount = amount,
                        fee = fee,
                        currency = currency,
                        # debit_currency = response_data['data']['debit_currency'],
                        reference = reference,
                        is_approved = is_approved,
                        status = "pending",
                        action = "Mobile Money Withdrawal",
                        billing_full_name = full_name,
                        billing_email = billing_email,
                        billing_mobile_number = billing_mobile_number,
                        billing_recipient_address = billing_recipient_address,
                        bank_name = bank_name,
                        withdrawal_type = withdrawal_type,
                        
                    )

                    # getting the users currency
                    user_currency = request.user.default_currency_id
                    user_token = User.objects.get(id = request.user.id)
                    
                    user_token.kroon_token -= Decimal(amount_in_kroon)
                    user_token.save()


                    # Recipient Transactional Record History
                    Transactions.objects.create(user = request.user , benefactor = request.user,amount = Decimal(amount_in_kroon),transactional_id = reference, currency = 'KC',local_currency = user_currency,amount_in_localcurrency = amount, narration = f'Mobile Money Withdrawal has been queued successfully ',action = 'MOBILE MONEY WITHDRAWAL', status = 'pending', debited_kroon_amount = Decimal(amount_in_kroon) , kroon_balance = user_token.kroon_token)

                    return Response({'status':'success','message': 'Transfer has been queued', 'data': self.withdrawRecord(withdraw_record).data}, status=status.HTTP_201_CREATED)

                else:
                    country = ['Uganda', 'Rwanda', 'Tanzania']
                    if not str(request.user.country_of_residence) in country:
                        reference = response_data['data']['reference']
                        amount = response_data['data']['amount']
                        currency = response_data['data']['currency']
                        full_name = response_data['data']['meta']['first_name'] + " " + response_data['data']['meta']['last_name']
                        account_number = response_data['data']['account_number']
                        transaction_id = response_data['data']['id']
                        fee = response_data['data']['fee']
                        is_approved = response_data['data']['is_approved']
                        billing_email = response_data['data']['meta']['email']
                        billing_mobile_number = response_data['data']['meta']['mobile_number']
                        billing_recipient_address = response_data['data']['meta']['recipient_address']
                        bank_name = response_data['data']['bank_name']

                    else:
                        reference = response_data['data']['reference']
                        amount = response_data['data']['amount']
                        currency = response_data['data']['currency']
                        full_name = response_data['data']['meta'][0]['FirstName'] + " " + response_data['data']['meta'][0]['LastName']
                        account_number = response_data['data']['account_number']
                        transaction_id = response_data['data']['id']
                        fee = response_data['data']['fee']
                        is_approved = response_data['data']['is_approved']
                        billing_email = response_data['data']['meta'][0]['EmailAddress']
                        billing_mobile_number = response_data['data']['meta'][0]['MobileNumber']
                        billing_recipient_address = response_data['data']['meta'][0]['Address']
                        bank_name = response_data['data']['bank_name']


                    withdraw_record = Kroon_Withdrawal_Record.objects.create(
                        user = request.user,
                        full_name = full_name,
                        account_number = account_number,
                        transaction_id = transaction_id,
                        amount = amount,
                        fee = fee,
                        currency = currency,
                        # debit_currency = response_data['data']['debit_currency'],
                        reference = reference,
                        is_approved = is_approved,
                        status = "failed",
                        action = "Mobile Money Withdrawal",
                        billing_full_name = full_name,
                        billing_email = billing_email,
                        billing_mobile_number = billing_mobile_number,
                        billing_recipient_address = billing_recipient_address,
                        bank_name = bank_name,
                        withdrawal_type = withdrawal_type,

                    )

                    # Recipient Transactional Record History
                    Transactions.objects.create(user = request.user , benefactor = request.user,amount = Decimal(amount_in_kroon),transactional_id = reference, currency = 'KC',local_currency = user_currency,amount_in_localcurrency = amount, narration = response_data['message'],action = 'MOBILE MONEY WITHDRAWAL', status = 'failed' , kroon_balance = request.user.kroon_token)

                    return Response({'status':'error','message':response_data['message'],'data': self.withdrawRecord(withdraw_record).data}, status=status.HTTP_400_BAD_REQUEST)
                
                
            else:
                return Response({'status':'error', 'message':'Kroon mobile money withdrawal is not allowed in your country,'},  status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors,  status=status.HTTP_400_BAD_REQUEST)
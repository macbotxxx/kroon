import string
import random
import requests
import json
import os
import uuid
from binascii import hexlify
from datetime import timedelta

from decimal import Decimal
from yaml import serialize
from helpers.common.security import KOKPermission
from helpers.common.push_notification import mobile_push_notification
from helpers.common.trasaction_fees import Transactional_Percentage

from kroon.users.models import User, UserWrongPinValidate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authentication import SessionAuthentication, BasicAuthentication 
from rest_framework import status, serializers
from rest_framework.generics import ListAPIView , CreateAPIView, UpdateAPIView, GenericAPIView
from django.db.models import Q

from django.contrib.auth.hashers import make_password, check_password

# django email settings
from django.core import mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
import threading

# from drf_yasg import openapi
# from drf_yasg.utils import swagger_auto_schema
# from twilio.rest import Client

from .serializers import TransactionSerializer, UserTokenTransferDetails, WalletSerializer, TokenConvertionSerializer, TransferTokenSerializer, TransferTokenHistorySerializer, KroonTokenRequestSerializer, PayTokenRequestSerializer, KroonRequestDetails, TransactionPasswordsSerializer,ChangerTransactionPinSerializer, UserKroonTransferSerializer, DeclineTokenRequestSerializer, AcceptTokenRequestSerializer, TransferTokenDetails, StatementOfAccountSerilizers,  CancelFastCheckoutRequestSerializer , Transactional_Pin_Serializer


from transactions.models import Transactions, KroonTokenTransfer, KroonTokenRequest, TransactionalPin, UserRequestToken

from locations.models import Country
from statement_of_account.models import Mask_Statement_Of_Account
from generate_pin.models import Generate_Pin
from transactions.tasks import cross_border_currency_convertion

from kroon_token.models import TokenRate
from django.conf import settings



FLUTTERWAVE_SECRET_KEY = settings.FLUTTERWAVE_SECRET_KEY
FCM_SERVER_KEY = settings.FCM_SERVER_KEY

# masking id 
def _createId():
    return uuid.uuid4()


class EmailThreading (threading.Thread):
    def __init__ (self, send_mail):
        self.send_mail = send_mail
        threading.Thread.__init__(self)

    def run(self):
        self.send_mail()



def transaction_ref():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=30))




class TransactionView(APIView):
    """
    transaction view set
    """
    permission_classes = [ IsAuthenticated, KOKPermission ]
    serializer_class = None

    # @swagger_auto_schema(operation_description="to get all transactions , note the will still be a change to this because it is a testing api view for now.")

    def get (self, request, *args, **kwargs):
        total_c = 0
        total_d = 0
        # getting all user transactional history
        qs = Transactions.objects.select_related("user", "benefactor", "recipient").filter(user = self.request.user)[0:20]

        # getting the total amount for credited
        credit = Transactions.objects.select_related("user",  "benefactor", "recipient").filter(user = request.user, recipient = request.user, currency = "KC", status = "successful")

        for i in credit:
            total_c += i.credited_kroon_amount
           
        total_credit = Decimal( total_c )
       
        # getting the total amount debitted
        debit = Transactions.objects.filter(user = request.user, benefactor = request.user, currency = "KC", status = "successful")
        for i in debit:
            total_d += i.debited_kroon_amount
        total_debit = Decimal( total_d ) 
    
        all_transactional_history = TransactionSerializer(qs, many=True)
        
        return Response({'status':'success','message':'list of transactions which include transfer token, request kroon token','total_credit':total_credit,'total_debit':total_debit,'data':all_transactional_history.data,}, status=status.HTTP_200_OK)




class CreditTransactionDetails(APIView):
    """
    transaction view set
    """
    permission_classes = (IsAuthenticated, )

    # @swagger_auto_schema(operation_description="to get all transactions , note the will still be a change to this because it is a testing api view for now.")

    def get (self, request, *args, **kwargs):
        # getting all user credited transactional history
        qs = Transactions.objects.select_related("user",  "benefactor", "recipient").filter(user= request.user, recipient = request.user, currency = "KC", status = "successful")
        credit_transactions = TransactionSerializer(qs, many=True)
        
        return Response({'status':'success','message':'list of credited kroon token transactions ','data':credit_transactions.data,}, status=status.HTTP_200_OK)



class DebitTransactionDetails(APIView):
    """
    transaction view set
    """
    permission_classes = (IsAuthenticated, )

    # @swagger_auto_schema(operation_description="to get all transactions , note the will still be a change to this because it is a testing api view for now.")

    def get (self, request, *args, **kwargs):
        # getting all user debited transactional history
        qs = Transactions.objects.select_related("user",  "benefactor", "recipient").filter(user= request.user, benefactor = request.user , currency = "KC", status = "successful")
        debit_transactions = TransactionSerializer(qs, many=True)
        
        return Response({'status':'success','message':'list of all debit kroon token transactions ','data':debit_transactions.data,}, status=status.HTTP_200_OK)


class WalletIDView (ListAPIView):
    permission_classes = [ IsAuthenticated, KOKPermission ]
    serializer_class = WalletSerializer

    def get (self, request, *args, **kwargs):
        wallet_id = kwargs.get('wallet_id')
        if not wallet_id:
            return Response({'status':'error', 'message':'wallet id cant be blank or mobile number cant be blank'},  status=status.HTTP_400_BAD_REQUEST)
        try:
            wallets = User.objects.get(Q(wallet_id = wallet_id) | Q(contact_number = wallet_id))
        except User.DoesNotExist:
            return Response({'status':'error', 'message':'wallet id or mobile number does not exists'},  status=status.HTTP_400_BAD_REQUEST)

        user_wallet =  User.objects.get(Q(wallet_id = wallet_id) | Q(contact_number = wallet_id))
        serializer = WalletSerializer(user_wallet)
        return Response({'status':'success','message':'wallet id information fetch successfully.','data':serializer.data}, status=status.HTTP_202_ACCEPTED)



class TokenTransfer (CreateAPIView, ListAPIView):

    permission_classes = [ IsAuthenticated, KOKPermission ]
    serializer_class = TransferTokenSerializer
    serializer_details = TransferTokenDetails

    def get (self, request, *args, **kwargs):
        user_token_record = KroonTokenTransfer.objects.filter(Q(sender= request.user) | Q(recipient= request.user))
        serializer = self.serializer_details(user_token_record, many=True)
        return Response({'status':'success', 'message':'list of users kroon transfer', 'data':serializer.data}, status=status.HTTP_200_OK)
      
    def post(self, request, *args, **kwargs):
        serializer = TransferTokenSerializer(data=request.data)
        if serializer.is_valid():
            amount = serializer.data.get('kroon_token_ammount') 
            wallet_id = serializer.data.get('wallet_id')
            transaction_pin = serializer.data.get('transaction_pin')

            # validating transaction pin.........................................
            try:
                check_pin = TransactionalPin.objects.get(user= request.user)
            except TransactionalPin.DoesNotExist:
                return Response({'status':'error', 'message':'User havent inputed his or her transactional pin.'},status=status.HTTP_404_NOT_FOUND)
            # cross border transfer 
            try:
                recipient_user = User.objects.get(Q(wallet_id= wallet_id) | Q(contact_number= wallet_id))
            except User.DoesNotExist:
                return Response({'status':'error', 'message':'wallet id does not exists'},  status=status.HTTP_404_NOT_FOUND) 

            sender = User.objects.get(id = request.user.id )

            # if recipient_user.country_of_residence != sender.country_of_residence:
            #     pass
                # converted_amount = cross_border_currency_convertion(
                #     sender_currency = sender.default_currency_id,
                #     reciepent_currency = recipient_user.default_currency_id,
                #     amount = amount
                # )
                
                # return Response({'status':converted_amount, 'message':'international kroon transaction is not allowed at the moment.'},  status=status.HTTP_404_NOT_FOUND) 

            if recipient_user.wallet_id == request.user.wallet_id:
                return Response({'status':'error', 'message':'you cant make a kroon transfer to the same user'},  status=status.HTTP_404_NOT_FOUND) 

            # conv_amount = converted_amount
            pasd = check_pin.password
            verify_pin = check_password(transaction_pin,pasd)

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
            # validating transaction pin end here .............................................

            # validate and check if wallet address is valid
            

            if Decimal(amount) > sender.kroon_token:
                return Response({'status':'error', 'message':'insufficent balance, cant proceed'},  status=status.HTTP_404_NOT_FOUND)
            else:
                sender.kroon_token -=  Decimal(amount) 
                sender.save()
                reciever = User.objects.get(Q(wallet_id= wallet_id) | Q(contact_number= wallet_id))
                kroon_token = round(reciever.kroon_token)

                # subtracting the kroon_token percentage 
                amount_percentage = Transactional_Percentage()
                final_amount = amount_percentage.kroon_transfer_percentage(request, amount = amount)
                
                reciever.kroon_token += Decimal(final_amount)
                reciever.save() 

                # save transaction history
                trasac_ref = f"eTranc_{transaction_ref()}"

                # Benefactor Transactional Record History
                Transactions.objects.create(user = request.user, benefactor = request.user, recipient = reciever,amount = amount,transactional_id = trasac_ref, currency = 'KC', narration = f' Kroon Token sent from {sender.name} TO {reciever.name}',action = 'TOKEN TRANSFER', status = 'successful', debited_kroon_amount = amount, kroon_balance = sender.kroon_token )

                # Recipient Transactional Record History
                Transactions.objects.create(user = reciever , benefactor = request.user, recipient = reciever,amount = amount,transactional_id = trasac_ref, currency = 'KC', narration = f' Kroon Token sent from {sender.name} TO {reciever.name}',action = 'TOKEN TRANSFER', status = 'successful', credited_kroon_amount = final_amount , kroon_balance = reciever.kroon_token)

                transferHistory = KroonTokenTransfer()
                transferHistory.sender = request.user
                transferHistory.recipient = reciever
                transferHistory.transactional_id = trasac_ref
                transferHistory.kroon_token = Decimal(amount)
                transferHistory.status = True
                transferHistory.save()


                # TODO:push notification to the user
                platform = "kroon"
                device_id = reciever.device_id
                title = "KROON TOKEN TRANSFER"
                body_message = f"Hey {reciever.name}, a kroon token was transfered to you from a kroon user, enjoy a free kroon token transfer without limitation and with zero charges #KroonMan"
                mobile_push_notification( device_id = device_id , title = title, body_message = body_message , platform = platform)
                # push notification ends here 

                # FCM push-notifications
     
                #  sending email to the customer alerting him of the succesful transfer 
                subject = 'Kroon Token Transfer Was Successful'
                html_message = render_to_string(
                    'emails/token_transfer.html',
                    {
                    'sender': request.user,
                    'sender_wallet': request.user.wallet_id,
                    'amount':amount,
                    'receiver':reciever,
                    'transaction':transferHistory,
                    'transaction_ref':trasac_ref,
                    } 
                )
                plain_message = strip_tags(html_message)
                from_email = f"{settings.EMAIL_HOST_USER}" 
                to = request.user.email
                mail.send_mail(subject, plain_message, from_email, [to], html_message = html_message)

                #  sending email to the customer alerting him of the succesful sent to his account 
                subject = 'Kroon Token Transfer Was Successful'
                html_message = render_to_string(
                    'emails/token_transfer.html',
                    {
                    'action':'reciever',
                    'sender': request.user,
                    'sender_wallet': request.user.wallet_id,
                    'amount':final_amount,
                    'receiver':reciever,
                    'transaction':transferHistory,
                    'transaction_ref':trasac_ref,
                    } 
                )
                plain_message = strip_tags(html_message)
                from_email = f"{settings.EMAIL_HOST_USER}" 
                to = reciever.email
                mail.send_mail(subject, plain_message, from_email, [to], html_message = html_message)
                
                return Response({'status': 'success','message':'Token transfer completed successfully','data':self.serializer_details(transferHistory).data},  status=status.HTTP_200_OK)

        return Response(serializer.errors,  status=status.HTTP_400_BAD_REQUEST)



class Open_TokenRequest (CreateAPIView, ListAPIView):

    permission_classes = [ IsAuthenticated, KOKPermission ]
    serializer_class = KroonTokenRequestSerializer
    serializer_details = KroonRequestDetails

    def get (self, request, *args, **kwargs):
        # getting all user transactional history
        all_token_transfer = KroonTokenRequest.objects.filter(Q(sender= request.user) | Q(recipient= request.user))
        all_token_request_history = KroonRequestDetails(all_token_transfer, many=True)
        return Response({'status':'success','message':'List of kroon token request' , 'data':all_token_request_history.data}, status=status.HTTP_200_OK)

    def post (self, request, *args, **kwargs):
        serializer = KroonTokenRequestSerializer(data=request.data)
        if serializer.is_valid():
            kroon_token = serializer.data.get('amount_in_kroon_token')
            request_user = request.user
            request_user_wallet_id  = request.user.wallet_id
            user_token = request.user.kroon_token


            # creating token request transaction
            transaction_id = f"KROON_{transaction_ref()}"
         
            # Benefactor Transactional Record History
            Transactions.objects.create(user = request.user,  recipient = request_user,amount = kroon_token,transactional_id = transaction_id, currency = 'KC', narration = f'{request.user.name} requested for a {kroon_token} kroon token ',action = 'OPEN KROON REQUEST', status = 'pending', kroon_balance = user_token )


            tokenRequest = KroonTokenRequest()
            tokenRequest.recipient = request_user
            tokenRequest.amount_in_kroon_token = Decimal (kroon_token )
            tokenRequest.transactional_id = transaction_id
            tokenRequest.wallet_id = request_user_wallet_id
            tokenRequest.save()

            return Response({'status':'success', 'message':'kroon Token has been generated successfully.', 'data':self.serializer_details(tokenRequest).data},  status=status.HTTP_201_CREATED)

        return Response(serializer.errors,  status=status.HTTP_400_BAD_REQUEST)



class Open_TokenRequest_Payment (CreateAPIView):

    permission_classes = [ IsAuthenticated, KOKPermission ]
    serializer_class = PayTokenRequestSerializer
    serializer_details = KroonRequestDetails

    def post(self, request, *args, **kwargs):
        serializer = PayTokenRequestSerializer(data=request.data)
        if serializer.is_valid():
            amount_in_kroon_token = serializer.data.get('kroon_token_amount')
            wallet_id = serializer.data.get('wallet_id')
            transactional_id = serializer.data.get('transactional_id')
            transactional_pin = serializer.data.get('transactional_pin')

            user_check = User.objects.get(wallet_id=wallet_id)
            sender_user = User.objects.get(id = request.user.id)
            
            # test = KroonTokenRequest.objects.filter(wallet_id = wallet_id,transactional_id = transactional_id)
            # for i in test:
            #     if i.status == 'successful':
            #         msg = {'error': 'Payment is already settled.', }
            #         return Response({'status':'failed','message':msg,},  status=status.HTTP_404_NOT_FOUND)
            try:
                recipient_user = User.objects.get(wallet_id=wallet_id)
                transaction_id = KroonTokenRequest.objects.get(transactional_id = transactional_id, status = 'pending')
            except User.DoesNotExist:
                return Response({'status':'error','message':'Wallet ID does not exists',},  status=status.HTTP_404_NOT_FOUND)

            except KroonTokenRequest.DoesNotExist:
                return Response({'status':'error','message':'Transactonal ID does not exists',},  status=status.HTTP_404_NOT_FOUND)

            if request.user.country_of_residence != recipient_user.country_of_residence:
                return Response({'status':'error', 'message':'international kroon transaction is not allowed at the moment.'},  status=status.HTTP_404_NOT_FOUND) 

            if user_check.id == request.user.id:
                return Response({'status':'error','message':'Scan to Pay cant be performed by the same token request user',},  status=status.HTTP_404_NOT_FOUND)

            if Decimal(amount_in_kroon_token) > sender_user.kroon_token:
                return Response({'status':'error','message':'Insufficent balance , transaction can not be completed'},  status=status.HTTP_404_NOT_FOUND)

            # if transaction_id.amount_in_kroon_token != amount_in_kroon_token:
            #     msg = {'error': 'Input the same amount with the token request.', }
            #     return Response({'status':'failed','message':msg,},  status=status.HTTP_404_NOT_FOUND)

            # validations end here 

            # checking and verifying transaction pin starts here 
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

            sender_user.kroon_token -= Decimal(amount_in_kroon_token)
            sender_user.save()   
            transaction_num = transaction_id.transactional_id    
           
            user_check.kroon_token += Decimal(amount_in_kroon_token)
            user_check.save()
            
        
            request_user_history = KroonTokenRequest()
            request_user_history.recipient = user_check
            request_user_history.sender = sender_user
            request_user_history.transactional_id = transaction_num
            request_user_history.amount_in_kroon_token = Decimal(amount_in_kroon_token)
            request_user_history.wallet_id = user_check.wallet_id
            request_user_history.status = 'successful'
            request_user_history.save()

            # FCM push-notifications
            serverToken = f'{FCM_SERVER_KEY}'
            deviceToken = f'{user_check.device_id}'
            headers = {
                    'Content-Type': 'application/json',
                    'Authorization': 'key=' + serverToken,
                }
            body = {
                    'notification': {
                                    'title': 'OPEN KROON TOKEN TRANSFER',
                                    'body': f'#{sender_user} responded to your open kroon token request, refer kroon to your friends and stand a chance to win weekend kroon giveaway from #KroonMan' ,
                                    'sound': 'default',
                                    },
                    'to':deviceToken,
                    'priority': 'high',
                    #   'data': dataPayLoad,
                    }
            response = requests.post("https://fcm.googleapis.com/fcm/send",headers = headers, data=json.dumps(body))
           
         
            # Benefactor Transactional Record History
            Transactions.objects.create(user = request.user, benefactor = request.user, recipient = user_check,amount = amount_in_kroon_token,transactional_id = transaction_num, currency = 'KC', narration = f'QrCod Token Request Paid By {sender_user} TO {user_check} was successfully',action = 'OPEN KROON REQUEST', status = 'successful', debited_kroon_amount = amount_in_kroon_token, kroon_balance = sender_user.kroon_token )

            # Recipient Transactional Record History
            Transactions.objects.create(user = user_check , benefactor = request.user, recipient = user_check,amount = amount_in_kroon_token,transactional_id = transaction_num, currency = 'KC', narration = f'QrCod Token Request Paid By {sender_user} TO {user_check} was successfully',action = 'OPEN KROON REQUEST', status = 'successful', credited_kroon_amount = amount_in_kroon_token , kroon_balance = user_check.kroon_token)

            return Response({'status':'success','message':'Token transfer completed successfully','data':self.serializer_details(request_user_history).data },  status=status.HTTP_200_OK)

                        
        return Response(serializer.errors,  status=status.HTTP_400_BAD_REQUEST)




class TransactionPin (CreateAPIView):

    permission_classes = [ IsAuthenticated, KOKPermission ]
    serializer_class = TransactionPasswordsSerializer
    
    def post (self, request, *args, **kwargs):
        serializer = TransactionPasswordsSerializer(data=request.data)
        if serializer.is_valid():
            pin = serializer.data.get('pin')
            pin_confirm = serializer.data.get('pin_confirm')
            # validating password 
            if pin != pin_confirm:
                return Response({'status':'error', 'message':'transactional pin does not match.'},  status=status.HTTP_404_NOT_FOUND)
            # hashing the above inputed password
            hashed_pwd = make_password(pin_confirm,salt=None, hasher='default')
            user_pass = TransactionalPin.objects.filter(user =request.user).delete()
            # storing hashed password
            check_userPWD = TransactionalPin.objects.filter(user= request.user)
            for i in check_userPWD:
                if i.user:
                    return Response({'status':'error', 'message':'user already has a transaction pin'},  status=status.HTTP_404_NOT_FOUND)

            transaction_pin = TransactionalPin()
            transaction_pin.user = request.user
            transaction_pin.password = hashed_pwd
            transaction_pin.save()

            return Response({'status':'success','message':'transactional pin is been created successfully', }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors,  status=status.HTTP_400_BAD_REQUEST)



class ChangeTransactionPin (CreateAPIView):

    permission_classes = [ IsAuthenticated, KOKPermission ]
    serializer_class =ChangerTransactionPinSerializer

    def post (self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            old_pin = serializer.data.get('old_pin')
            new_pin = serializer.data.get('new_pin')
            new_pin2 = serializer.data.get('new_pin2')

            try:
                TransactionalPin.objects.get(user= request.user)   
            except TransactionalPin.DoesNotExist:
                return Response({'status':'error', 'message':'User havent inputed his or her transactional pin.'},status=status.HTTP_404_NOT_FOUND)

            check_pin = TransactionalPin.objects.get(user= request.user)
            pasd = check_pin.password
            verify_pin = check_password(old_pin,pasd)
            if not verify_pin:
                return Response({'status':'error','message':'Transactional pin is invalid or incorrect', }, status=status.HTTP_404_NOT_FOUND)

            # validating password 
            if new_pin != new_pin2:
                return Response({'status':'error', 'message':'transactional pin does not match'},  status=status.HTTP_404_NOT_FOUND)

            # hashing the above inputed password
            hashed_pwd = make_password(new_pin,salt=None, hasher='default')
            # delete the user transactional pin account
            TransactionalPin.objects.get(user= request.user).delete()
            TransactionalPin.objects.create(user= request.user, password = hashed_pwd)
            
            return Response({'status':'success','message':'transactional pin has been updated successfully', }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors,  status=status.HTTP_400_BAD_REQUEST)
        



class PushNotification (APIView):
    """
    this is for testing purposes only
    """
    permission_classes = (AllowAny,)
    def get(self, request, *args, **kwargs):
         # Find your Account SID and Auth Token at twilio.com/console
        # and set the environment variables. See http://twil.io/secure
        account_sid = "AC1e165b1a83552a5bdd278abcef7c392e"
        auth_token = "3158cb03bcd6f80e900567e4466f731f"
        client = Client(account_sid, auth_token)

        message = client.messages \
                        .create(
                            body="Join Earth's mightiest heroes. Like Kevin Bacon.",
                            from_='+18455793930',
                            to='+23407067679537'
                        )



 
class UserKroonRequestView (CreateAPIView, ListAPIView):

    permission_classes = [ IsAuthenticated, KOKPermission ]
    serializer_class = UserKroonTransferSerializer
    serializer_details = UserTokenTransferDetails

    def get (self, request, *args, **kwargs):
        # getting the sender history
        # user_kroon_sender = UserRequestToken.objects.select_related("recipient", "sender").filter(Q(sender = request.user) | Q(recipient = request.user), status = "pending")
        user_kroon_sender = UserRequestToken.objects.select_related( "sender","recipient").filter(sender = request.user, status = "pending")
        serializer = self.serializer_details(user_kroon_sender, many=True)
       
        return Response({'status':'success','message':'list of all kroon request and transfer','data':serializer.data}, status=status.HTTP_202_ACCEPTED)

    def post (self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            wallet_id = serializer.validated_data.get('wallet_id')
            amount_in_kroon_token = serializer.validated_data.get('amount_in_kroon_token')
            request_pin = serializer.data.get('request_pin')

            # getting sender info using wallet id 
            transac_ref = f"KROON_{transaction_ref()}"
            try:
                sender = User.objects.get(Q(wallet_id= wallet_id) | Q(contact_number= wallet_id))
            except User.DoesNotExist:
                return Response({'status': 'error', 'message': 'Invalid wallet id or mobile number, kindly check your input'},  status=status.HTTP_404_NOT_FOUND)

            # verifying the generated pin number
            try:
                verifying_request_pin = Generate_Pin.objects.get(user = sender.id , pin = request_pin)
            except Generate_Pin.DoesNotExist:
                return Response({'status': 'error', 'message': 'Invalid request pin, kindly check your input'},  status=status.HTTP_404_NOT_FOUND)
            
            verifying_request_pin.delete()
            
            sender_info = User.objects.get( id=request.user.id )

            if wallet_id == sender_info.wallet_id:
                msg = {'warning': 'kroon token request cant be sent to the same user requesting.', }
                return Response({'status':'error','message':msg},  status=status.HTTP_404_NOT_FOUND)

            if wallet_id == sender_info.contact_number:
                msg = {'warning': 'kroon token request cant be sent to the same user requesting.', }
                return Response({'status':'error','message':msg},  status=status.HTTP_404_NOT_FOUND)

            if request.user.country_of_residence != sender.country_of_residence:
                return Response({'status':'error', 'message':'international kroon transaction is not allowed at the moment.'},  status=status.HTTP_404_NOT_FOUND) 

            user_data = UserRequestToken.objects.create(
                wallet_id = wallet_id,
                transactional_id = transac_ref, 
                sender = sender, 
                amount_in_kroon_token = Decimal(amount_in_kroon_token),
                recipient = request.user
                )

           

            # FCM push-notifications
            serverToken = f'{FCM_SERVER_KEY}'
            deviceToken = f'{sender.device_id}'
            headers = {
                    'Content-Type': 'application/json',
                    'Authorization': 'key=' + serverToken,
                }
            body = {
                    'notification': {
                                    'title': 'KROON TOKEN REQUEST',
                                    'body': f'#{request.user} request for a kroon token transfer , kroon token request helps in paying bills with with zero worries #KroonMan' ,
                                    'sound': 'default',
                                    },
                    'to':deviceToken,
                    'priority': 'high',
                    #   'data': dataPayLoad,
                    }
            response = requests.post("https://fcm.googleapis.com/fcm/send",headers = headers, data=json.dumps(body))

            # Benefactor Transactional Record History
            Transactions.objects.create(user = sender, benefactor = sender, recipient = request.user,amount = amount_in_kroon_token,transactional_id = transac_ref, currency = 'KC', narration = f'{request.user.name} requests a kroon token from  {sender.name}',action = 'KROON REQUEST', status = 'pending',  kroon_balance = sender.kroon_token )

            # Recipient Transactional Record History
            Transactions.objects.create(user = request.user , benefactor = sender, recipient = request.user,amount = amount_in_kroon_token,transactional_id = transac_ref, currency = 'KC', narration = f'{request.user.name} requests a kroon token from  {sender.name}',action =  'KROON REQUEST', status = 'pending', kroon_balance = request.user.kroon_token)

            return Response({'status':'success','message':'customers kroon token request is completed','data':self.serializer_details(user_data).data},  status=status.HTTP_201_CREATED)

        return Response(serializer.errors,  status=status.HTTP_400_BAD_REQUEST)


class DeclineTokenRequest (CreateAPIView):
    permission_classes = [ IsAuthenticated, KOKPermission ]
    serializer_class = DeclineTokenRequestSerializer
    serializer_details = UserTokenTransferDetails

    def post (self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            transactional_id = serializer.validated_data.get('transactional_id')
            declined_request = UserRequestToken.objects.get(transactional_id = transactional_id)
            # checking if transaction was decliend
            if declined_request.status == 'declined':
                return Response({'status':'error','message':'token request is already been declined by a user.'},  status=status.HTTP_404_NOT_FOUND)

            declined_request.status = 'declined'
            declined_request.save()

            recipient = User.objects.get(id = declined_request.recipient.id)

            # FCM push-notifications
            serverToken = f'{FCM_SERVER_KEY}'
            deviceToken = f'{recipient.device_id}'
            headers = {
                    'Content-Type': 'application/json',
                    'Authorization': 'key=' + serverToken,
                }
            body = {
                    'notification': {
                                    'title': 'KROON TOKEN REQUEST',
                                    'body': f'#{request.user} declined your kroon token request , kroon token request helps in paying bills with with zero worries #KroonMan' ,
                                    'sound': 'default',
                                    },
                    'to':deviceToken,
                    'priority': 'high',
                    #   'data': dataPayLoad,
                    }
            response = requests.post("https://fcm.googleapis.com/fcm/send",headers = headers, data=json.dumps(body))

            # Benefactor Transactional Record History
            Transactions.objects.create(user = declined_request.sender , benefactor = declined_request.sender, recipient = declined_request.recipient,amount = declined_request.amount_in_kroon_token,transactional_id = declined_request.transactional_id, currency = 'KC', narration = f'{declined_request.sender} declined {declined_request.recipient} kroon request', status = 'declined', kroon_balance = request.user.kroon_token, action = 'KROON REQUEST')

            # Recipient Transactional Record History
            Transactions.objects.create(user = declined_request.recipient , benefactor = declined_request.sender, recipient = declined_request.recipient,amount = declined_request.amount_in_kroon_token,transactional_id = declined_request.transactional_id, currency = 'KC', narration = f'{declined_request.sender} declined {declined_request.recipient} kroon request', status = 'declined', kroon_balance = recipient.kroon_token,action = 'KROON REQUEST')

            return Response({'status':'success','message':'Kroon request is declined','data':self.serializer_details(declined_request).data},  status=status.HTTP_201_CREATED)

        return Response(serializer.errors,  status=status.HTTP_400_BAD_REQUEST)


class AcceptTokenRequest (CreateAPIView):
    permission_classes = [ IsAuthenticated, KOKPermission ]
    serializer_class = AcceptTokenRequestSerializer
    serializer_details = UserTokenTransferDetails


    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            transactional_pin = serializer.validated_data.get('transactional_pin')
            transactional_id = serializer.validated_data.get('transactional_id')
            amount_in_kroon_token = serializer.validated_data.get('amount_in_kroon_token')

            # checking and verifying transaction pin starts here 
            try:
                check_pin = TransactionalPin.objects.get(user= request.user)
                accept_request = UserRequestToken.objects.get(transactional_id = transactional_id, accepted_status = False)

            except TransactionalPin.DoesNotExist:
                return Response({'status':'error', 'message':'User havent inputed his or her transactional pin.'},status=status.HTTP_404_NOT_FOUND)

            except UserRequestToken.DoesNotExist:
                return Response({'status':'error','message':'transactional id does not exist or its been settled, kindly check your input'},  status=status.HTTP_404_NOT_FOUND)

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
            # transactional pin ends here 
        
            # substracting the amount from the sender user
            sender = User.objects.get(id = request.user.id)
            # checking the amount of the sender
            if Decimal(amount_in_kroon_token) > sender.kroon_token:
                return Response({'status':'error','message':'Insufficent balance'},  status=status.HTTP_404_NOT_FOUND)

            # checking if transaction is already processed
            if accept_request.status == 'successful':
                return Response({'status':'error','message':'token request is already settled'},  status=status.HTTP_404_NOT_FOUND)
            
            # checking if transaction was decliend
            if accept_request.status == 'declined':
                return Response({'status':'error','message':'token request has already been declined, cant process.'},  status=status.HTTP_404_NOT_FOUND)


            # checking if the request user is the same submitting the accept kroon token
            if accept_request.recipient == request.user.id :
                return Response({'status':'error','message':'kroon token requester can be the same user to make a payment.'},  status=status.HTTP_404_NOT_FOUND)

            sender.kroon_token -= Decimal(amount_in_kroon_token)
            sender.save()
            # adding kroon token to the requester user
            recipient = User.objects.get(id = accept_request.recipient.id)
            recipient.kroon_token += Decimal(amount_in_kroon_token)
            recipient.save()

            update_status = UserRequestToken.objects.get(transactional_id =  transactional_id)
            update_status.accepted_status = True
            update_status.save()

            request_record = UserRequestToken.objects.create(recipient = recipient,sender = sender, transactional_id =  accept_request.transactional_id, amount_in_kroon_token = Decimal(amount_in_kroon_token), wallet_id = accept_request.wallet_id, status = 'successful', accepted_status = True )

            # FCM push-notifications
            serverToken = f'{FCM_SERVER_KEY}'
            deviceToken = f'{recipient.device_id}'
            headers = {
                    'Content-Type': 'application/json',
                    'Authorization': 'key=' + serverToken,
                }
            body = {
                    'notification': {
                                    'title': 'KROON TOKEN REQUEST',
                                    'body': f'#{request.user} just accepted your kroon token request , kroon token request helps in paying bills with with zero worries #KroonMan' ,
                                    'sound': 'default',
                                    },
                    'to':deviceToken,
                    'priority': 'high',
                    #   'data': dataPayLoad,
                    }
            response = requests.post("https://fcm.googleapis.com/fcm/send",headers = headers, data=json.dumps(body))

            # Benefactor Transactional Record History
            Transactions.objects.create(user = sender , benefactor = sender, recipient = recipient,amount = amount_in_kroon_token,transactional_id = accept_request.transactional_id, currency = 'KC', narration = f'{sender} accepted {recipient} kroon request', status = 'successful', debited_kroon_amount = Decimal(amount_in_kroon_token), kroon_balance = sender.kroon_token, action = 'KROON REQUEST')

            # Recipient Transactional Record History
            Transactions.objects.create(user = recipient , benefactor = sender, recipient = recipient,amount = amount_in_kroon_token,transactional_id = accept_request.transactional_id, currency = 'KC', narration = f'{sender} accepted {recipient} kroon request', status = 'successful',credited_kroon_amount = Decimal(amount_in_kroon_token),  kroon_balance = recipient.kroon_token,action = 'KROON REQUEST')

            return Response({'status':'success','message':'successfully approve kroon token request.','data':self.serializer_details(request_record).data},  status=status.HTTP_201_CREATED)

        return Response(serializer.errors,  status=status.HTTP_400_BAD_REQUEST)


class StatementOfAccountView (CreateAPIView):
    permission_classes = [ IsAuthenticated, KOKPermission ]
    serializer_class = StatementOfAccountSerilizers
    trans_serializer = TransactionSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            start_date = serializer.validated_data.get('start_date')
            end_date = serializer.validated_data.get('end_date')
            
            # checking if the user is valid to request for statement of account
            count = Transactions.objects.select_related("user", "recipient", "benefactor").filter(user=request.user).count()
            if count < 5:
                return Response({'status':'error','message':'you cant request for statment of account if you havent performed enough transactions.',},  status=status.HTTP_201_CREATED)

            # masking user info for statement of account creation
            masked_id = _createId()
            Mask_Statement_Of_Account.objects.create(user = request.user,masked_id = masked_id ,start_date = start_date, end_date = end_date)

           
            # email notification for topup_payment
            subject = 'Copy Of Your Statement Of Account'
            html_message = render_to_string(
                'emails/statement.html',
                {
                'id':masked_id,
                'start_date':start_date,
                'end_date':end_date,
                } 
            )
            plain_message = strip_tags(html_message)
            from_email = f"{settings.EMAIL_HOST_USER}" 
            to = request.user.email
            mail.send_mail(subject, plain_message, from_email, [to], html_message = html_message)
         
            return Response({'status':'success','message':'successfully created statement of account.',},  status=status.HTTP_201_CREATED)

        return Response(serializer.errors,  status=status.HTTP_400_BAD_REQUEST)


class FastCheckout(CreateAPIView):
    permission_classes = [ IsAuthenticated, KOKPermission ]
    serializer_class = KroonTokenRequestSerializer
    serializer_details = KroonRequestDetails


    def get (self, request, *args, **kwargs):
        # getting all user transactional history
        all_token_transfer = KroonTokenRequest.objects.filter(Q(sender= request.user) | Q(recipient= request.user), action = "FAST CHECKOUT")
        all_token_request_history = KroonRequestDetails(all_token_transfer, many=True)
        return Response({'status':'success','message':'List of fast checkout request' , 'data':all_token_request_history.data}, status=status.HTTP_200_OK)

    def post (self, request, *args, **kwargs):
        trans_ref = transaction_ref()
        serializer = KroonTokenRequestSerializer(data=request.data)
        if serializer.is_valid():
            kroon_token = serializer.data.get('amount_in_kroon_token')
            request_user = request.user
            request_user_wallet_id  = request.user.wallet_id

            # creating token request transaction
            transaction_id = f"KROON_{trans_ref}"
          
            # Recipient Transactional Record History
            Transactions.objects.create(user = request_user ,  recipient = request_user,amount = kroon_token,transactional_id = transaction_id, currency = 'KC', narration = f'{request.user.name} requested for a {kroon_token} kroon token ', status = 'pending',  kroon_balance = request_user.kroon_token,action = 'FAST CHECKOUT')

            tokenRequest = KroonTokenRequest()
            tokenRequest.recipient = request_user
            tokenRequest.amount_in_kroon_token = Decimal(kroon_token)
            tokenRequest.transactional_id = transaction_id
            tokenRequest.wallet_id = request_user_wallet_id
            tokenRequest.action = "FAST CHECKOUT"
            tokenRequest.save()

            return Response({'status':'success', 'message':'fast checkout fees has been generated successfully.', 'data':self.serializer_details(tokenRequest).data},  status=status.HTTP_201_CREATED)

        return Response(serializer.errors,  status=status.HTTP_400_BAD_REQUEST)


class CancelFastCheckoutRequest (CreateAPIView):
    permission_classes = [ IsAuthenticated, KOKPermission ]
    serializer_class = CancelFastCheckoutRequestSerializer

    def post (self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            transactional_id = serializer.validated_data.get('transactional_id')
            try:
                update_record = KroonTokenRequest.objects.get(transactional_id=transactional_id)
            except KroonTokenRequest.DoesNotExist:
                return Response({'status':'error', 'message':'transactional id does not exist'}, status=status.HTTP_404_NOT_FOUND)

            update_record.status = "cancelled"
            update_record.save()

            update_transaction = Transactions.objects.get(transactional_id = transactional_id)
            update_transaction.status = "cancelled"
            update_transaction.save()

            return Response({'status':'success', 'message':'fast checkout has been cancelled successfully.',},  status=status.HTTP_201_CREATED)

        return Response(serializer.errors,  status=status.HTTP_400_BAD_REQUEST)



class FastCheckoutPayment (CreateAPIView):
    permission_classes = [ IsAuthenticated, KOKPermission ]
    serializer_class = PayTokenRequestSerializer
    serializer_details = KroonRequestDetails

    def post(self, request, *args, **kwargs):
        serializer = PayTokenRequestSerializer(data=request.data)
        if serializer.is_valid():
            amount_in_kroon_token = serializer.data.get('kroon_token_amount')
            wallet_id = serializer.data.get('wallet_id')
            transactional_id = serializer.data.get('transactional_id')
            transactional_pin = serializer.data.get('transactional_pin')

            user_check = User.objects.get(wallet_id=wallet_id)
            sender_user = User.objects.get(id = request.user.id)
            
            test = KroonTokenRequest.objects.filter(wallet_id = wallet_id,transactional_id = transactional_id)
            for i in test:
                if i.status == 'successful':
                    return Response({'status':'error','message':'Payment is already settled.',},  status=status.HTTP_401_UNAUTHORIZED)

            try:
                recipient_user = User.objects.get(wallet_id=wallet_id)
                transaction_id = KroonTokenRequest.objects.get(transactional_id = transactional_id, status = 'pending')
            except User.DoesNotExist:
                return Response({'status':'error','message':'Wallet ID does not exists',},  status=status.HTTP_404_NOT_FOUND)

            except KroonTokenRequest.DoesNotExist:
                return Response({'status':'error','message':'Transactonal ID does not exists',},  status=status.HTTP_404_NOT_FOUND)

            if request.user.country_of_residence != recipient_user.country_of_residence:
                return Response({'status':'error', 'message':'internation kroon transaction is not allowed at the moment.'},  status=status.HTTP_404_NOT_FOUND) 

            if user_check.id == request.user.id:
                return Response({'status':'error','message':'Scan to Pay cant be performed by the same token request user',},  status=status.HTTP_404_NOT_FOUND)

            if Decimal(amount_in_kroon_token) > sender_user.kroon_token:
                return Response({'status':'error','message':'Insufficent balance , transaction can not be completed'},  status=status.HTTP_404_NOT_FOUND)

            if transaction_id.amount_in_kroon_token != Decimal(amount_in_kroon_token):
                return Response({'status':'error','message':'the amount initialized is not the same amount with the token request.',},  status=status.HTTP_404_NOT_FOUND)

            # checking and verifying transaction pin starts here 
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

            # validations end here 

            sender_user.kroon_token -= Decimal(amount_in_kroon_token)
            sender_user.save()   
            transaction_num = transaction_id.transactional_id    
           
            user_check.kroon_token += Decimal(amount_in_kroon_token)
            user_check.save()
            
        
            request_user_history = KroonTokenRequest()
            request_user_history.recipient = user_check
            request_user_history.sender = sender_user
            request_user_history.transactional_id = transaction_num
            request_user_history.amount_in_kroon_token = Decimal(amount_in_kroon_token)
            request_user_history.wallet_id = user_check.wallet_id
            request_user_history.status = 'successful'
            request_user_history.action = "FAST CHECKOUT"
            request_user_history.save()

            # FCM push-notifications
            serverToken = f'{FCM_SERVER_KEY}'
            deviceToken = f'{user_check.device_id}'
            headers = {
                    'Content-Type': 'application/json',
                    'Authorization': 'key=' + serverToken,
                }
            body = {
                    'notification': {
                                    'title': 'FAST CHECKOUT SETTLED',
                                    'body': f'Fast checkout has been settled by {sender_user.name}, fast checkout helps merchants to ensure the fastest checkout for their customers #KroonMan' ,
                                    'sound': 'default',
                                    },
                    'to':deviceToken,
                    'priority': 'high',
                    #   'data': dataPayLoad,
                    }
            response = requests.post("https://fcm.googleapis.com/fcm/send",headers = headers, data=json.dumps(body))

            
            # Benefactor Transactional Record History
            Transactions.objects.create(user = request.user, benefactor = request.user, recipient = user_check,amount = Decimal(amount_in_kroon_token),transactional_id = transaction_num, currency = 'KC', narration = f'fast checkout paid By {sender_user} was successfully',action = "FAST CHECKOUT", status = 'successful', debited_kroon_amount = Decimal(amount_in_kroon_token), kroon_balance = sender_user.kroon_token )

            # Recipient Transactional Record History
            Transactions.objects.create(user = user_check , benefactor = request.user, recipient = user_check,amount = Decimal(amount_in_kroon_token),transactional_id = transaction_num, currency = 'KC', narration = f'fast checkout paid By {sender_user} was successfully',action = "FAST CHECKOUT", status = 'successful', credited_kroon_amount = Decimal(amount_in_kroon_token) , kroon_balance = user_check.kroon_token)

            return Response({'status':'success','message':'fast checkout is been completed successfully','data':self.serializer_details(request_user_history).data },  status=status.HTTP_200_OK)

                        
        return Response(serializer.errors,  status=status.HTTP_400_BAD_REQUEST)



class Verify_Transactionan_Pin_View ( CreateAPIView ):
    """
    verify transactional pin

    **Verify Transactional Pin**

    This call verifies the user transactional pin.

    **PATH PARAMS**

    **transactional_pin**

    This transactional_pin is been created using the create-transactional-pin endpoints, which is required to perform some sensitive validations.
    """
    permission_classes = [ IsAuthenticated, KOKPermission ]
    serializer_class = Transactional_Pin_Serializer

    def post (self, request, *args, **kwargs):
        serializer = self.serializer_class( data = request.data )
        if serializer.is_valid():
            transactional_pin = serializer.data.get('transactional_pin')

             # checking and verifying transaction pin starts here 
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
                return Response({'status':'success','message':'transactional pin is valid'},  status=status.HTTP_200_OK)



        return Response(serializer.errors,  status=status.HTTP_400_BAD_REQUEST)

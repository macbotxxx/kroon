from decimal import Decimal
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.generics import ListAPIView , CreateAPIView, UpdateAPIView, get_object_or_404
from rest_framework import status
from django.contrib.auth.hashers import make_password, check_password
from helpers.common.security import KOKPermission
from kroon.users.models import UserWrongPinValidate
from transactions.models import Transactions, TransactionalPin

from kroon.users.models import User
from kroon_gift.models import KroonGift

from .serializers import KroonGiftSerializer, RedeemKroonGift, KroonGiftInfoSerializer, GiftDetails

import string
import random
import requests
import json
from django.conf import settings


# django email settings
from django.core import mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
import threading

def transaction_ref():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=20))

class KroonGiftView(CreateAPIView):
    permission_classes = [ IsAuthenticated, KOKPermission ]
    serializer_class = KroonGiftSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data.get('email')
            amount = serializer.validated_data.get('amount')
            redeem_pin = serializer.validated_data.get('redeem_pin')
            transactional_pin = serializer.validated_data.get('transactional_pin')
            
            # checking if the user is an already registered user
            try:
                check_user = User.objects.get(email=email)
                if check_user:
                    return Response({'status': 'error','message':'the following user is an already registered user, kindly use the kroon token transfer method'}, status=status.HTTP_404_NOT_FOUND)
            except User.DoesNotExist:
                pass

              # checking and verifying transaction pin
            try:
                check_pin = TransactionalPin.objects.get(user= request.user)
                pasd = check_pin.password
                verify_pin = check_password(transactional_pin,pasd)
            except TransactionalPin.DoesNotExist:
                msg = {"User havent inputed his or her transactional pin."}
                return Response({'status':'Failed', 'message':msg},status=status.HTTP_404_NOT_FOUND)

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
                            msg = {'warning': 'your transactional pin have been disabled, an opt message has been sent to reset your pin', }
                            return Response({'error':msg},  status=status.HTTP_404_NOT_FOUND)
                        else:
                            failed_pin.failed_password += 1
                            update = UserWrongPinValidate.objects.get(user=request.user)
                            update.failed_password = failed_pin.failed_password
                            update.save()
                            msg = {'warning': 'Transactional pin is not valid', }
                            return Response({'error':msg},  status=status.HTTP_404_NOT_FOUND)
                except UserWrongPinValidate.DoesNotExist:
                    UserWrongPinValidate.objects.create(user=request.user)
                    msg = {'warning': 'Transactional pin is not valid', }
                    return Response({'error':msg},  status=status.HTTP_404_NOT_FOUND)

            else:
                try:
                    UserWrongPinValidate.objects.get(user=request.user).delete()
                except UserWrongPinValidate.DoesNotExist:
                    pass


            if KroonGift.objects.filter(email = email).exists():
                return Response({'status': 'error','message':'the following user is already been gifted kroon token.'}, status=status.HTTP_404_NOT_FOUND)

            # checking for insufficent balance
            if Decimal(amount) > request.user.kroon_token:
                return Response({'status':'error','message':'insufficent balance , the gift amount is above your current kroon token balance',},  status=status.HTTP_404_NOT_FOUND)

            # reducting the amount from the user kroon token account.
            user_account = User.objects.get(id = request.user.id)
            user_account.kroon_token -= Decimal(amount)
            user_account.save()

            trans_ref = f"KROON_GIFT_{transaction_ref()}"
            # adding tramsactional pin 
            redeem_pin_hashed = make_password(redeem_pin,salt=None, hasher='default')
            # saving kroon gift record 
            serializer = KroonGift.objects.create(user = request.user, email = email, amount = amount, transactional_id = trans_ref, redeem_pin = redeem_pin_hashed, country = request.user.country_of_residence)

           
            # Benefactor Transactional Record History
            Transactions.objects.create(user = self.request.user , benefactor = request.user,amount = Decimal(amount),transactional_id = trans_ref, currency = 'KC', narration = f'{request.user.name} gift kroon token to {email}',action = 'GIFT KROON TOKEN', status = 'successful', debited_kroon_amount = Decimal(amount) , kroon_balance = user_account.kroon_token)

            # sending email to the user about to be giftted kroon token 
            gift_kroon_details = KroonGift.objects.filter(email = email)
            subject = 'You Have Been Gifted Kroon Token'
            html_message = render_to_string(
                'emails/gift_kroon.html',
                {
                'user': request.user,
                'gift_details': gift_kroon_details,
                'redeem_pin':redeem_pin,
                } 
            )
            plain_message = strip_tags(html_message)
            from_email = f"{settings.EMAIL_HOST_USER}" 
            to = email
            mail.send_mail(subject, plain_message, from_email, [to], html_message = html_message)

            return Response({'status':'success','message':'kroon gift has been successfully.'}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors,  status=status.HTTP_400_BAD_REQUEST)


class RedeemKroonGiftView (CreateAPIView):
    permission_classes = [ IsAuthenticated, KOKPermission ]
    serializer_class = RedeemKroonGift

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data.get('email')
            redeem_pin = serializer.validated_data.get('redeem_pin')
            transactional_pin = serializer.validated_data.get('transactional_pin')

            try:
                gifted_user = KroonGift.objects.get(email=email,)
            except KroonGift.DoesNotExist:
                return Response({'status':'error','message':' the above user havent been gifted any kroon token',},  status=status.HTTP_404_NOT_FOUND)

            if gifted_user.settled == True:
                return Response({'status':'error','message':'the above user has been credited his or her gift kroon token',},  status=status.HTTP_404_NOT_FOUND)

            # verifying the redeem token
            pasd = gifted_user.redeem_pin
            verify_pin = check_password(redeem_pin,pasd)

            if not verify_pin:
                return Response({'status':'error','message':'kroon gift redeem pin is not valid',},  status=status.HTTP_404_NOT_FOUND)

            if request.user.country_of_residence != gifted_user.country:
                return Response({'status':'error','message':'cant redeem a kroon gifted from another country',},  status=status.HTTP_404_NOT_FOUND)
  
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

            gift_user = User.objects.get(email = email)
            gift_user.kroon_token += Decimal(gifted_user.amount)
            gift_user.save()

            # final update on the gift user settle sections
            gifted_user.settled = True
            gifted_user.save()

       
            # Recipient Transactional Record History
            Transactions.objects.create(user = gifted_user.user , benefactor = gifted_user.user, recipient = request.user,amount = Decimal(gifted_user.amount),transactional_id = gifted_user.transactional_id, currency = 'KC', narration = f'{gifted_user.user} gift kroon token to {request.user}',action = 'GIFT KROON TOKEN', status = 'successful', credited_kroon_amount = Decimal(gifted_user.amount) , kroon_balance = gift_user.kroon_token)

            return Response({'status':'success','message':'kroon gift has been successfully.', 'data':serializer.data}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors,  status=status.HTTP_400_BAD_REQUEST)
        
class KroonGiftInfoView (CreateAPIView):
    permission_classes = [ IsAuthenticated, KOKPermission ]
    serializer_class = KroonGiftInfoSerializer
    serializer_details = GiftDetails

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data.get('email')
            try:
                user_email = KroonGift.objects.get(email=email, settled = False)
            except KroonGift.DoesNotExist:
                return Response({'status':'error', 'message':'email havent been gifted or it has been settled'}, status=status.HTTP_404_NOT_FOUND)

            serializer = self.serializer_details(user_email)
            return Response({'status':'success','message':'email has been gifted a kroon token', 'data':serializer.data},  status=status.HTTP_202_ACCEPTED)

        return Response(serializer.errors,  status=status.HTTP_400_BAD_REQUEST)
        

from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.generics import  CreateAPIView
from helpers.common.security import KOKPermission
from django.core.mail import send_mail


from .serializers import OTPSerializer, EmailOtpSerializer
from notifications.tasks import send_otp_email_func 

from kroon_otp.models import OPTs

from django.conf import settings

import string
import random

import datetime
import pytz

utc=pytz.UTC

from datetime import datetime, timezone

# django email settings
from django.core import mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
import threading


def opt_code():
    return ''.join(random.choices(string.digits, k=6))


class EmailOpt (CreateAPIView):
    permission_classes = [ AllowAny, KOKPermission ]
    serializer_class = EmailOtpSerializer

    def post(self, request, *args, **kwargs):
        opt_pin = opt_code()
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data.get('email')
            platform = serializer.validated_data.get('platform')
        
            # # checking if the user already have an otp
            OPTs.objects.filter(email=email).delete()
            OPTs.objects.create(email=email,otp_code= opt_pin)

            # send otp to the user email address
            send_otp_email_func.delay( email = email , otp_pin = opt_pin , platform = platform )
            # store otp 
            return Response({'status':'success','message':'Opt pin has been sent successfully'},  status=status.HTTP_201_CREATED)

        return Response(serializer.errors,  status=status.HTTP_400_BAD_REQUEST)
    

class EmailFuncTest (CreateAPIView):
    permission_classes = [ AllowAny, KOKPermission ]
    serializer_class = EmailOtpSerializer

    def post(self, request, *args, **kwargs):
        opt_pin = opt_code()
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data.get('email')
            platform = serializer.validated_data.get('platform')
        
            subject = 'MacBot9219, a festive season of Xbox savings has started!'
            html_message = render_to_string(
                    'emails/google.html',
                    {
                    'user': "Hello",
                    'opt': 2992,
                    'content':"mike",
                    } 
            )
               
            plain_message = strip_tags(html_message)
            from_email = "support@kroonkiosk.com" 

            to = email
            mail.send_mail(subject, plain_message, from_email, [to], html_message = html_message)
            # store otp 
            return Response({'status':'success','message':'Opt pin has been sent successfully'},  status=status.HTTP_201_CREATED)

        return Response(serializer.errors,  status=status.HTTP_400_BAD_REQUEST)

         
class OTPVerification(CreateAPIView):
    permission_classes = [ AllowAny, KOKPermission ]
    serializer_class = OTPSerializer

    def post(self, request, *args, **kwargs):
        serializer = OTPSerializer(data = request.data)
        
        if serializer.is_valid():
            otp_pin = serializer.validated_data.get('otp_pin')
            email = serializer.validated_data.get('email')
            # validating OTP pin 
            if email:
                try:
                    check_otp = OPTs.objects.get( otp_code = otp_pin, email = email )
                    
                except OPTs.DoesNotExist:
                    return Response({'status':'error','message':'OTP pin is invalid, kindly check your input'},  status=status.HTTP_404_NOT_FOUND)
                
                #checking and verifying if the pin is invalid or expired  
                current_time = datetime.now()
                # check_otp_duration = utc.localize(check_otp.duration)
                current_time = utc.localize(current_time)
                
                if check_otp.duration < current_time:
                    return Response({'status':'error','message':'OTP pin has expired'},  status=status.HTTP_404_NOT_FOUND)
                else:
                    check_otp.delete()
                    return Response({'status':'success','message':'OTP pin is valid'},  status=status.HTTP_202_ACCEPTED)
            else:
                check_otp = OPTs.objects.filter(otp_code = otp_pin)
                if check_otp:
                    #checking and verifying if the pin is invalid or expired  
                    current_time = datetime.now()
                    # check_otp_duration = utc.localize(check_otp.duration)
                    current_time = utc.localize(current_time)
                    for i in check_otp:
                        if i.duration < current_time:
                            return Response({'status':'error','message':'OTP pin has expired'},  status=status.HTTP_404_NOT_FOUND)
                        else:
                            check_otp.delete()
                            return Response({'status':'success','message':'Opt pin valid'},  status=status.HTTP_202_ACCEPTED)
                else:
                    return Response({'status':'error','message':'Opt pin is invalid or expired'},  status=status.HTTP_404_NOT_FOUND)
               
        return Response({'status':'error','message':'The input is not valid.'},  status=status.HTTP_404_NOT_FOUND)
        
    

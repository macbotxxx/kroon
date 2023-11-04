import json
import random
import string
from django.http import JsonResponse

from rest_framework import  status
from rest_framework.response import Response
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.utils import timezone
from django.core import mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.contrib import messages
from datetime import timedelta, datetime
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Count , Sum
from django.core.mail import send_mail


from helpers.common.security import KOKPermission , KOKMerchantPermission
from subscriptions.models import Subscription_Plan ,Merchant_Subcribers
from promotional_codes.models import Government_Promo_Code, Discount_Code
from helpers.subscriptions.apple import Apple_Service
from helpers.subscriptions.google import Google_Service
from helpers.subscriptions.huawei import Huawei_Service
from .serializers import Gov_Promo_Code_Serializer , In_App_Sub_check , In_App_Sub_Migrate, MerchantSubSerializer
from kiosk_cart.api.views import _company_account , _company_account_in_app
from notifications.tasks import kiosk_promo_code_email
from kiosk_stores.models import Merchant_Product



class Gov_promo_code_view (CreateAPIView):
    permission_classes = [ IsAuthenticated, KOKPermission , KOKMerchantPermission ]
    serializer_class = Gov_Promo_Code_Serializer

    def post (self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        company_profile = _company_account(request)

        if serializer.is_valid():
            promo_code = serializer.validated_data.get('promo_code')

            # Checking if the code is a discount code or a susbscription code
            discount = Discount_Code.objects.filter( discount_code = promo_code , used_code = False )
            if discount.exists():
                for i in discount:
                    i.user = self.request.user
                    i.used_code = True
                    i.save()
                return Response({'status':'success', 'message':'the discount code is valid'}, status=status.HTTP_202_ACCEPTED)
            else:
                pass

            try:
                code = Government_Promo_Code.objects.get ( promo_code = promo_code , used_code = False  )
                plan = code.code_plan
                days = code.code_plan.plan_duration
                end_date = datetime.now()+timedelta( days = days )

                 # get the privious plan and deactivates it 
                try:
                    # deactivating the old plan
                    old_plan = Merchant_Subcribers.objects.get( user = self.request.user , active = True )
                    old_plan.active = False
                    old_plan.end_date = datetime.now()
                    old_plan.save()

                    # activating the new plans
                    Merchant_Subcribers.objects.create( user = self.request.user , active = True , plan = plan , end_date = end_date , sub_plan_id = plan.slug_plan_name )
                    # email parameters
                    subject = 'Successful Payment'
                    email = self.request.user.email
                    s = Merchant_Subcribers.objects.get( user = self.request.user , active = True )

                    invoice_id = s.id
                    if s.yearly_plan:
                        amount_paid = s.plan.yearly_plan_fee
                        plan_duration = s.plan.yearly_plan_duration
                    else:
                        amount_paid = s.plan.plan_fee
                        plan_duration = s.plan.plan_duration

                    sub_type = s.plan.plan_name
                    sub_start_date = s.start_date
                    sub_end_date = s.end_date

                    # # sending email
                    kiosk_promo_code_email.delay( subject = subject , invoice_id = invoice_id , amount_paid = amount_paid, plan_duration = plan_duration , sub_type = sub_type , sub_start_date = sub_start_date , sub_end_date = sub_end_date ,  email = email )
                
                except Merchant_Subcribers.DoesNotExist:
                    # activating the new plans
                    Merchant_Subcribers.objects.create( user = request.user , active = True , plan = plan , end_date = end_date , sub_plan_id = plan.slug_plan_name )
                    

                    subject = 'Successful Payment'
                    email = self.request.user.email
                    s = Merchant_Subcribers.objects.get( user = self.request.user , active = True )

                    invoice_id = s.id
                    if s.yearly_plan:
                        amount_paid = s.plan.yearly_plan_fee
                        plan_duration = s.plan.yearly_plan_duration
                    else:
                        amount_paid = s.plan.plan_fee
                        plan_duration = s.plan.plan_duration

                    sub_type = s.plan.plan_name
                    sub_start_date = s.start_date
                    sub_end_date = s.end_date

                    # # sending email
                    kiosk_promo_code_email.delay( subject = subject , invoice_id = invoice_id , amount_paid = amount_paid, plan_duration = plan_duration , sub_type = sub_type , sub_start_date = sub_start_date , sub_end_date = sub_end_date ,  email = email )

                # expiring the promo code 
                code.used_code = True
                code.user = request.user
                code.save()

                return Response({'status':'success', 'message':'subscription is been activated'}, status=status.HTTP_201_CREATED)

            except Government_Promo_Code.DoesNotExist:
                return Response({'status':'error', 'message':'Promotional code is ether inactive or incorrect , kindly check the code and try again. '}, status=status.HTTP_404_NOT_FOUND)
                
        return Response(serializer.errors,  status=status.HTTP_400_BAD_REQUEST)



class InAppSubCheckView (CreateAPIView):
    permission_classes = [ IsAuthenticated, KOKPermission , KOKMerchantPermission ]
    serializer_class = In_App_Sub_check

    def create (self, request, *args, **kwargs):
        serializer = self.serializer_class( data = request.data )
        if serializer.is_valid():
            device_type = serializer.validated_data.get('device_type')
            receipt_data = serializer.validated_data.get('receipt_data')
            subcription_id = serializer.validated_data.get('subcription_id')

            if device_type == 'apple':
                apple_verification = Apple_Service()
                verify_data = apple_verification.verify_receipt_data( receipt_data = receipt_data )
                if verify_data['status_action']:
                    return Response({'status':'success', 'message':'subscription verification is handled successfully', 'verification':verify_data['status_action'], 'exp_date':verify_data['exp_date']}, status=status.HTTP_200_OK)
                else:
                    return Response({'status':'error', 'message':'subcription is not handled or invalid', 'verification':verify_data['status_action'], 'exp_date':verify_data['exp_date']}, status=status.HTTP_400_BAD_REQUEST)
                
            elif device_type == 'google':
                google_verification = Google_Service()
                verify_data = google_verification.verify_subscription_token( subcription_id = subcription_id , receipt_data = receipt_data )

                if verify_data['status_action']:
                    return Response({'status':'success', 'message':'subscription verification is handled successfully', 'verification':verify_data['status_action'], 'exp_date':verify_data['exp_date']}, status=status.HTTP_200_OK)
                else:
                    return Response({'status':'error', 'message':'subcription is not handled or invalid', 'verification':verify_data['status_action'], 'exp_date':verify_data['exp_date']}, status=status.HTTP_400_BAD_REQUEST)

            elif device_type == 'huawei':
                huawei_verification = Huawei_Service()
                verify_data = huawei_verification.subscription_verification( subcription_id = subcription_id , receipt_data = receipt_data )
                if verify_data['status_action']:
                    return Response({'status':'success', 'message':'subscription verification is handled successfully', 'verification':verify_data['status_action'], 'exp_date':verify_data['exp_date']}, status=status.HTTP_200_OK)
                else:
                    return Response({'status':'error', 'message':'subcription is not handled or invalid', 'verification':verify_data['status_action'], 'exp_date':verify_data['exp_date']}, status=status.HTTP_400_BAD_REQUEST)
                
            else:
                return Response({'status':'error', 'message':'device type is not found, kindly check the parameter and try again. '}, status=status.HTTP_404_NOT_FOUND)
    
        return Response(serializer.errors,  status=status.HTTP_400_BAD_REQUEST)


class Inapp_sub_migrations (CreateAPIView):
    permission_classes = [ IsAuthenticated, KOKPermission , KOKMerchantPermission ]
    serializer_class = In_App_Sub_Migrate

    def create (self, request, *args, **kwargs):
        serializer = self.serializer_class( data = request.data )
        company_profile = _company_account(request)

        if serializer.is_valid():
            device_type = serializer.validated_data.get('device_type')
            receipt_data = serializer.validated_data.get('receipt_data')
            subcription_id = serializer.validated_data.get('subcription_id')
            exp_date = serializer.validated_data.get('exp_date')
            product_id = serializer.validated_data.get('product_id')
            yearly_product_id = serializer.validated_data.get('yearly_product_id')
            # cancilling the previous subscription
            old_sub = Merchant_Subcribers.objects.filter( user = self.request.user )
            for i in old_sub:
                i.active = False
                i.end_date = timezone.now()
                i.save()
            
            sub = Merchant_Subcribers.objects.create( user = self.request.user, plan = Subscription_Plan.objects.get( slug_plan_name = product_id ) ,start_date = timezone.now() ,end_date = exp_date , device_type = device_type , subscription_id = subcription_id , receipt_data = receipt_data , active = True , sub_plan_id = yearly_product_id )

            subject = 'Successful Payment'
            email = self.request.user.email
            s = Merchant_Subcribers.objects.get( user = self.request.user , active = True )

            invoice_id = s.id
            if s.yearly_plan:
                amount_paid = s.plan.yearly_plan_fee
                plan_duration = s.plan.yearly_plan_duration
            else:
                amount_paid = s.plan.plan_fee
                plan_duration = s.plan.plan_duration

            sub_type = s.plan.plan_name
            sub_start_date = s.start_date
            sub_end_date = s.end_date

            # # sending email
            kiosk_promo_code_email.delay( subject = subject , invoice_id = invoice_id , amount_paid = amount_paid, plan_duration = plan_duration , sub_type = sub_type , sub_start_date = sub_start_date , sub_end_date = sub_end_date ,  email = email )
            
            return Response({'status':'success', 'message':'subscription migration is handled successfully'}, status=status.HTTP_200_OK)
            
        return Response(serializer.errors,  status=status.HTTP_400_BAD_REQUEST)


class Obtain_Cre (CreateAPIView):
    permission_classes = [ IsAuthenticated, KOKPermission , KOKMerchantPermission ]
    serializer_class = In_App_Sub_check

    def create (self, request, *args, **kwargs):
        google_func = Google_Service()
        obtain_v = google_func.obtain_credentials()
        return Response({'status':'success', 'message':'subscription verification is handled successfully', 'verification':obtain_v}, status=status.HTTP_200_OK)
    

class MerchantSubID(ListAPIView):
    permission_classes = [ IsAuthenticated, KOKPermission , KOKMerchantPermission ]
    serializer_class = MerchantSubSerializer
    queryset = Merchant_Subcribers.objects.all()

    def get_object(self):
        qs = self.get_queryset().filter( active = True , user = self.request.user ).first()
        return qs
    
    def list (self , request , *args, **kwargs):
        qs = self.get_object()
        serializer = self.get_serializer(qs)
        return Response( serializer.data )



class TestEnd (ListAPIView):
    permission_classes = [ AllowAny,]
    serializer_class = MerchantSubSerializer

    def get (self, request, *args, **kwargs):
        products_qs = Merchant_Product.objects.filter( expire_notify = True ).values('business_profile').annotate( total_expired_products = Count('expire_notify'))
        print(products_qs)
        for i in products_qs:
            exired_qs = Merchant_Product.objects.filter( expire_notify = True , business_profile = i['business_profile'] ).values('expiry_days_notify').annotate( total_expired_pros = Count('expire_notify'))
            merchant_email = Merchant_Product.objects.filter(business_profile = i['business_profile']).first()
            print(exired_qs)
            for e in exired_qs:
                exp_pro = Merchant_Product.objects.filter( expire_notify = True , business_profile = i['business_profile'] ).values('expiry_days_notify').annotate( total_expired_products = Count('expire_notify'))
                for p in exp_pro:
                    # Get the current date
                    current_date = datetime.now()
                    # Calculate the date 3 days from now
                    three_days_from_now = current_date + timedelta(days=int(p['expiry_days_notify']))

                    ex_products_qs = Merchant_Product.objects.filter( expire_notify = True , business_profile = i['business_profile'] , expiring_date__lte = three_days_from_now )
                    
        send_mail(
                "Subject here",
                f"{ex_products_qs}",
                "from@example.com",
                [f"{merchant_email.user.email}"],
                fail_silently=False,
            )
                
        return Response('completed')
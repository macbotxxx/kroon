import string
import random

from rest_framework import  status
from rest_framework.response import Response
from rest_framework.views import APIView
# from rest_auth.views import LoginView as RestLoginView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.generics import ListAPIView, CreateAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView, GenericAPIView
from django.views.decorators.debug import sensitive_post_parameters
from django.utils.decorators import method_decorator
# django email settings
from django.utils import timezone
from datetime import timedelta, datetime


from rest_framework_simplejwt.views import TokenObtainPairView
from helpers.common.security import KOKPermission , KOKMerchantOnly
from helpers.common.disable_account import Delete_Accounts
from kiosk_categories.models import Category
from kroon_otp.models import OPTs
from subscriptions.models import Subscription_Plan , Merchant_Subcribers
from notifications.tasks import send_otp_email_func

from .serializers import UserAddressSerializer, UserBankDetailsSerializer, KroonTermsAndConditionsSerializer, ForgetPasswordEmailNotification, ForgotPasswordSerilizer, UpdateDeviceIdSerilizer,BusinessProfileSerilizer,  PolicyAndConditionSerializer, KroonFQASerializer, MyTokenObtainPairSerializer, UpdateUserDeviceInfoSerializer ,KioskFQASerializer , KroonKioskToken 

from kroon.users.models import User, UserAddress, UserBankDetails,  KroonTermsAndConditions, BusinessProfile, PolicyAndCondition, KroonFQA, KioskFAQ

# FCM push notification configuration
from django.conf import settings


sensitive_post_parameters_m = method_decorator(
    sensitive_post_parameters(
        'password', 'old_password', 'new_password1', 'new_password2'
    )
)

def otp_code():
    return ''.join(random.choices(string.digits, k=6))


# class Login(RestLoginView):
#     permission_classes = (AllowAny,)
#     # serializer_class = None

#     def post(self, request, *args, **kwargs):
#         serializer = LoginUserSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         user = serializer.validated_data['user']
#         login(request, user)
#         return super().post(request, format=None)


class MyTokenObtainPairView(TokenObtainPairView):
    permission_classes = [ AllowAny, KOKPermission ]
    serializer_class = MyTokenObtainPairSerializer

class KroonKioskTokenView (TokenObtainPairView):
    permission_classes = [ AllowAny, KOKPermission ]
    serializer_class = KroonKioskToken


class UserAddressView (ListCreateAPIView):
    permission_classes = [ IsAuthenticated, KOKPermission ]
    serializer_class = UserAddressSerializer
    queryset = UserAddress.objects.all()


    def post(self, request, *args, **kwargs):
        serializer = UserAddressSerializer(data=request.data)
        if serializer.is_valid():
            user_address = UserAddress()
            user_address.type = serializer.data.get('type')
            user_address.user = request.user
            user_address.street_or_flat_number = serializer.data.get('street_or_flat_number')
            user_address.street_name = serializer.data.get('street_name')
            user_address.building_name = serializer.data.get('building_name')
            user_address.state = serializer.data.get('state')
            user_address.city = serializer.data.get('city')
            user_address.zip_post_code = serializer.data.get('zip_post_code')
            user_address.save()
            user_info = User.objects.get(id=self.request.user.id)
            user_info.address.add(user_address)
            # user_info.set()
            return Response({'status':'success','message':'user home address is setup successfully','data':UserAddressSerializer(user_address).data}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors,  status=status.HTTP_400_BAD_REQUEST)


class UpdateUserAddressView (RetrieveUpdateDestroyAPIView):
    permission_classes = [ IsAuthenticated, KOKPermission ]
    serializer_class = UserAddressSerializer
    queryset = UserAddress.objects.all()
    lookup_field = 'id'



class UserBankDetailsView (ListAPIView, CreateAPIView ):
    
    permission_classes = [ IsAuthenticated, KOKPermission ]
    serializer_class = UserBankDetailsSerializer

    def get (self, request, *args, **kwargs):
        try:
            user_bank_details = UserBankDetails.objects.get(user=request.user)   
        except UserBankDetails.DoesNotExist:
            return Response({'status': 'error', 'message':'user havent inputted any bank details'},  status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(user_bank_details)
        return Response({'status': 'success', 'message':'user bank details fetched', 'data': serializer.data}) 

    def patch (self, request, *args, **kwargs):
        serializer = UserBankDetailsSerializer(data=request.data)
        if serializer.is_valid():
            account_number = serializer.validated_data.get('account_number')
            account_name = serializer.validated_data.get('account_name')
            bank_code = serializer.validated_data.get('bank_code')
            bank_name = serializer.validated_data.get('bank_name')

            try:
                user_account = UserBankDetails.objects.get(user=request.user)
            except UserBankDetails.DoesNotExist:
                return Response({'status':'error','message':'user havent inputted his or her local bank details',}, status=status.HTTP_404_NOT_FOUND)

            # checking if account number exists 
            # check_account_number = UserBankDetails.objects.filter(account_number = account_number, user = request.user)
            # if check_account_number:
            #     return Response({'status':'error','message':'account details cant be inputted because its been assigned to another user.'},  status=status.HTTP_400_BAD_REQUEST)
           
            # return response_data['status'],response_data['data']
           
            user_account.user = request.user
            user_account.account_name = account_name
            user_account.account_number = account_number
            user_account.bank_name = bank_name
            user_account.bank_code = bank_code
            user_account.verified = True
            user_account.save()
            user_info = User.objects.get(id=self.request.user.id)
            user_info.bank_details = user_account
            user_info.save()
            
            return Response({'status':'success','message':'bank account details has been updated successfully','data':UserBankDetailsSerializer(user_account).data}, status=status.HTTP_201_CREATED)  

    def post(self, request, *args, **kwargs):
        # PAYSTACK_SECRET_KEY = settings.PAYSTACK_SECRET_KEY
        serializer = UserBankDetailsSerializer(data=request.data)
        if serializer.is_valid():
            account_number = serializer.data.get('account_number')
            account_name = serializer.data.get('account_name')
            bank_code = serializer.data.get('bank_code')
            bank_name = serializer.data.get('bank_name')

            # checking if account number exists 
            check_account_number = UserBankDetails.objects.filter(user = request.user)
            if check_account_number:
                return Response({'status':'error','message':'account details has already been created'},  status=status.HTTP_400_BAD_REQUEST)
        
            user_bank = UserBankDetails()
            user_bank.user = request.user
            user_bank.account_name = account_name
            user_bank.account_number = account_number
            user_bank.bank_name = bank_name
            user_bank.bank_code = bank_code
            user_bank.verified = True
            user_bank.save()
            user_info = User.objects.get(id=self.request.user.id)
            user_info.bank_details = user_bank
            user_info.save()

            return Response({'status':'success','message':'account details has been created successfully','data':UserBankDetailsSerializer(user_bank).data}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors,  status=status.HTTP_400_BAD_REQUEST)

class KroonTermsAndConditionsView (APIView):
    permission_classes = [ AllowAny, KOKPermission ]
    serializer_class = KroonTermsAndConditionsSerializer

    def get(self, request, *args, **kwargs):
        platform = kwargs.get('platform')
        try:
            terms = KroonTermsAndConditions.objects.get( active = True , platform = platform)
            serializer = self.serializer_class(terms)
            return Response({'status':'success','message':'Kroon terms and conditions fetch successfully.','data':serializer.data},status=status.HTTP_200_OK)
        
        except KroonTermsAndConditions.DoesNotExist :
            return Response({'status': 'error', 'message':'not found in your database'},status=status.HTTP_404_NOT_FOUND)


class PolicyAndConditionView (ListAPIView):
    permission_classes = [ AllowAny, KOKPermission ]
    serializer_class = PolicyAndConditionSerializer

    def get(self, request, *args, **kwargs):
        platform = kwargs.get('platform')
        try:
            terms = PolicyAndCondition.objects.get( active=True , platform = platform)
            serializer = self.serializer_class(terms)
            return Response({'status':'success','message':'Kroon policy fetch successfully.','data':serializer.data},status=status.HTTP_200_OK)
        except PolicyAndCondition.DoesNotExist:
            return Response({'status': 'error', 'message':'not found in your database'},status=status.HTTP_404_NOT_FOUND)


class ForgetPasswordEmailNotificationView (CreateAPIView):
    permission_classes = [ AllowAny, KOKPermission ]
    serializer_class = ForgetPasswordEmailNotification

    def post (self, request, *args, **kwargs):
        otp_pin = otp_code()
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data.get('email')

            try:
                user_details = User.objects.get(email=email)
            except User.DoesNotExist:
                return Response({'status': 'error', 'message':'The e-mail address is not assigned to any user account'}, status=status.HTTP_404_NOT_FOUND)
            
            content ="you are getting this email because a kroon user requested for a change of password, kindly input the following OTP code or ignore this email if it wasnt you — it will expire in 15 minutes:"
                
            # checking if the user already have an otp
            send_otp_email_func.delay( forget_password_content = content , otp_pin = otp_pin , platform = "kiosk", email = email )
           
            OPTs.objects.filter(email=email).delete()
            OPTs.objects.create(email=email,otp_code= otp_pin)

            return Response({'status':'success','message':'an opt has been sent to the following email for password change'},  status=status.HTTP_201_CREATED)

        return Response(serializer.errors,  status=status.HTTP_400_BAD_REQUEST)


class ForgotPasswordSerilizerView (CreateAPIView):
    permission_classes = [ AllowAny, KOKPermission ]
    serializer_class = ForgotPasswordSerilizer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data.get('email')
            new_password1 = serializer.validated_data.get('new_password1')
            new_password2 = serializer.validated_data.get('new_password2')

            # validating the passwords 
            if new_password1 != new_password2:
                return Response({'status':'error', 'message':'Your old password was entered incorrectly michake. Please enter it again.'}, status=status.HTTP_404_NOT_FOUND)

            try:
                user_details = User.objects.get(email=email)
            except User.DoesNotExist:
                return Response({'status': 'error', 'message':'The e-mail address is not assigned to any user account'}, status=status.HTTP_404_NOT_FOUND)

            user_details.set_password(new_password1)
            user_details.save()
            return Response({'status': 'success', 'message':'user account password has been updated successfully'}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors,  status=status.HTTP_400_BAD_REQUEST)


class UpdateDeviceId (CreateAPIView):
    permission_classes = [ IsAuthenticated, KOKPermission ]
    serializer_class = UpdateDeviceIdSerilizer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            device_id = serializer.validated_data.get('device_id')
            device_type = serializer.validated_data.get('device_type')

            # removing the privious device fingerprint
            try:
                old_device_fingerprint = User.objects.filter( device_id = device_id  )
                for i in old_device_fingerprint:
                    i.device_id = 'null'
                    i.save()

                # saving a new record for the device id 
                user_device_fingerprint = User.objects.get( email = request.user.email )
                user_device_fingerprint.device_id = device_id
                user_device_fingerprint.device_type = device_type
                user_device_fingerprint.save()

                return Response({'status':'success','message':'device id has been updated successfully','device_id':device_id}, status=status.HTTP_201_CREATED)

            except User.DoesNotExist:
                # getting user details and device fingerprint
                user_device_fingerprint = User.objects.get( email = request.user.email )
                user_device_fingerprint.device_id = device_id
                user_device_fingerprint.device_type = device_type
                user_device_fingerprint.save()

                return Response({'status':'success','message':'user device id is been updated successfully','device_id':device_id}, status=status.HTTP_201_CREATED)
            

        return Response(serializer.errors,  status=status.HTTP_400_BAD_REQUEST)


class BusinessProfileView (ListCreateAPIView ):
    permission_classes = [ IsAuthenticated, KOKPermission , KOKMerchantOnly ]
    serializer_class = BusinessProfileSerilizer
    queryset = BusinessProfile.objects.all()

    def list (self, request, *args, **kwargs):
        business_info = self.get_queryset().get ( user = request.user , active = True)
        serializer = self.get_serializer(business_info)
        return Response( serializer.data )

    def create (self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            if BusinessProfile.objects.filter( user = request.user ):
                return Response({'status': 'error', 'message':'user has created a business account', 'data':'null'}, status=status.HTTP_400_BAD_REQUEST)

            business_category = serializer.validated_data.get('business_category')
            serializer.save(user = request.user , active = True , business_category = '' )

            for category in business_category:
                if category.get("category" ) is not None:
                    business_categorys = int( category.get("category" ) )
                    user_category = Category.objects.get ( id = business_categorys )
                    user_business = BusinessProfile.objects.get ( user = request.user , active = True)
                    user_business.business_category.add(user_category) 
 
            merchant_account = User.objects.get( id = request.user.id )
            merchant_account.merchant_business_name = serializer.validated_data.get('business_name')
            merchant_account.save()

            return Response({'status': 'success', 'message':'merchant business profile has been created successfully', 'data': serializer.data}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors,  status=status.HTTP_400_BAD_REQUEST)



class BusinessProfileEditView ( RetrieveUpdateDestroyAPIView ):
    permission_classes = [ IsAuthenticated, KOKPermission , KOKMerchantOnly ]
    serializer_class = BusinessProfileSerilizer
    queryset = BusinessProfile.objects.all()
    lookup_field = "id"
    lookup_value_regex = "[0-9a-fA-F]{8}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{12}"
  


class KroonFQAView (ListAPIView):
    permission_classes = [ AllowAny, KOKPermission ]
    serializer_class = KroonFQASerializer
    
    def get(self, request, *args, **kwargs):
        fqa = KroonFQA.objects.all()
        serializer = self.serializer_class(fqa, many=True)

        return Response({'status':'success','message':'list of FAQs fetched successfully', 'data':serializer.data}, status=status.HTTP_200_OK)


class KioskFQAView (ListAPIView):
    permission_classes = [ AllowAny, KOKPermission ]
    serializer_class = KioskFQASerializer

    def get(self, request, *args, **kwargs):
        fqa = KioskFAQ.objects.all()
        serializer = self.serializer_class(fqa, many=True)

        return Response({'status':'success','message':'list of FAQs fetched successfully', 'data':serializer.data}, status=status.HTTP_200_OK)


class DeviceFringerprintView (CreateAPIView):
    permission_classes = [ IsAuthenticated, KOKPermission ]
    serializer_class = UpdateUserDeviceInfoSerializer
    
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            device_fingerprint = serializer.validated_data.get('device_fingerprint')
            device_type = serializer.validated_data.get('device_type')
            app_version = serializer.validated_data.get('app_version')
            
            # removing the privious device fingerprint
            old_device = User.objects.filter( device_fingerprint = device_fingerprint  )
            for i in old_device:
                i.device_fingerprint = 'null'
                i.save()
                    
            # getting user details and device fingerprint
            user_device_fingerprint = User.objects.get( email = request.user.email )
            user_device_fingerprint.device_fingerprint = device_fingerprint
            user_device_fingerprint.device_type = device_type
            user_device_fingerprint.app_version = app_version
            user_device_fingerprint.save()

            return Response({'status':'success','message':'device finger print has been updated successfully','device_id':device_fingerprint}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors,  status=status.HTTP_400_BAD_REQUEST)


class DeleteMyAccount (APIView):
    permission_classes = [IsAuthenticated, KOKPermission]

    def post(self, request, *args, **kwargs):
        
        # # deleting the user record
        delete_user_account = Delete_Accounts()
        response_data = delete_user_account.kiosk_delete_account(self.request.user , self.request.user.id)
     
        return Response({'status':'success','message':'account has been deleted successfully'}, status=status.HTTP_201_CREATED)     


class SwitchAccountMerchant (APIView):
    permission_classes = [IsAuthenticated, KOKPermission]

    def post(self, request, *args, **kwargs):
        # switching to a merchant account
        switch_merchant_account = User.objects.get( id = request.user.id)
        switch_merchant_account.account_type = "merchant"
        switch_merchant_account.save()
        # assiginig the basic subscription plan 
        plan = Subscription_Plan.objects.get( default_plan = True )
        migrate_plan = Merchant_Subcribers()
        migrate_plan.user = self.request.user
        migrate_plan.plan = plan
        migrate_plan.start_date = timezone.now()
        migrate_plan.end_date = datetime.now()+timedelta( days = 30 )
        migrate_plan.active = True
        migrate_plan.save()
        
        return Response({'status':'success','message':'your personal account has been switched to merchant account successfully.'}, status=status.HTTP_201_CREATED)


class SwtichBusinessAccounts (APIView):
    permission_classes = [IsAuthenticated, KOKPermission]

    def get(self, request, *args, **kwargs):
        business_id = kwargs.get('id')
        # updating the previously saved business accounts
        try:
            BusinessProfile.objects.get( user = request.user , id = business_id )
            business_account = BusinessProfile.objects.get( user = request.user , active = True)
            business_account.active = False
            business_account.save()
        except BusinessProfile.DoesNotExist:
            return Response({'status': 'error', 'message':'user havent created a business account or id incorrect',}, status=status.HTTP_404_NOT_FOUND)

        # switching to a business account
        switch_business_account = BusinessProfile.objects.get(user = request.user , id = business_id )
        switch_business_account.active = True
        switch_business_account.save()
        return Response({'status':'success','message':'the following business account has been updated to default'}, status=status.HTTP_201_CREATED)


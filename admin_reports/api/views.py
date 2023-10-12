import contextlib

from django.http.response import Http404
from django.db.models import Q
from drf_yasg.utils import swagger_auto_schema

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny

from kroon.users.pagination import StandardResultsSetPagination
from helpers.common.security import KOKPermission
from kroon.users.models import User
from admin_reports.models import AdminPushNotifications
from admin_reports.task import device_push_notification
from admin_reports.permissions import IsBlekieAndEtransac
from e_learning.models import Kiosk_E_Learning , App_Survey


from transactions.models import (
    Transactions, 
    KroonTokenTransfer, 
    KroonTokenRequest, 
    UserRequestToken
    )
from kroon.users.api.serializers import UserDetailsSerializer
from rest_framework.mixins import (
    ListModelMixin,
    RetrieveModelMixin,
    DestroyModelMixin,
    CreateModelMixin
)
from rest_framework.viewsets import GenericViewSet
from .serializers import (
    UserListSerializers, 
    TransactionsListSerializers , 
    TransactionDetailsSerializers,
    AdminPushNotificationsSerializer,
    NotificationInfo,
    ELearningSerializers,
    ElearningInfo
    )





class AllUserListView(
    RetrieveModelMixin,
    ListModelMixin,
    GenericViewSet
    ):
    """
    Get all Users 

    This endpoint allows you to get all users registered in kroon and kiosk
    """
    permission_classes = [
        IsAuthenticated,
        KOKPermission,
        IsBlekieAndEtransac,
        ]
    lookup_field = "wallet_id"
    serializer_class = UserListSerializers
    queryset = User.objects.select_related('country_of_residence','country_province','on_boarding_user', 'government_organization_name','bank_details').filter(Q(country_of_residence__iso2 = "NG" ) | Q(country_of_residence__iso2 = "GH") ) #getting the full list of Nigerians and ghana users
    pagination_class = StandardResultsSetPagination

    def get_object(self, queryset=None):
        return User.objects.filter(wallet_id=self.kwargs["wallet_id"]).first()

    @swagger_auto_schema(
        tags=['Admin Reports'],  # Add your desired tag(s) here
        operation_summary="All User",
        operation_description="Endpoints retrieves the list of registered users both on kroon and kiosk.",
    )
    def list(self, request, *args, **kwargs):
        return super(AllUserListView, self).list(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=['Admin Reports'],  # Add your desired tag(s) here
        operation_summary="Get A User",
        operation_description="Retrieve the information of a user by passed Wallet Id.",
    )
    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
        except Exception as e:
            return Response({"message": str(e)})
        else:
            # any additional logic
            serializer = UserDetailsSerializer(instance)

            return Response(serializer.data)



class TransactionListView(
    RetrieveModelMixin,
    ListModelMixin,
    GenericViewSet
    ):
    """
    Get all transactions 

    This endpoint allows you to get all transactions been made by the users in kroon and kiosk

    A transaction details consists of the following TOPUP, KROON TRANSFER , WITHDRAWAL

    """
    permission_classes = [
        IsAuthenticated,
        KOKPermission,
        IsBlekieAndEtransac,
        ]
    lookup_field = "transactional_id"
    serializer_class = TransactionsListSerializers
    queryset = Transactions.objects.all()
    pagination_class = StandardResultsSetPagination

    def get_object(self, queryset=None):
        return Transactions.objects.filter(transactional_id=self.kwargs["transactional_id"]).first()

    @swagger_auto_schema(
        tags=['Admin Reports'],  # Add your desired tag(s) here
        operation_summary="All Transactions",
        operation_description="Endpoints retrieves the list of Transactions.",
    )
    def list(self, request, *args, **kwargs):
        return super(TransactionListView, self).list(request, *args, **kwargs)


    @swagger_auto_schema(
        tags=['Admin Reports'],  # Add your desired tag(s) here
        operation_summary="Get Transaction",
        operation_description="Retrieve the information of Transaction by passed Id.",
    )
    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
        except Exception as e:
            return Response({"message": str(e)})
        else:
            # any additional logic
            serializer = TransactionDetailsSerializers(instance)

            return Response(serializer.data)
        

class PushNotificationViewSet(
    RetrieveModelMixin,
    ListModelMixin,
    GenericViewSet,
    DestroyModelMixin,
    CreateModelMixin
    ):
    """
    Send Push Notification 

    This endpoints allows you to send push notifications to kroon and kiosk users , using the notification ID to get and delete the notification that is stored

    """
 
    permission_classes = [
        IsAuthenticated,
        KOKPermission,
        IsBlekieAndEtransac,
        ]
    lookup_field = "id"
    serializer_class = AdminPushNotificationsSerializer
    queryset = AdminPushNotifications.objects.all()
    pagination_class = StandardResultsSetPagination

    def get_object(self, queryset=None):
        return AdminPushNotifications.objects.get(id=self.kwargs["id"])
    
    # Post Push Notifications
    @swagger_auto_schema(
        tags=['Admin Reports'],  # Add your desired tag(s) here
        operation_summary="Post Push Notifications",
        operation_description="Create and push Push Notifications.",
    )
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # sendout push notification
        device_push_notification(serializer = serializer)
        self.perform_create( serializer )
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
    def perform_create(self, serializer):
        serializer.save(publisher = self.request.user) # save the publisher
    
    
    # All Push Notifications
    @swagger_auto_schema(
        tags=['Admin Reports'],  # Add your desired tag(s) here
        operation_summary="All Push Notifications",
        operation_description="Endpoints retrieves the list of Push Notifications.",
    )
    def list(self, request, *args, **kwargs):
        return super(PushNotificationViewSet, self).list(request, *args, **kwargs)
    
    # Get Push Notifications
    @swagger_auto_schema(
        tags=['Admin Reports'],  # Add your desired tag(s) here
        operation_summary="Get Push Notifications",
        operation_description=" Retrieve the information of a push notification by passed Id.",
    )
    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
        except Exception as e:
            return Response({"message": str(e)})
        else:
            # any additional logic
            serializer = NotificationInfo(instance)
            return Response(serializer.data)
    
    # Delete Push Notifications
    @swagger_auto_schema(
        tags=['Admin Reports'],  # Add your desired tag(s) here
        operation_summary="Delete Push Notifications",
        operation_description="This deletes a push notification using the push notification ID",
    )
    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
        except Exception as e:
            return Response({"message": str(e)})
        else:
            self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    
    

class ELearningViewSet(
    RetrieveModelMixin,
    ListModelMixin,
    GenericViewSet,
    DestroyModelMixin,
    CreateModelMixin
    ):
    """
    E-Learning  

    This endpoints allows you to publish tutorials videos to kroon and kiosk users , using each video ID to get and delete the any published clip that is stored to guild the users on how to use the application.

    """
 
    permission_classes = [
        IsAuthenticated,
        KOKPermission,
        IsBlekieAndEtransac,
        ]
    lookup_field = "id"
    serializer_class = ELearningSerializers
    queryset = Kiosk_E_Learning.objects.all()
    pagination_class = StandardResultsSetPagination

    def get_object(self, queryset=None):
        return Kiosk_E_Learning.objects.get(id=self.kwargs["id"])
    
    # Post Push Notifications
    @swagger_auto_schema(
        tags=['Admin Reports'],  # Add your desired tag(s) here
        operation_summary="Upload Elearning Clip",
        operation_description="Create and uploads the elearning clip.",
    )
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True) 
        self.perform_create( serializer )
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
    # def perform_create(self, serializer):
    #     serializer.save(publisher = self.request.user) # save the publisher
    
    
    # All Push Notifications
    @swagger_auto_schema(
        tags=['Admin Reports'],  # Add your desired tag(s) here
        operation_summary="List of Elearning clips",
        operation_description="Endpoints retrieves the list of kroon and kiosk tutorial clips which is known as elearning.",
    )
    def list(self, request, *args, **kwargs):
        return super(ELearningViewSet, self).list(request, *args, **kwargs)
    
    # Get Push Notifications
    @swagger_auto_schema(
        tags=['Admin Reports'],  # Add your desired tag(s) here
        operation_summary="Get elearning clip",
        operation_description=" Retrieve the information of a video by passed Id.",
    )
    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
        except Exception as e:
            return Response({"message": str(e)})
        else:
            # any additional logic
            serializer = ElearningInfo(instance)
            return Response(serializer.data)
    
    # Delete Push Notifications
    @swagger_auto_schema(
        tags=['Admin Reports'],  # Add your desired tag(s) here
        operation_summary="Delete Elearning Video",
        operation_description="This deletes a elearning Video using the elearning VideoID",
    )
    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
        except Exception as e:
            return Response({"message": str(e)})
        else:
            self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
    


    


    


        

# this is recorded to be a sandbox to the original data and records
# sandbox starts here ----------------------------------------------------------------
# sandbox starts here ----------------------------------------------------------------
# sandbox starts here ----------------------------------------------------------------
# sandbox starts here ----------------------------------------------------------------

class TotalTransactions(GenericViewSet):
    """
    Get total of all transactions 

    This endpoint allows you to get all transactions been made by the users in kroon and kiosk

    A transaction details consists of the following TOPUP, KROON TRANSFER , WITHDRAWAL

    """
    permission_classes = [
        IsAuthenticated,
        KOKPermission,
        IsBlekieAndEtransac,
        ]
    queryset = Transactions.objects.all()

    @swagger_auto_schema(
        tags=['Admin Reports'],  # Add your desired tag(s) here
        operation_summary="Total Transaction",
        operation_description=" *SANDBOX* // this shows the amount of all transactions to compare last year record",
    )
    def list(self, request, *args, **kwargs):
        data = {
            'local_currency': 'NGN',
            'total_amount': 398090,
            'transaction_percentage':'+18.20',
            'last_year_amount':1283729,
            'total_percentage':'73'
        }

        return Response(data , status=status.HTTP_200_OK)
    

class TotalWalletValue(GenericViewSet):
   
    permission_classes = [
        IsAuthenticated,
        KOKPermission,
        IsBlekieAndEtransac,
        ]
    queryset = Transactions.objects.all()

    @swagger_auto_schema(
        tags=['Admin Reports'],  # Add your desired tag(s) here
        operation_summary="Total Wallet Value",
        operation_description=" *SANDBOX* // this shows the amount of all wallet value to compare last year record",
    )
    def list(self, request, *args, **kwargs):
        data = {
            'local_currency': 'NGN',
            'total_amount': 4557690,
            'transaction_percentage':'+11.20',
            'last_year_amount':1983729,
            'total_percentage':'90'
        }

        return Response(data , status=status.HTTP_200_OK)
    


class TotalPayouts(GenericViewSet):
   
    permission_classes = [
        IsAuthenticated,
        KOKPermission,
        IsBlekieAndEtransac,
        ]
    queryset = Transactions.objects.all()

    @swagger_auto_schema(
        tags=['Admin Reports'],  # Add your desired tag(s) here
        operation_summary="Total Payouts",
        operation_description=" *SANDBOX* // this shows the amount of all payouts to compare last year record",
    )
    def list(self, request, *args, **kwargs):
        data = {
            'local_currency': 'NGN',
            'total_amount': 9157690,
            'transaction_percentage':'+9.20',
            'last_year_amount':1983729,
            'total_percentage':'87'
        }

        return Response(data , status=status.HTTP_200_OK)
    

class TotalEwallets(GenericViewSet):
   
    permission_classes = [
        IsAuthenticated,
        KOKPermission,
        IsBlekieAndEtransac,
        ]
    queryset = Transactions.objects.all()

    @swagger_auto_schema(
        tags=['Admin Reports'],  # Add your desired tag(s) here
        operation_summary="Total E-Wallets",
        operation_description=" *SANDBOX* // this shows the amount of all E wallets to compare last year record",
    )
    def list(self, request, *args, **kwargs):
        data = {
            'total_wallets': 8201,
            'last_year_wallets':4903,
        }

        return Response(data , status=status.HTTP_200_OK)
    


class TotalMerchants(GenericViewSet):
   
    permission_classes = [
        IsAuthenticated,
        KOKPermission,
        IsBlekieAndEtransac,
        ]
    queryset = Transactions.objects.all()
    lookup_value_regex = "[0-9a-fA-F]{8}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{12}"

    @swagger_auto_schema(
        tags=['Admin Reports'],  # Add your desired tag(s) here
        operation_summary="Total Merchants",
        operation_description=" *SANDBOX* // this shows the amount of all registered merchants to compare last year record",
    )
    def list(self, request, *args, **kwargs):
        data = {
            'total_merchants': 8901,
            'last_year_merchants':2793,
        }

        return Response(data , status=status.HTTP_200_OK)
    


class CrossBorderTransfer(GenericViewSet):
   
    permission_classes = [
        AllowAny,
        # KOKPermission,
        # IsBlekieAndEtransac,
        ]
    queryset = Transactions.objects.all()
    lookup_value_regex = "[0-9a-fA-F]{8}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{12}"

    @swagger_auto_schema(
        tags=['Admin Reports'],  # Add your desired tag(s) here
        operation_summary="Cross Border Transfer",
        operation_description=" *SANDBOX* // this shows the amount of all cross border transfer to compare last year record ",
    )
    def list(self, request, *args, **kwargs):
        data = {
            'local_currency': 'NGN',
            'total_cross_border_transfers': 453928,
            'last_year_cross_border_transfers':36392124,
        }

        return Response(data , status=status.HTTP_200_OK)
    

class DailyAverage(GenericViewSet):
   
    permission_classes = [
        IsAuthenticated,
        KOKPermission,
        IsBlekieAndEtransac,
        ]
    queryset = Transactions.objects.all()

    @swagger_auto_schema(
        tags=['Admin Reports'],  # Add your desired tag(s) here
        operation_summary="Daily Average",
        operation_description=" *SANDBOX* // this shows the amount of all daily average to compare yesterday record",
    )
    def list(self, request, *args, **kwargs):
        response = {
            'local_currency': 'NGN',
            'transaction_volume': 23678,
            'transaction_volume_per': '+17,82',
            'yesterday_transaction_volume':12984,
            'transaction_value': 40350,
            'transaction_value_per': '+13,20',
            'yesterday_transaction_value':20341,
        }

        return Response(data=response , status=status.HTTP_200_OK)
    

class TotalActiveMerchants(GenericViewSet):
   
    permission_classes = [
        IsAuthenticated,
        KOKPermission,
        IsBlekieAndEtransac,
        ]
    queryset = Transactions.objects.all()

    @swagger_auto_schema(
        tags=['Admin Reports'],  # Add your desired tag(s) here
        operation_summary="Daily Average",
        operation_description=" *SANDBOX* // this shows the total count of all merchants both the new and loss merchants on the platform ",
    )
    def list(self, request, *args, **kwargs):
        data = {
            'new_merchants':10456,
            'loss_merchants':2450
        }

        return Response(data , status=status.HTTP_200_OK)
    


class TopPerformingRegions(GenericViewSet):
  
    permission_classes = [
        IsAuthenticated,
        KOKPermission,
        IsBlekieAndEtransac,
        ]
    queryset = Transactions.objects.all()

    @swagger_auto_schema(
        tags=['Admin Reports'],  # Add your desired tag(s) here
        operation_summary="Top Performing Regions",
        operation_description=" *SANDBOX* // this shows the list of top performing regions",
    )
    def list(self, request, *args, **kwargs):
        data = [
            {
                'region': 'Lagos',
                'transaction_value': 29321490,
            },
            {
                'region': 'Abuja',
                'transaction_value': 19300250,
            },
            {
                'region': 'Kano',
                'transaction_value': 17322822,
            }
        ]

        return Response(data , status=status.HTTP_200_OK)
    


class GlobalOverview(GenericViewSet):
   
    permission_classes = [
        IsAuthenticated,
        KOKPermission,
        IsBlekieAndEtransac,
        ]
    queryset = Transactions.objects.all()

    @swagger_auto_schema(
        tags=['Admin Reports'],  # Add your desired tag(s) here
        operation_summary="Top Performing Regions",
        operation_description=" *SANDBOX* // this shows the list of top performing regions",
    )
    def list(self, request, *args, **kwargs):
        data = [
            {
                'region': 'Lagos',
                'local_currency': 'NGN',
                'total_wallets': 2046,
                'wallet_value': 893876,
                'payout_value': 45723,
                'total_merchants': 2046,
                'active_merchants': 2046,
                'merchants_revenue': 29321490,
                'inventory_on_hand': 9321490,
                'avg_transactions': 60,
            },
            {
                'region': 'FCT Abuja',
                'local_currency': 'NGN',
                'total_wallets': 2046,
                'wallet_value': 893876,
                'payout_value': 45723,
                'total_merchants': 2046,
                'active_merchants': 2046,
                'merchants_revenue': 29321490,
                'inventory_on_hand': 9321490,
                'avg_transactions': 60,
            },
            {
                'region': 'Oyo',
                'local_currency': 'NGN',
                'total_wallets': 2046,
                'wallet_value': 893876,
                'payout_value': 45723,
                'total_merchants': 2046,
                'active_merchants': 2046,
                'merchants_revenue': 29321490,
                'inventory_on_hand': 9321490,
                'avg_transactions': 60,
            },
            {
                'region': 'Abia',
                'local_currency': 'NGN',
                'total_wallets': 2046,
                'wallet_value': 893876,
                'payout_value': 45723,
                'total_merchants': 2046,
                'active_merchants': 2046,
                'merchants_revenue': 29321490,
                'inventory_on_hand': 9321490,
                'avg_transactions': 60,
            },
           
        ]

        return Response(data , status=status.HTTP_200_OK)
    

# this is recorded to be a sandbox to the original data and records
# sandbox end here ----------------------------------------------------------------

    
    

        

    
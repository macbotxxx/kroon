import contextlib
from rest_framework import status
from django.http.response import Http404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from kroon.users.pagination import StandardResultsSetPagination
from helpers.common.security import KOKPermission
from admin_reports.permissions import IsBlekieAndEtransac
from django.db.models import Q
from drf_yasg.utils import swagger_auto_schema
from kroon.users.models import User
from transactions.models import Transactions, KroonTokenTransfer , KroonTokenRequest, UserRequestToken
from kroon.users.api.serializers import UserDetailsSerializer
from rest_framework.mixins import (
    ListModelMixin,
    RetrieveModelMixin,
)
from rest_framework.viewsets import GenericViewSet
from .serializers import UserListSerializers, TransactionsListSerializers , TransactionDetailsSerializers





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
        

# this is recorded to be a sandbox to the original data and records
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
    """
    Get total of all wallet value 

    this endpoint shows the list of all wallets value compare to last year

    """
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
    """
    Get total of all payouts 

    this endpoint shows the list of all payouts compare to last year

    """
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
    """
    Get total of all E wallet  

    this endpoint shows the list of all E wallets compare to last year

    """
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
    """
    Get total registered merchants  

    this endpoint shows the list of all registered merchants compare to last year

    """
    permission_classes = [
        IsAuthenticated,
        KOKPermission,
        IsBlekieAndEtransac,
        ]
    queryset = Transactions.objects.all()

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
    """
    Get total cross border transfer 

    this endpoint shows the list of all cross border transfer compare to last year

    """
    permission_classes = [
        IsAuthenticated,
        KOKPermission,
        IsBlekieAndEtransac,
        ]
    queryset = Transactions.objects.all()

    @swagger_auto_schema(
        tags=['Admin Reports'],  # Add your desired tag(s) here
        operation_summary="Cross Border Transfer",
        operation_description=" *SANDBOX* // this shows the amount of all cross border transfer to compare last year record",
    )
    def list(self, request, *args, **kwargs):
        data = {
            'local_currency': 'NGN',
            'total_cross_border_transfers': 453928,
            'last_year_cross_border_transfers':36392124,
        }

        return Response(data , status=status.HTTP_200_OK)
    

class DailyAverage(GenericViewSet):
    """
    Get the daily average

    this endpoint shows the list of all daily average compare to last year

    """
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
        data = {
            'local_currency': 'NGN',
            'transaction_volume': 23678,
            'transaction_volume_per': '+17,82',
            'yesterday_transaction_volume':12984,
            'transaction_value': 40350,
            'transaction_value_per': '+13,20',
            'yesterday_transaction_value':20341,
        }

        return Response(data , status=status.HTTP_200_OK)
    

class TotalActiveMerchants(GenericViewSet):
    """
    Get the number of merchants

    this endpoint shows the total count of all merchants both the new and loss merchants on the platform

    """
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
    """
    Get the list of top performing regions

    this endpoint shows the total of top performing regions

    """
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
    """
    Get the list of top performing regions

    this endpoint shows the total of top performing regions

    """
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
    


    
    

        

    
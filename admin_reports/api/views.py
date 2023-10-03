import contextlib
from rest_framework import status
from django.http.response import Http404
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from kroon.users.pagination import StandardResultsSetPagination
from helpers.common.security import KOKPermission
from admin_reports.permissions import IsBlekieAndEtransac
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
    queryset = User.objects.all()
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
        

    
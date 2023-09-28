import contextlib
import logging
from rest_framework import status
from django.http.response import Http404
from rest_framework.generics import ListAPIView , RetrieveAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from kroon.users.pagination import StandardResultsSetPagination
from helpers.common.security import KOKPermission
from admin_reports.permissions import IsBlekieAndEtransac, EtransacAdmin

from kroon.users.models import User
from transactions.models import Transactions, KroonTokenTransfer , KroonTokenRequest, UserRequestToken
from kroon.users.api.serializers import UserDetailsSerializer
from .serializers import UserListSerializers, TransactionsListSerializers
from rest_framework.mixins import (
    ListModelMixin,
    RetrieveModelMixin,
)
from rest_framework.viewsets import GenericViewSet




class UserListView(ListAPIView):
    permission_classes = [
        IsAuthenticated,
        KOKPermission,
        IsBlekieAndEtransac,
        ]
    serializer_class = UserListSerializers
    queryset = User.objects.all()
    pagination_class = StandardResultsSetPagination


class TransactionListView(
    RetrieveModelMixin,
    ListModelMixin,
    GenericViewSet
    ):
    """
    Create a Budget Item

    This endpoint allows you to create a new Budget Item by an authenticated user.

    A budget item can be either an INCOME or EXPENSE.

    **Adding an Income**:
    When adding an income, quantity is not required.

    **Adding an Expense**:
    When adding an income, quantity is optional and defaults to 1. 
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

    def list(self, request, *args, **kwargs):
        """
        All Transaction

        Endpoints retrieves the list of Transactions.

        tags['Admin Report']
        """
        return super(TransactionListView, self).list(request, *args, **kwargs)


    def retrieve(self, request, *args, **kwargs):
        """
        Get Transaction

        Retrieve the information of Transaction by passed Id.

        tags['Admin Report']
        """
        try:
            instance = self.get_object()
        except Exception as e:
            return Response({"message": str(e)})
        else:
            # any additional logic
            serializer = self.get_serializer(instance)

            return Response(serializer.data)
        

    
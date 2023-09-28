import datetime
import time
import os
# from twilio.rest import Client
from django.db.models import Q
from rest_framework.generics import CreateAPIView, ListAPIView , GenericAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status, serializers
from drf_yasg.utils import swagger_auto_schema
from kroon.users.models import User
from helpers.common.security import KOKPermission

from .serializers import AdSerializer
from ads.models import Ads

class AdsView (ListAPIView):
    permissions_classes = [ IsAuthenticated , KOKPermission ]
    serializer_class = AdSerializer
    queryset = Ads.objects.all()
    

    @swagger_auto_schema(
            responses={
                404: 'platform does not exist', 
                status.HTTP_200_OK: AdSerializer },
            operation_summary="kroon Ads",
            operation_description="The kroon ad section shows the list of published ads according to the platform ",
            tags=["Kroon Ads"]
            )
    def get (self, request, *args, **kwargs):
        platform = kwargs.get('platform')

        active_ads = self.get_queryset().filter( Q( platform = platform) | Q( platform = "all_the_above") ,ad_country = self.request.user.country_of_residence , active = True )
        
        serializer = self.get_serializer(active_ads , many = True)
        return Response({'status':'success','message':'list of ads fetched successfully', 'data':serializer.data}, status=status.HTTP_201_CREATED)
    

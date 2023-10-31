import json
import requests
from platform import platform
from rest_framework.generics import ListAPIView , GenericAPIView
from rest_framework.viewsets import GenericViewSet

from rest_framework.mixins import ListModelMixin , CreateModelMixin
from rest_framework import status
from rest_framework.permissions import IsAuthenticated , AllowAny
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema


from django.conf import settings
from django.db.models import Q

from notifications.models import NewsFeed
from notifications.tasks import mobile_push_notification, service_push_notification
from .serializers import NewsFeedSerializer, GeneralNotificationSerializer
from rest_framework.views import APIView

from helpers.common.security import KOKPermission
FCM_SERVER_KEY = settings.KIOSK_FCM_SERVER_KEY


class NewsFeedView(ListAPIView):
    permission_classes = [ IsAuthenticated, KOKPermission ]
    serializer_class = NewsFeedSerializer
    
    def get(self, request, *args, **kwargs):
        platform = kwargs.get('platform')
        news_feed = NewsFeed.objects.filter( Q(platform=platform) | Q(platform = "all_the_above" ) ,news_feed_country = request.user.country_of_residence)
        serializer = self.serializer_class(news_feed, many=True)

        return Response({'status':'success','message':'this is the list of all active news feed', 'data':serializer.data}, status = status.HTTP_200_OK)



class Test_Push_Notifications(APIView):
    permission_classes = [ AllowAny ]

    def get (self, request , *args, **kwargs ):
        device_id = kwargs.pop('device_id', None)
        title = "Testing push notification "
        body_message="Testing device can be carried out from the testing endpoint"
        platform = "kiosk"
        device_type = "phone"

        mobile_push_notification.delay( device_id = device_id , title = title , body_message = body_message , platform = platform , device_type = device_type)
       
        return Response({'status':'success','message':'notifications', 'data':''}, status = status.HTTP_200_OK)
    


class SimulatePushNotificationsNewsfeed(APIView):
    permission_classes = [ AllowAny ]

    def get (self, request , *args, **kwargs ):
        device_id = kwargs.pop('device_id', None)
        title = "Testing push notification "
        body_message="Testing newsfeed notifications can come in with a data structure that has the link in it"
        platform = "kiosk"
        device_type = "phone"
        notification_type = "newsfeed"

        mobile_push_notification.delay(
             device_id = device_id , 
             title = title , 
             body_message = body_message , 
             platform = platform , 
             device_type = device_type , 
             notification_type = notification_type
             )
       
        return Response({'status':'success','message':'notifications', 'data':''}, status = status.HTTP_200_OK)
    


class GeneralNotificationViewSet(CreateModelMixin, GenericViewSet):
    permission_classes = [
        IsAuthenticated,
        KOKPermission,
        ]
    queryset = NewsFeed.objects.all()
    serializer_class = GeneralNotificationSerializer
   
    # Post Uploaded Tutorial videos
    @swagger_auto_schema(
        tags=['Admin Reports'],  # Add your desired tag(s) here
        operation_summary="General Push Notification",
        operation_description="Create a general notification that will be sent out to all users ",
    )
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True) 
        service_push_notification.delay(body_message = serializer.data)
        return Response({'message':'push notification sent' ,'data':serializer.data}, status=status.HTTP_201_CREATED)
        

        
from django.urls import path
from . import views

urlpatterns = [
    path('news-feed/<str:platform>/', views.NewsFeedView.as_view(), name='news-feed'),
    path('push-notification-test/<str:device_id>/', views.Test_Push_Notifications.as_view(), name='push_notifciations'),
    path('newsfeed-notification-test/<str:device_id>/', views.SimulatePushNotificationsNewsfeed.as_view(), name='newsfeed_notification'),
]
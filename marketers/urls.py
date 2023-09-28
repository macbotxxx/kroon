from django.urls import path
from . import views

app_name = 'marketers'

urlpatterns = [
    path('', views.marketer_index, name='marketer_index'),
    path('users-index/', views.users_index, name='users_index'),
    path('user-details/<str:user_id>/', views.user_details, name='user_details'),
    path('general-push-notifications/', views.general_push_notifications, name='general_push_notifications'),
    path('general-email-notifications/', views.general_email_notification, name='general_email_notification'),
    path('per-country-email-notifications/', views.general_email_notification_per_country, name='general_email_notification_per_country'),
    path('push-notifications-per-country/', views.push_notification_per_country, name='push_notification_per_country'),
    path('list-of-active-users/', views.list_of_all_active_users, name='list_of_active_users'),
    
    path('personal-push-notifications/<str:user_id>/', views.personal_push_notifications, name='personal_push_notifications'),
    path('personal-email-notifications/<str:user_id>/', views.send_personal_email, name='personal_email_notifications'),

    path('statement/', views.marketer_statment, name='marketer_statement'),

    # ads and news feeds
    path('general-ads/', views.general_ads, name='general_ads'),
    path('general-news-feed/', views.general_news_feed_views, name='general_news_feed_views'),

]
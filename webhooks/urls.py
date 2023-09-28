from django.urls import path
from . import views

urlpatterns = [

    path('push-webhook/', views.flutter_webhook, name='push-webhook'),
    path('push-webhook-pay/', views.paystack_webhook, name='push_webhook_pay'),
    path('paypal-webhook-pay/', views.paypal_webhook, name='paypal_webhook_pay'),
    path('kyc-update/', views.kyc_notification, name='kyc_notification'),

]
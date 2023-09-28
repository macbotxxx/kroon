from django.urls import path
from . import views

urlpatterns = [

    path('topup-payment/', views.TopUpPaymentView.as_view(), name='topup_payment'),
    path('topup-payment-verification/', views.TopUpPaymentVerification.as_view(), name='topup_payment_verification'),
    path('cancel-payment/', views.CancelPaymentRequest.as_view(), name='cancel-Payment'),
    
]
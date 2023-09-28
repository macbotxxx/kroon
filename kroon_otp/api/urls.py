from django.urls import path
from . import views

urlpatterns = [
    path('email-opt/', views.EmailOpt.as_view(), name='email-opt'),
    path('email-test-func/', views.EmailFuncTest.as_view(), name='email-test'),
    path('verify-otp/', views.OTPVerification.as_view(), name='verify_otp'),

]
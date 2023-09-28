from django.urls import path
from . import views
# from rest_auth.views import PasswordResetConfirmView

urlpatterns = [
    
    path('create-user-address/', views.UserAddressView.as_view(), name='create-user-address'),
    path('update-user-address/<str:id>/', views.UpdateUserAddressView.as_view(), name='update-user-address'),
    path('create-user-bank-details/', views.UserBankDetailsView.as_view(), name='create-user-bank'),
   
    path('terms-and-conditions/<str:platform>/', views.KroonTermsAndConditionsView.as_view(), name='terms_and_conditions'),
    path('email-forget-password/', views.ForgetPasswordEmailNotificationView.as_view(), name='email_forget_password'),
    path('forgot-password/', views.ForgotPasswordSerilizerView.as_view(), name='forgot_password'),
    path('device-id/', views.UpdateDeviceId.as_view(), name='device_id'),

    path('business-profile/', views.BusinessProfileView.as_view(), name='business-profile'),
    path('business-profile/<str:id>/', views.BusinessProfileEditView.as_view(), name='business-profile-update'),

    path('kroon-policy/<str:platform>/', views.PolicyAndConditionView.as_view(), name='kroon_policy'),
    path('kroon-fqas/', views.KroonFQAView.as_view(), name='kroon_fqa'),
    path('koisk-faqs/', views.KioskFQAView.as_view(), name='kiosk_faqs'),
    path('update-device-fingerprint/', views.DeviceFringerprintView.as_view(), name='update_fingerprint'),
    path('delete-my-account/', views.DeleteMyAccount.as_view(), name='delete_my_account'),
    path('switch-merchant-account/', views.SwitchAccountMerchant.as_view(), name='SwitchAccountMerchant'),
    path('switch-business-account/<str:id>/', views.SwtichBusinessAccounts.as_view(), name='SwtichBusinessAccounts'),
    
]
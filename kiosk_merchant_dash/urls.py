from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
# from account import views as acc_views


urlpatterns = [

    path('email-verification/', views.email_verification , name='email_verification'), 
    path('register-account/', views.registration_merchant , name='registration_merchant'), 
    path('otp-verification/', views.otp_verification , name='otp_verification'), 
    path('login/', auth_views.LoginView.as_view(template_name='account/login.html'), name='login'),

    path('', views.index_page , name='index_page'), 
    path('submit-kyc/', views.kyc_form , name='kyc_form'), 
    path('all-products/', views.all_products , name='all_products'), 
    path('all-sales/', views.all_sales , name='all_sales'), 
    path('delete-sale/<str:product_id>/', views.delete_product , name='delete_product'), 
    
    path('business-analytics/', views.business_analytics , name='business_analytics'), 
    path('account-settings/', views.account_settings , name='account_settings'), 
    path('financial-analytics/', views.financial_analytics , name='financial_analytics'), 
    path('invoice/<str:order_id>/', views.invoice , name='invoice'), 
    path('sale-detail/<str:order_id>/', views.sale_details , name='sale_details'), 
    path('change-password-settings/', views.account_settings_password , name='account_settings_password'), 
    path('language-settings/', views.account_settings_language , name='account_settings_language'), 
    path('theme-color/', views.account_settings_theme , name='account_settings_theme'), 
    path('activate-theme/', views.activate_theme , name='activate_theme'), 
    path('warning/', views.warning , name='warning'), 
    path('delete-my-account/', views.delete_my_account , name='delete_my_account'),
    path('switch-my-account/', views.switchAccountMerchant , name='switch_Account'),
    path('my-business-account/<str:business_id>/', views.switchBusinessAccountMerchant , name='my_business_account'), 



]
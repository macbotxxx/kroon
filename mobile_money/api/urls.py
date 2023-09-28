from django.urls import path
from . import views


urlpatterns = [
    path('network-providers/', views.NetworkProviderView.as_view(), name='network-providers'),
    path('create-mobile-money-account/', views.MobileMobileAccountView.as_view(), name='create-mobile-money-account'),
    path('mobile-topup/', views.MobileMoneyTopUpView.as_view(), name='mobile-top'),
    path('delete-mobile-money-account/', views.DeleteMobileMoneyDetails.as_view(), name='delete-mobile-money-account'),
]
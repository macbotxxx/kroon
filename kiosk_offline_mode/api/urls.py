from django.urls import path
from . import views

urlpatterns = [

    path('network-test/', views.Network_Test.as_view(), name='network_test'),
    path('upload-offline-records/', views.Kiosk_Offline_Checkout.as_view(), name='Kiosk_Offline_Checkout'),
    path('upload-offline-products/', views.Offline_Product_UPload_View.as_view(), name='Offline_Product_UPload_View'),
    path('kroon-app-verison/', views.KroonAPP_Version.as_view(), name='KroonAPP_Version'),
    path('support-email/', views.Customer_Support_Email.as_view(), name='Customer_Support_Email'),
    
]
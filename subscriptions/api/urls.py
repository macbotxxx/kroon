from django.urls import path
from . import views

urlpatterns = [
    path('migrate-plan/', views.Gov_promo_code_view.as_view(), name='gov_promo_code_view'),
    path('inapp-receipt-verification/', views.InAppSubCheckView.as_view(), name='InAppSubCheckView'),
    path('inapp-migrate/', views.Inapp_sub_migrations.as_view(), name='Inapp_sub_migrations'),
    path('obtain-v/', views.Obtain_Cre.as_view(), name='Obtain_Cre'),
    path('merchant-sub-id/', views.MerchantSubID.as_view(), name='merchantSUbid'),
    path('testing/', views.TestEnd.as_view(), name='TestEnd'),
]
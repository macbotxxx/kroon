from django.urls import path
from . import views

urlpatterns = [
    path('gift-kroon/', views.KroonGiftView.as_view(), name='kroon_gift'),
    path('redeem-gift-kroon/', views.RedeemKroonGiftView.as_view(), name='redeem_gift'),
    path('gift-kroon-info/', views.KroonGiftInfoView.as_view(), name='kroon_gift_info'),
]
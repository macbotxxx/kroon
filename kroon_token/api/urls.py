from django.urls import path
from . import views

urlpatterns = [
    path('token-and-vat-rate/', views.FeesAndVatFeesView.as_view(), name ='purchase_token_fee' ),
]
from django.urls import path
from . import views

urlpatterns = [
    path('bank-withdrawal/', views.FlutterWaveWithdrawal.as_view(), name='bank_wothdrawal'),
]
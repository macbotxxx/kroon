from django.urls import path
from . import views


urlpatterns = [

    path('list-of-banks/', views.List_Of_Banks.as_view(), name = 'ListOfBanks'),
    path('account-number-verification/', views.Account_Number_Verification.as_view(), name = 'account_number_verification'),

]
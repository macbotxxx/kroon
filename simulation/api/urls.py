from django.urls import path
from . import views


urlpatterns = [
    path('simulate-accounts/', views.Simulate_Account_View.as_view() , name = 'simulate-account'),
    path('delete-simulate-accounts/', views.Delete_Simulate_Accounts.as_view() , name = 'delete-simulate-account'),
    path('simulate-products/', views.Simulate_Products.as_view() , name = 'simulate-products'),
    path('simulate-users/', views.Create_Users_CSv.as_view() , name = 'simulate-users'),
    path('simulate-sales/<str:period>/', views.Simulate_Sales.as_view() , name = 'simulate-sales'),
    path('create-nasme-promo-codes/', views.GenerateNasmePromoCode.as_view()),

]
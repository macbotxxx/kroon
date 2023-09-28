from django.urls import path
from . import views
app_name = "locations"

urlpatterns = [
    path('countries/', views.CountryListView.as_view(), name='country'),
    path('kiosk-countries/', views.KoiskCountryListView.as_view(), name='kiosk_country'),
    path('user-kroon-verification/', views.User_Country_Kroon_verification.as_view(), name='kroon_verification'),
    path('fire-base/', views.Notifications.as_view(), name='fire-base'),
    path('country-state/<str:country_id>/', views.CountryStates.as_view()),
]
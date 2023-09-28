from django.urls import path
from . import views

app_name = "financial"

urlpatterns = [
    path("", views.home_page, name="home_page_financial"),
    path("analytics/<int:country>/", views.financial_analytics, name="financial_analytics"),
]
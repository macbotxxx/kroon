from django.urls import path
from . import views

urlpatterns = [
    path('list-of-gov-orgs/', views.ListGovOrgs.as_view()),

]
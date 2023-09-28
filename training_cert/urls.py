from django.urls import path
from . import  views

urlpatterns = [
    path('', views.Training_Cert_View, name="training_cert_view"),
    path('cert-list/', views.Cert_list, name="cert_view_list"),
    path('cert-validate/', views.validate_cert, name="validate_cert"),
]
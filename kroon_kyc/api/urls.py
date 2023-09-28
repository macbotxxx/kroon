from django.urls import path
from . import views

urlpatterns = [
    path('submit-kyc/', views.KYCView.as_view(), name='submit-kyc'),
    path('marchant_kyc/', views.MarchantKYCVIEW.as_view(), name='marchant_kyc'),
]
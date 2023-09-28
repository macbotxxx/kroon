from django.urls import path
from . import views 

urlpatterns = [
    path('employee-agreement/', views.BusinessAgreementsView.as_view() , name="Business Agreement"), 
    path('employee-agreement/<str:id>/', views.BusinessAgreementsView.as_view() , name="Business Agreement"), 
    
    path('business-agreements-info/', views.AgreementsInfoView.as_view() , name="agreement_info"), 
    path('business-agreements-info/<str:id>/', views.AgreementsInfoListView.as_view() , name="agreement_info_get"), 

    path('share-agreements/', views.SharesAgreementView.as_view() , name="Share Agreement"),
    path('share-agreements/<str:id>/', views.SharesAgreementListView.as_view() , name="Share Agreement"),

    path('good-and-services-agreements/', views.GoodsAndServicesAgreementView.as_view() , name="Share Agreement"),
    path('good-and-services-agreements/<str:id>/', views.GoodsAndServicesAgreementListView.as_view() , name="Share Agreement"),

    path('loan-agreements/', views.LoanAgreementView.as_view() , name="Share Agreement"),
    path('loan-agreements/<str:id>/', views.LoanAgreementViewListView.as_view() , name="Share Agreement"),

    path('all-agreements/', views.AllAgreementView.as_view() , name="all-Agreement"),


] 
from django.urls import path
from . import views 

urlpatterns = [
    path('business-plan', views.BusinessPlanView.as_view(), name='business-plan'),
    path('business-plan/<str:id>/', views.BusinessPlanDeleteView.as_view(), name='business-plan-delete'),
    path('business-plan-detials/<str:report_id>/', views.GeneratedBusinessPlanView.as_view(), name='business-plan-details'),
]
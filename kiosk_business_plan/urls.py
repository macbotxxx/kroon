from django.urls import path
from . import views


urlpatterns = [

    path('create-business-plan/', views.create_business_plan, name='create_business_plan'),
    path('business-plan-record/', views.business_plan, name='business_plan'),
    path('my-records/', views.my_business_record, name='my_business_record'),
    path('my-records-pdf/<str:plan_id>/', views.business_record_detail, name='business_record_detail'),
    path('delete-plan/<str:plan_id>/', views.delete_plan, name='delete_plan'),

]
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
# from account import views as acc_views


urlpatterns = [
 
    path('my-workers/', views.workers , name='workers'), 
    path('workers-details/<str:worker_id>/', views.worker_details , name='worker_details'), 
    path('verify-worker-email/', views.verify_email , name='verify_worker_email'), 
    path('verify-worker-code/', views.worker_otp_verification , name='worker_otp_verification'), 
    path('register-worker/', views.register_worker , name='register_worker'), 
    path('add-worker/', views.add_worker , name='add_worker'),
    path('remove-workers/<str:worker_id>/', views.remove_worker , name='remove_worker'), 
     
]
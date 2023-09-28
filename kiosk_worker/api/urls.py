from django.urls import path
from . import views

urlpatterns = [

    path('create-workers-account/', views.CreateWorkersAccountView.as_view(), name='WorkersAccount'),
    path('check-workers-email/<str:email>/', views.CheckWorkerEmailView.as_view(), name='CheckWorkerEmail'),
    path('workers-account/', views.All_Workers.as_view(), name='workers-profile'),
    path('workers-details/<str:email>/', views.Worker_Details.as_view(), name='Worker_Details'),
    path('add-workers/<str:email>/', views.Add_Worker_VIew.as_view(), name='Worker_add'),

]


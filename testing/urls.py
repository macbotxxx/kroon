from django.urls import path
from . import views


urlpatterns = [
    path('', views.my_scheduled_job, name='my_scheduled_job')
]
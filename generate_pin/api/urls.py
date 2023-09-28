from django.urls import path
from . import views


urlpatterns = [
    path('', views.Generate_pin_view.as_view(), name='generate_pin')
]

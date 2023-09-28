from django.urls import path
from . import views

urlpatterns = [
    path('all-users-list/', views.UserListView.as_view() ),
]
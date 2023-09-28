from django.urls import path
from . import views


urlpatterns = [

    path('categories/', views.List_Of_Categories.as_view()),
    path('categories/<int:category_id>/', views.Category_View.as_view()),
    path('categories-list/', views.Parent_Category.as_view()),
    path('all-user-category/', views.User_Category_View.as_view()),
    path('add-user-category/', views.User_Category_Add_View.as_view()),
    path('remove-user-category/', views.User_Category_Remove_View.as_view()),


]
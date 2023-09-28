from django.urls import path
from . import views

urlpatterns = [
    path('upload-products/', views.Upload_Production_view.as_view(), name ='upload_products'),
    path('product/<str:id>/', views.Update_Product.as_view(), name='edit_product'),
]
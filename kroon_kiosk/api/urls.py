# from django.urls import path
# from . import views

# urlpatterns = [
#     path('create-category/', views.CategoryView.as_view(), name='create-category'),
#     path('update-category/<str:id>/', views.UpdateCategoryView.as_view(), name='update-category'),
#     path('upload-product/', views.ProductView.as_view(), name='upload-product'),
#     path('product/<str:id>/', views.UpdateProductView.as_view(), name='edit-product'),
#     path('add-to-cart/', views.AddToCartView.as_view(), name='add_to_cart'),
#     path('reduce-cart-item/', views.RemoveItemCartView.as_view(), name='reduce_cart'),
#     path('delete-cart-item/<str:id>/', views.DeleteCartItem.as_view(), name='delete_cart'),
#     path('clear-cart/', views.ClearCart.as_view(), name='clear_cart'),
#     path('checkout/', views.CheckoutView.as_view(), name='checkout'),
# ]
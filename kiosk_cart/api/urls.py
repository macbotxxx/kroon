from django.urls import path
from . import views


urlpatterns = [
    
    path('add-to-cart/', views.AddToCartView.as_view(), name='add_to_cart'),
    path('reduce-cart-item/', views.RemoveItemCartView.as_view(), name='reduce_cart'),
    path('delete-cart-item/<str:id>/', views.DeleteCartItem.as_view(), name='delete_cart'),
    path('clear-cart/', views.ClearCart.as_view(), name='clear_cart'),
    path('kiosk_fast_checkout/', views.Kiosk_FastCheckout.as_view(), name='kiosk_fast_checkout'),
    path('checkout/', views.CheckoutView.as_view(), name='checkout'),

]

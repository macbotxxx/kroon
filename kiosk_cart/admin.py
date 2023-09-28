from django.contrib import admin
from .models import CartItem, OrderProduct, Order , Payment 
# Register your models here.


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('product',  'cart', 'quantity', 'is_active')
    list_display_links = ('product',  'cart', 'quantity', 'is_active')


class OrderProductInline(admin.TabularInline):
    model = OrderProduct
    readonly_fields = ('product_total_price','payment','user', 'quantity','variation', 'product_price', 'product','created_date', 'modified_date', 'ordered')
    extra = 0
   
    

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('user', 'payment_ref', 'payment_method', 'amount_paid', 'verified')
    list_display_link = ('user',)
    readonly_fields = ('user', 'payment_ref', 'payment_method', 'amount_paid', 'verified', 'status')
    list_filter = ('created_date','user', 'verified','status', )


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'payment', 'order_number', 'is_ordered')
    list_display_link = ('user',)
    readonly_fields = ('user', 'payment', 'order_number', 'order_total', 'is_ordered')
    inlines = [OrderProductInline]
    list_filter = ('created_date','user' )

@admin.register(OrderProduct)
class OrderProductAdmin(admin.ModelAdmin):
    list_display = ('user', 'worker', 'order', 'payment', 'product', 'quantity', 'weight_quantity', 'product_price',  'product_total_price',  'ordered')
    list_display_link = ('user', 'worker', 'order', 'payment', 'product', 'quantity',  'product_price','product_total_price', 'ordered')
    list_filter = ('created_date','user','ordered' )
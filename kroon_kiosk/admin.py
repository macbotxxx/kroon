# from django.contrib import admin
# from .models import Category, Product, Cart, CartItem


# @admin.register(Category)
# class CategoryAdmin(admin.ModelAdmin):
#     list_display = ('user','category','slug',  'created_date', 'modified_date', 'active',)
#     list_display_link = ('user','category','slug',  'created_date', 'modified_date', 'active',)


# @admin.register(Product)
# class ProductAdmin(admin.ModelAdmin):
#     list_display = ('user', 'product_sku', 'product_name',  'price', 'stock', 'is_available',)
#     list_display_link = ('user', 'product_sku', 'product_name',  'price', 'stock', 'is_available',)


# @admin.register(CartItem)
# class CartItemAdmin(admin.ModelAdmin):
#     list_display = ('product',  'cart', 'quantity', 'is_active')
#     list_display_links = ('product',  'cart', 'quantity', 'is_active')
from django.contrib import admin
from .models import Merchant_Product, ProductVariation
# Register your models here.


# @admin.register(ProductVariation)
# class ProductVariationAdmin(admin.ModelAdmin):
#     list_display = ('product', 'variations_category', 'variation_value', 'is_active')
#     list_display_links = ('product', 'variations_category', 'variation_value')
#     list_editable = ('is_active',)


# tabular section 
class ProductVariationTabular(admin.TabularInline):
    model = ProductVariation
    fields = ('variations_category','variation_value','quantity','weight_quantity', 'is_active')
    extra = 1


class ProductPrice(admin.TabularInline):
    model = Merchant_Product
    fields = ('price', 'cost_price', 'merchant_local_currency')
    extra = 0


@admin.register(Merchant_Product)
class Merchant_ProductAdmin(admin.ModelAdmin):
    list_display = ('user', 'product_sku', 'product_name','charge_by_weight','price','cost_price', 'stock')
    list_display_links = ('user', 'product_sku', 'product_name')
    inlines = [ProductVariationTabular ]




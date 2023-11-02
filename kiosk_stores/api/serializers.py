from rest_framework import serializers
from django_filters import rest_framework as filters
from kiosk_stores.models import Merchant_Product, ProductVariation
from kroon.users.models import User

class UserDetails (serializers.ModelSerializer):
    
    class Meta:
        model = User
        ref_name = "kiosk_user"
        fields = ('id', 'name','wallet_id', 'email', 'merchant_business_name')


class ProductVariationSerializer (serializers.ModelSerializer):

    class Meta:
        model = ProductVariation
        fields = ['variations_category','variation_value','quantity','weight_quantity']


class ProductFilter(filters.FilterSet):
    product_name = filters.CharFilter(field_name="product_name" , lookup_expr='icontains')
    stock = filters.NumberFilter()
    stock__lt = filters.NumberFilter(field_name='stock', lookup_expr='lt')
    charge_by_weight = filters.NumberFilter()
    charge_by_weight__lt = filters.NumberFilter(field_name='charge_by_weight', lookup_expr='lt')
    class Meta:
        model = Merchant_Product
        fields = ['product_name', 'category', 'is_available', 'stock','charge_by_weight',]


class Upload_Products_Serializer (serializers.ModelSerializer):
    products_variation = ProductVariationSerializer( required = False ,  many = True )

    class Meta:
        model = Merchant_Product
        fields = ['product_sku', 'product_name', 'price', 'cost_price', 'stock', 'charge_by_weight','weight_quantity','weight_unit','out_of_stock_notify','low_stock_limit', 'category', 'products_variation', 'image', 'expire_notify', 'expiring_date','expiry_days_notify',]


class Edit_Products_Serializer (serializers.ModelSerializer):
    products_variation = ProductVariationSerializer( required = False ,  many = True )

    class Meta:
        model = Merchant_Product
        fields = ['product_sku', 'product_name', 'price', 'cost_price', 'stock', 'charge_by_weight','weight_quantity','weight_unit','out_of_stock_notify','low_stock_limit', 'category', 'products_variation','expire_notify', 'expiring_date','expiry_days_notify',]
 


class Update_Products_Serializer (serializers.ModelSerializer):
    id = serializers.UUIDField()

    class Meta:
        model = Merchant_Product
        fields = "__all__"
        read_only_fields = ('user','slug','is_available','merchant_local_currency','created_date', 'modified_date')



class Product_Details_Serializers (serializers.ModelSerializer):
    products_variation = ProductVariationSerializer( many=True, read_only=True )
    class Meta:
        model = Merchant_Product
        # fields = ['id', 'product_sku', 'product_name', 'products_variation']
        fields = ['id', 'products_variation','product_sku','charge_by_weight','weight_quantity','weight_unit','out_of_stock_notify','low_stock_limit', 'product_name', 'slug', 'category', 'price','cost_price','image', 'stock','is_available','expire_notify', 'expiring_date','expiry_days_notify','created_date', 'modified_date',]
        read_only_fields = fields

  
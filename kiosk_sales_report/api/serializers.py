from rest_framework import serializers
from django_filters import rest_framework as filters

from kiosk_stores.models import Merchant_Product, ProductVariation
from kroon.users.models import User
from kiosk_cart.models import Payment, OrderProduct , Order


class ProductDetails (serializers.ModelSerializer):

    class Meta:
        model = Merchant_Product
        fields = "__all__"
        ref_name = "product_details"
        read_only_fields = ('id','user', 'product_sku', 'product_name', 'slug', 'category', 'price', 'merchant_local_currency', 'image', 'stock', 'is_available', 'created_date', 'modified_date',)


class UserDetails (serializers.ModelSerializer):
    
    class Meta:
        model = User
        ref_name = "User_12"
        fields = ('id', 'name','wallet_id', 'email', 'merchant_business_name')


class PaymentDetails (serializers.ModelSerializer):

    class Meta:
        model = Payment
        fields =  ('id', 'payment_ref', 'payment_method', 'amount_paid','cash_collected', 'customers_change','verified', 'status')
        


class PaymentDetails1 (serializers.ModelSerializer):
    class Meta:
        model = Payment
        ref_name ='payment_method1'
        fields = ( 'payment_ref', 'verified','payment_method')


class SalesListFilter(filters.FilterSet):
    order_number = filters.CharFilter( field_name='order_number', lookup_expr='icontains')
    payment = filters.CharFilter( field_name='payment__payment_method', lookup_expr='icontains')
    created_date = filters.CharFilter( field_name='created_date', lookup_expr='icontains')
    class Meta:
        model = Order
        fields = ['order_number', 'is_ordered','refund', 'payment','created_date',]



class List_Of_Sales_Serializer (serializers.ModelSerializer):
    payment = PaymentDetails1(read_only = True)
    class Meta:
        model = Order
        fields = ['order_number', 'order_total', 'is_ordered','refund', 'worker', 'payment','created_date', 'modified_date',]


class ProductDetailsTwo (serializers.ModelSerializer):

    class Meta:
        model = Merchant_Product
        fields =['product_sku', 'product_name', 'price','merchant_local_currency', 'image',]



class ProductVariationSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductVariation
        ref_name = 'product_variation2'
        fields = ['variations_category', 'variation_value', ]        


class SaleDetailsSerializer(serializers.ModelSerializer):
    product = ProductDetailsTwo( read_only = True)
    variation = ProductVariationSerializer( required = False, many = True )
    payment = PaymentDetails( read_only = True )

    class Meta:
        model = OrderProduct
        fields = ('worker', 'product', 'variation','quantity','product_total_price', 'ordered','refund', 'refund_quantity','refund_weight_quantity','refund_product_price', 'payment')
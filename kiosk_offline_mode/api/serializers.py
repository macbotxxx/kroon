from rest_framework import serializers
from kiosk_cart.models import CartItem, Payment , OrderProduct
from django.utils.translation import gettext_lazy as _
from kiosk_stores.models import Merchant_Product, ProductVariation



class ProductVariationSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductVariation
        ref_name = 'product_variation'
        fields = ['variations_category', 'variation_value', ]



class Offline_Product (serializers.ModelSerializer):
    product_variation = ProductVariationSerializer( required = False, many = True )
    quantity = serializers.CharField(required = True)
    
    class Meta:
        model = CartItem
        fields = ('quantity', 'product', 'product_variation', )


class Offline_CheckOut_Payment (serializers.ModelSerializer):

    cash_collected = serializers.DecimalField(max_digits = 300, decimal_places = 2, required = False)
    customers_change = serializers.DecimalField(max_digits = 300, decimal_places = 2, required = False)
    manual_sale = serializers.DecimalField(max_digits = 300, decimal_places = 2, required = False)
    is_manual_sale = serializers.BooleanField( required = False )
    created_date = serializers.DateTimeField()
    products = Offline_Product( many = True)

    class Meta:
        model = Payment
        fields = [ 'cash_collected','amount_paid', 'customers_change' , 'manual_sale', 'is_manual_sale','payment_method', 'products','created_date', ]



class Offline_Checkout_Serializer (serializers.Serializer):
    offline_checkout = Offline_CheckOut_Payment( many=True , source="cartitem_set" )


class Email_Support_Serializer (serializers.Serializer):
    customer_email = serializers.EmailField()
    email_subject = serializers.CharField()
    message = serializers.CharField()


class OfflineProductVariationSerializer (serializers.ModelSerializer):

    class Meta:
        model = ProductVariation
        fields = ['variations_category','variation_value','quantity','weight_quantity']


class OfflineUpload_Products_Serializer (serializers.ModelSerializer):
    products_variation = OfflineProductVariationSerializer( required = False ,  many = True )

    class Meta:
        model = Merchant_Product
        fields = ['product_sku', 'product_name', 'price', 'cost_price', 'stock', 'charge_by_weight','weight_quantity','weight_unit','out_of_stock_notify','low_stock_limit', 'category', 'products_variation', 'image', 'expire_notify', 'expiring_date','expiry_days_notify',]


class Offline_Product_Upload ( serializers.Serializer ):
    offline_products = OfflineUpload_Products_Serializer( many = True )


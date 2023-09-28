from xml.parsers.expat import model
from rest_framework import serializers
from kiosk_cart.models import CartItem, Payment , OrderProduct
from django.utils.translation import gettext_lazy as _
from kiosk_stores.models import Merchant_Product, ProductVariation



class ProductSerializer(serializers.ModelSerializer):
    image = serializers.ImageField()
    class Meta:
        model = Merchant_Product
        fields = "__all__"
        read_only_fields = ('id','user','slug', 'created_date', 'modified_date',)


class ProductVariationSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductVariation
        ref_name = 'product_variation'
        fields = ['variations_category', 'variation_value', ]


class ProductDetails (serializers.ModelSerializer):

    class Meta:
        model = Merchant_Product
        fields =['id', 'product_sku', 'product_name', 'price', 'cost_price', 'merchant_local_currency', 'image', 'stock', 'charge_by_weight', 'is_available', 'category']


class AddToCartSerializer(serializers.ModelSerializer):

    class Meta:
        model = CartItem
        fields = "__all__"
        read_only_fields = ('id', 'user', 'cart', 'is_active', 'created_date', 'modified_date',)



class AddToCartSerializerNew(serializers.ModelSerializer):
    product_variation = ProductVariationSerializer( required = False, many = True )
    quantity = serializers.CharField()
    
    class Meta:
        model = CartItem
        fields = ('quantity', 'product', 'product_variation', )
        


class NewAddToCartSerializer (serializers.Serializer):
    add_to_cart = AddToCartSerializerNew( many=True , source="cartitem_set" )


class GetCartSerializer(serializers.ModelSerializer):
    product = ProductDetails( read_only=True )
    product_variation = ProductVariationSerializer( many=True , read_only=True )
    class Meta:
        model = CartItem
        fields = ('id', 'quantity', 'is_active','product_variation' ,'product')
        


class RemoveItemCartSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = "__all__"
        read_only_fields = ('id', 'user', 'cart', 'is_active','quantity', 'created_date', 'modified_date',)


class CheckOutSerializer(serializers.ModelSerializer):
    kroon_transaction_ref = serializers.CharField( required = False)
    cash_collected = serializers.DecimalField(max_digits = 300, decimal_places = 2, required = False)
    customers_change = serializers.DecimalField(max_digits = 300, decimal_places = 2, required = False)
    manual_sale = serializers.DecimalField(max_digits = 300, decimal_places = 2, required = False)
    is_manual_sale = serializers.BooleanField( required = False )
    class Meta:
        model = Payment
        fields = "__all__"
        read_only_fields = ('user', 'payment_ref', 'verified', 'status', 'created_date', 'modified_date', 'worker')




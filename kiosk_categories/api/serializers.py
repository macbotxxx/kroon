from rest_framework import serializers

from kiosk_categories.models import Category
from kiosk_stores.models import Merchant_Product
from kiosk_stores.models import ProductVariation
from kroon.users.models import User, BusinessProfile

class UserDetails (serializers.ModelSerializer):
    
    class Meta:
        model = User
        ref_name = "kiosk_user"
        fields = ('id', 'name','wallet_id', 'email', 'merchant_business_name')


class ProductVariationSerializer (serializers.ModelSerializer):

    class Meta:
        model = ProductVariation
        ref_name = 'product_variation_category'
        fields = ['variations_category','variation_value','quantity','weight_quantity',]



class Category_child (serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('id','category', 'slug')


class Category_Serializer(serializers.ModelSerializer):
    # children = Category_child( many=True, required=False )

    class Meta:
        model = Category
        fields = ('id','category','image')
   

class Category_Parent_Serializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('id','category', 'parent', 'slug', 'image')
        read_only_fields = ('id','category', 'parent', 'slug', 'image')



class User_Selected_Category (serializers.ModelSerializer):
    class Meta:
        model = BusinessProfile
        fields = ['business_category',]



class Product_Details_Serial (serializers.ModelSerializer):
    user = UserDetails( read_only = True )
    products_variation = ProductVariationSerializer( many=True, read_only=True )
    
    class Meta:
        model = Merchant_Product
        fields = ['id', 'user', 'products_variation','product_sku','charge_by_weight','weight_quantity','weight_unit','out_of_stock_notify','low_stock_limit', 'product_name', 'slug', 'category', 'price','cost_price', 'image', 'stock', 'is_available','expire_notify','expiring_date', 'created_date', 'modified_date',]
        read_only_fields = fields


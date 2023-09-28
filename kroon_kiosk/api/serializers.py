# from rest_framework import serializers
# from kroon_kiosk.models import Category, Product, CartItem, Payment
# from django.utils.translation import gettext_lazy as _



# class CategorySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Category
#         fields = "__all__"
#         read_only_fields = ('id','user', 'slug','active' ,'created_date', 'modified_date',)


# class ProductSerializer(serializers.ModelSerializer):
#     image = serializers.ImageField()
#     class Meta:
#         model = Product
#         fields = "__all__"
#         read_only_fields = ('id','user','slug', 'created_date', 'modified_date',)

# class ProductDetails (serializers.ModelSerializer):
#     class Meta:
#         model = Product
#         fields = "__all__"

# class AddToCartSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = CartItem
#         fields = "__all__"
#         read_only_fields = ('id', 'user', 'cart', 'is_active', 'created_date', 'modified_date',)

# class GetCartSerializer(serializers.ModelSerializer):
#     product = ProductDetails(read_only=True)
#     class Meta:
#         model = CartItem
#         fields = "__all__"
#         read_only_fields = ('id', 'user', 'cart', 'is_active', 'created_date', 'modified_date','sub_totals')


# class RemoveItemCartSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = CartItem
#         fields = "__all__"
#         read_only_fields = ('id', 'user', 'cart', 'is_active','quantity', 'created_date', 'modified_date',)


# class CheckOutSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Payment
#         fields = "__all__"
#         read_only_fields = ('user', 'payment_ref', 'verified', 'status', 'created_date', 'modified_date')
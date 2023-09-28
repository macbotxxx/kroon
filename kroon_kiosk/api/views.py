# from django.http import request
# from helpers.common.security import KOKPermission
# from kroon.users.models import User, UserWrongPinValidate
# from rest_framework.response import Response
# from rest_framework.permissions import IsAuthenticated, AllowAny
# from rest_framework import status, serializers
# from rest_framework.generics import  CreateAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView, DestroyAPIView, ListAPIView,get_object_or_404
# from rest_framework.views import APIView

# from .serializers import CategorySerializer , ProductSerializer, AddToCartSerializer, GetCartSerializer, RemoveItemCartSerializer, CheckOutSerializer


# from kroon_kiosk.models import Category, Product, Cart, CartItem
# import requests
# import random
# import string

# def cart_number():
#     return ''.join(random.choices(string.ascii_lowercase + string.digits, k=45))


# def _cart_id (request):
#     cart = request.session.get('cart_x')
#     if not cart:
#         cart = request.session['cart_x'] = cart_number()
#     return cart

# # marchant cateogry function starts here 

# class CategoryView (ListCreateAPIView):
#     permission_classes = [ IsAuthenticated, KOKPermission ]
#     serializer_class = CategorySerializer

#     def get(self, request, *args, **kwargs):
#         user_category = Category.objects.filter(user=request.user)
#         serializer = self.serializer_class(user_category, many=True)
#         return Response({'status':'success', 'message':'Successfully get merchant category','data':serializer.data}, status=status.HTTP_201_CREATED)

#     def post(self, request, *args, **kwargs):
#         serializer = self.serializer_class(data=request.data)
#         if serializer.is_valid():
#             serializer.save(user=request.user)
#             return Response({'status':'success', 'message':'Successfully created category','data':serializer.data}, status=status.HTTP_201_CREATED)

#         return Response(serializer.errors,  status=status.HTTP_400_BAD_REQUEST)


# class UpdateCategoryView (RetrieveUpdateDestroyAPIView):
#     permission_classes = [ IsAuthenticated, KOKPermission ]
#     serializer_class = CategorySerializer
#     queryset = Category.objects.all()
#     lookup_field = 'id'

# # marchant cateogry function ends here 

# # marchant products function starts here 

# class ProductView (ListCreateAPIView):
#     permission_classes = [ IsAuthenticated, KOKPermission ]
#     serializer_class = ProductSerializer

#     def get(self, request, *args, **kwargs):
#         user_product = Product.objects.filter(user=request.user)
#         serializer = self.serializer_class(user_product, many=True)
#         return Response({'status':'success', 'message':'merchant products fetched successfully','data':serializer.data}, status=status.HTTP_201_CREATED)

#     def post(self, request, *args, **kwargs):
#         serializer = self.serializer_class(data=request.data)
#         if serializer.is_valid():
#             serializer.save(user=request.user)
#             return Response({'status':'success', 'message':'product created successfully','data':serializer.data}, status=status.HTTP_201_CREATED)

#         return Response(serializer.errors,  status=status.HTTP_400_BAD_REQUEST)


# class UpdateProductView (RetrieveUpdateDestroyAPIView):
#     permission_classes = [ IsAuthenticated, KOKPermission ]
#     serializer_class = ProductSerializer
#     queryset = Product.objects.all()
#     lookup_field = 'id'
# # marchant cateogry function ends here 


# class AddToCartView (ListCreateAPIView):
#     permission_classes = [ IsAuthenticated, KOKPermission ]
#     serializer_class = AddToCartSerializer
    
#     def get(self, request, *args, **kwargs):
#         total = 0
#         all_cart_items = CartItem.objects.filter(user=request.user)
#         serializer = GetCartSerializer(all_cart_items, many=True)
#         for cart_item in all_cart_items:
#             total += (cart_item.product.price * cart_item.quantity)
#             # quantity += cart_item.quantity
#         # shipping_rate_per_quantity = ( 100 * quantity )
#         grandtotal = total 
#         return Response({'status':'success', 'message':'list of all current cart items','grand total':grandtotal, 'data':serializer.data},  status=status.HTTP_200_OK)
      
#     def post (self, request, *args, **kwargs):
#         serializer = self.serializer_class(data=request.data)
#         current_user = request.user

#         if serializer.is_valid():
#             product_id = serializer.data.get('product')
#             quantity = serializer.data.get('quantity')
#             try:
#                 is_cart_item_exist = CartItem.objects.get(product__id=product_id, user = current_user) #checking if the product and variation exists
#                 if is_cart_item_exist:
#                     is_cart_item_exist.quantity += quantity
#                     is_cart_item_exist.save()
#                     return Response({'status':'success', 'message':'Product is been added updated successfully', 'data':self.serializer_class(is_cart_item_exist).data},  status=status.HTTP_201_CREATED) 
              
#             except CartItem.DoesNotExist:
#                 product = Product.objects.get(id=product_id)
#                 if product:
#                     cart = CartItem.objects.create(product=product, quantity=quantity,  user = current_user)
#                     return Response({'status':'success', 'message':'Product is been added to cart successfully', 'data':self.serializer_class(cart).data},  status=status.HTTP_201_CREATED)
#                 else:
#                     return Response({'status':'error', 'message':'Product id dont not exist'},  status=status.HTTP_201_CREATED)

#         return Response(serializer.errors,  status=status.HTTP_400_BAD_REQUEST)


# class RemoveItemCartView (CreateAPIView):
#     permission_classes = [ IsAuthenticated, KOKPermission ]
#     serializer_class = RemoveItemCartSerializer

#     def post(self, request, *args, **kwargs):
#         serializer = self.serializer_class(data=request.data)
#         current_user = request.user
        
#         if serializer.is_valid():
#             product_id = serializer.data.get('product')
#             try:
#                 # get the product
#                 is_cart_item_exist = CartItem.objects.get(product__id=product_id, user = current_user) #checking if the product and variation exists
#                 if is_cart_item_exist.quantity > 1:
#                     is_cart_item_exist.quantity -= 1
#                     is_cart_item_exist.save()
#                     return Response({'status':'error', 'message':'Product quantity is reduced successfully', 'data':self.serializer_class(is_cart_item_exist).data},status=status.HTTP_201_CREATED) 
#                 else:
#                     is_cart_item_exist.delete()
#                     return Response({'status':'error', 'message':'Product is been deleted from cart list'},  status=status.HTTP_201_CREATED)
                 
#             except CartItem.DoesNotExist:
#                 return Response({'status': 'error', 'message':'product id does not exist'},  status=status.HTTP_404_NOT_FOUND)

#         return Response(serializer.errors,  status=status.HTTP_400_BAD_REQUEST)

# class DeleteCartItem (DestroyAPIView):
#     permission_classes = [ IsAuthenticated, KOKPermission ]

#     def delete(self, request, *args, **kwargs):
#         cart_id = kwargs.get('id')
#         try:
#             cart_item = CartItem.objects.get(id=cart_id, user=request.user)
#             cart_item.delete()
#             return Response({'status':'success', 'message':'Product is been deleted from cart list'},  status=status.HTTP_201_CREATED)
#         except CartItem.DoesNotExist:
#             return Response({'status':'success', 'message':'cart id does not exist'}, status.HTTP_400_BAD_REQUEST)


# class ClearCart (APIView):
#     permission_classes = [ IsAuthenticated, KOKPermission ]
    
#     def get(self, request, *args, **kwargs):
#         cart = CartItem.objects.filter(user=request.user)
#         cart.delete()
#         return Response({'status':'success', 'message':'cart items is cleared successfully'}, status=status.HTTP_201_CREATED)

# class CheckoutView (CreateAPIView):
#     permission_classes = [ IsAuthenticated, KOKPermission ]
#     serializer_class = CheckOutSerializer

#     def post(self, request, *args, **kwargs):
#         serializer = self.serializer_class(data=request.data)
#         if serializer.is_valid():
#             payment_method = serializer.data.get('payment_method')
#             amount_paid = serializer.data.get('amount_paid')

            




from helpers.common.security import KOKPermission , KOKMerchantPermission
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status, serializers
from rest_framework.generics import  CreateAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView, DestroyAPIView, ListAPIView,get_object_or_404
from rest_framework.views import APIView
from django.db.models import Q

from mptt.templatetags.mptt_tags import cache_tree_children
from .serializers import Category_Serializer, Product_Details_Serial ,Category_Parent_Serializer, User_Selected_Category
from kiosk_categories.models import Category
from kiosk_stores.models import Merchant_Product
from kiosk_cart.api.views import _company_account
from kroon.users.models import User, UserWrongPinValidate, BusinessProfile
from django_filters import rest_framework as filters




class List_Of_Categories (ListAPIView):
    permission_classes = [ IsAuthenticated, KOKPermission ]
    serializer_class = Category_Serializer
    queryset = Category.objects.all()

    def list (self, category, *args, **kwargs):
        # category with children
        # catgory_list = cache_tree_children(Category.objects.filter(level = 0 ))
    
        all_categories = self.serializer_class(self.get_queryset(), many=True)
        return Response({'status':'success','message':'List of all categories fetched successfully','data':all_categories.data}, status = status.HTTP_200_OK)


class Category_View (ListAPIView):
    permission_classes = [ IsAuthenticated,  KOKPermission ]
    serializer_class = Product_Details_Serial
    queryset = Category.objects.all()

    def get (self, request, *args, **kwargs):
        company_profile =  _company_account(request)
        category_id = kwargs.get('category_id')
        try:
            category = self.get_queryset().get( id = category_id )
        except Category.DoesNotExist:
            return Response({'status':'error', 'message':'Cant find the category , check your input and try again'}, status = status.HTTP_404_NOT_FOUND)
        
        if category.parent is None:
            products = Merchant_Product.objects.filter( Q(category__parent = category) | Q (category = category), user = company_profile  ) 
        else:
            products = Merchant_Product.objects.filter( category = category , user = company_profile ) 

        serializer = self.serializer_class(products, many=True)

        return Response({'status':'success','message':'List of categories','data':serializer.data}, status = status.HTTP_202_ACCEPTED)



class Parent_Category (ListAPIView):
    permission_classes = [ AllowAny, KOKPermission ]
    serializer_class = Category_Parent_Serializer
    queryset = Category.objects.all()
    def get (self, request, *args, **kwargs):
        category = self.get_queryset().filter( parent = None )
        serializer = self.serializer_class( category , many=True )
        return Response({'status':'success','message':'List of products in the particular category','data':serializer.data}, status = status.HTTP_202_ACCEPTED)



class User_Category_View (ListAPIView):
    permission_classes = [ IsAuthenticated, KOKPermission , KOKMerchantPermission ]
    serializer_class = Category_Serializer
    queryset = BusinessProfile.objects.all()

    def get(self, request, *args, **kwargs):
        user_business = self.get_queryset().filter( user = _company_account(request) , active = True )
        for i in user_business:
            serializer = self.serializer_class( i.business_category, many = True )
        return Response({'status':'success','message':'list of users selected category fetched successfully', 'data':serializer.data}, status=status.HTTP_200_OK)



class User_Category_Add_View (CreateAPIView):
    permission_classes = [ IsAuthenticated, KOKPermission , KOKMerchantPermission]
    serializer_class = User_Selected_Category
    queryset = BusinessProfile.objects.all()

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class( data=request.data )
        if serializer.is_valid():
            business_category = serializer.validated_data.get('business_category')
            for i in business_category:
                business_category = i.id
                try:
                    self.get_queryset().get( user = request.user , business_category = business_category, active = True )
                    return Response({'status':'error', 'message':'business category already been added'}, status=status.HTTP_400_BAD_REQUEST)

                except BusinessProfile.DoesNotExist:
                    user_business = self.get_queryset().get ( user = request.user , active = True)
                    user_business.business_category.add( business_category)

            return Response({'status':'success'}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors,  status=status.HTTP_400_BAD_REQUEST)



class User_Category_Remove_View (CreateAPIView):
    permission_classes = [ IsAuthenticated, KOKPermission , KOKMerchantPermission]
    serializer_class = User_Selected_Category
    queryset = BusinessProfile.objects.all()

    def post (self, request, *args, **kwargs):
        serializer = self.serializer_class( data=request.data )
        if serializer.is_valid():
            business_category = serializer.validated_data.get('business_category')
            for i in business_category:
                business_category = i.id
                try:
                    user_business = self.get_queryset().get ( user = request.user , active = True )
                    user_business.business_category.remove(business_category)

                    # delete products from category
                    Merchant_Product.objects.filter( category = business_category , user = _company_account(request) ).delete()

                    return Response({'status':'success', 'message':'business category is removed successfully'}, status=status.HTTP_200_OK)

                except self.get_queryset().DoesNotExist:
                    return Response({'status':'error', 'message':'business category not found'}, status=status.HTTP_404_NOT_FOUND)

        return Response(serializer.errors,  status=status.HTTP_400_BAD_REQUEST)






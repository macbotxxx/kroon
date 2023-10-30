import json
from os import access
from helpers.common.security import KOKPermission, KOKMerchantPermission
from kroon.users.models import User, UserWrongPinValidate , BusinessProfile
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status, serializers
from rest_framework.generics import  CreateAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView, DestroyAPIView, ListAPIView,get_object_or_404,UpdateAPIView
from rest_framework.views import APIView
from django_filters import rest_framework as filters

from .serializers import Upload_Products_Serializer, Product_Details_Serializers, Update_Products_Serializer,Edit_Products_Serializer, ProductFilter
from kiosk_stores.models import Merchant_Product , ProductVariation
from kiosk_cart.api.views import _company_account
from subscriptions.models import Subscription_Plan ,Merchant_Subcribers
from kroon.users.pagination import StandardResultsSetPagination



class Upload_Production_view (ListCreateAPIView):

    permission_classes = [ IsAuthenticated, KOKPermission , KOKMerchantPermission ]
    serializer_class = Upload_Products_Serializer
    queryset = Merchant_Product.objects.all()
    product_details_serializer_class = Product_Details_Serializers
    pagination_class = StandardResultsSetPagination
    # serializer_class_update = Update_Products_Serializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = ProductFilter


    def list(self, request, *args, **kwargs):
        company_profile = _company_account(request)
        business_profile = BusinessProfile.objects.get( user = company_profile , active = True )
        products = self.get_queryset().filter( user = company_profile , business_profile = business_profile )
        queryset = self.filter_queryset(products)
        page = self.paginate_queryset(queryset)
        serializer = self.product_details_serializer_class(page, many=True)
        return self.get_paginated_response(serializer.data)
      

    def create(self, request, *args, **kwargs):
        company_profile = _company_account(request)
        business_profile = BusinessProfile.objects.get( user = company_profile , active = True )
        unique_sku = business_profile.business_name
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            product_sku = serializer.validated_data.get('product_sku')
            product_name = serializer.validated_data.get('product_name')
            price = serializer.validated_data.get('price')
            cost_price = serializer.validated_data.get('cost_price')
            stock = serializer.validated_data.get('stock')
            weight_unit = serializer.validated_data.get('weight_unit')
            out_of_stock_notify = serializer.validated_data.get('out_of_stock_notify')
            low_stock_limit = serializer.validated_data.get('low_stock_limit')
            charge_by_weight = serializer.validated_data.get('charge_by_weight')
            weight_quantity = serializer.validated_data.get('weight_quantity')
            category = serializer.validated_data.get('category')
            products_variation = serializer.validated_data.pop('products_variation')
            image = serializer.validated_data.get('image')
            expire_notify = serializer.validated_data.get('expire_notify')
            expiring_date = serializer.validated_data.get('expiring_date')

            

            # if verify_image is not None:
            #     image = serializer.validated_data.get('image')
            # else:
            #     image = DEFAULT_IMAGE

            # checking the user plan and permissions
            # user permissions
            try:
                user_plan = Merchant_Subcribers.objects.get( user = request.user , active = True )
            except Merchant_Subcribers.DoesNotExist :
                user_plan = None 

            if user_plan is not None :
            
                if user_plan.plan.plan_name == "Basic":
                    count = Merchant_Product.objects.filter( user = company_profile ).count()
                    if count > 10:
                        return Response({'status':'error', 'message':'Your business account has exceeded it product limit kindly upgrade your package.'}, status=status.HTTP_400_BAD_REQUEST)
                        
                elif user_plan.plan.plan_name == "Kiosk Plus":
                    count = Merchant_Product.objects.filter( user = company_profile ).count()
                    if count > 49:
                        return Response({'status':'error', 'message':'Your business account has exceeded it product limit kindly upgrade your package.'}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    pass
            else:
                return Response({'status':'error', 'message':'Your business account has exceeded it product limit kindly upgrade your package.'}, status=status.HTTP_400_BAD_REQUEST)
            
            # uploading the product 
            product = Merchant_Product()
            product.product_sku = f'{unique_sku[0:3]}-{product_sku}'
            product.product_name = product_name
            product.price = price
            product.cost_price = cost_price
            product.stock = stock
            product.weight_quantity = weight_quantity
            product.charge_by_weight = charge_by_weight
            product.category = category
            product.weight_unit = weight_unit
            product.out_of_stock_notify = out_of_stock_notify
            product.low_stock_limit = low_stock_limit
            product.merchant_local_currency = request.user.default_currency_id
            product.user = company_profile
            product.image = image
            product.expire_notify = expire_notify
            product.expiring_date = expiring_date
            product.business_profile = business_profile
            product.save()

            # confirmation of the product is been created
            for variation in products_variation: #TODO: making variation optional 
                if variation.get("variations_category" ) is not None:
                    variations = ProductVariation()
                    variations.variations_category = variation.get("variations_category" )
                    variations.variation_value = variation.get("variation_value" )
                    variations.quantity = variation.get("quantity" )
                    variations.weight_quantity = variation.get("weight_quantity" )
                    variations.product = product
                    variations.save()
                        
            return Response({'status': 'success','message':'Item has been uploaded successfully', 'data':serializer.data}, status=status.HTTP_201_CREATED)
            
            # else:
            #     return Response({'status':'error', 'message':'product has not been uplaoded..'}, status=status.HTTP_403_FORBIDDEN )

        return Response(serializer.errors,  status=status.HTTP_400_BAD_REQUEST)



class Update_Product (RetrieveUpdateDestroyAPIView):

    permission_classes = [ IsAuthenticated, KOKPermission , KOKMerchantPermission ]
    serializer_class = Edit_Products_Serializer
    queryset = Merchant_Product.objects.all()
    lookup_field = 'id'

    def patch (self, request, *args, **kwargs):
        company_profile = _company_account(request)
        business_profile = BusinessProfile.objects.get( user = company_profile , active = True )

        product_id = kwargs.get('id')
        try:
            product = Merchant_Product.objects.get( id = product_id )
        except Merchant_Product.DoesNotExist:
            return Response({'status':'error','message':'Product does not exist in our database'}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class( data = request.data )
        if serializer.is_valid():
            product_sku = serializer.validated_data.get('product_sku')
            product_name = serializer.validated_data.get('product_name')
            price = serializer.validated_data.get('price')
            cost_price = serializer.validated_data.get('cost_price')
            stock = serializer.validated_data.get('stock')
            weight_unit = serializer.validated_data.get('weight_unit')
            out_of_stock_notify = serializer.validated_data.get('out_of_stock_notify')
            low_stock_limit = serializer.validated_data.get('low_stock_limit')
            charge_by_weight = serializer.validated_data.get('charge_by_weight')
            weight_quantity = serializer.validated_data.get('weight_quantity')
            expire_notify = serializer.validated_data.get('expire_notify')
            expiring_date = serializer.validated_data.get('expiring_date')
            category = serializer.validated_data.get('category')
            products_variation = serializer.validated_data.pop('products_variation')
        
            Merchant_Product.objects.filter( id = product_id ).update( product_sku = product_sku , product_name = product_name, price = price , cost_price = cost_price , stock = stock , weight_unit = weight_unit , out_of_stock_notify = out_of_stock_notify  ,  charge_by_weight = charge_by_weight ,weight_quantity = weight_quantity, low_stock_limit = low_stock_limit , category = category , merchant_local_currency = request.user.default_currency_id , user = company_profile , business_profile = business_profile,expire_notify = expire_notify , expiring_date = expiring_date  )

            ProductVariation.objects.filter( product = product ).delete()
            for variation in products_variation: #TODO: making variation optional 
                if variation.get("variations_category" ) is not None:
                
                    ProductVariation.objects.create( product = product, variations_category = variation.get("variations_category" ) , variation_value = variation.get("variation_value" ), quantity = variation.get("quantity") , weight_quantity = variation.get("weight_quantity") )
                else:
                    ProductVariation.objects.filter( product = product ).delete()
        
            return Response({'status': 'success','message':'item updated successfully', 'data': serializer.data})

        return Response(serializer.errors,  status=status.HTTP_400_BAD_REQUEST)



    



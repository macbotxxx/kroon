import json
import random
import string

from decimal import Decimal
from django.core.serializers.json import DjangoJSONEncoder
from django.core.mail import send_mail
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status, serializers
from rest_framework.generics import  CreateAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView, DestroyAPIView, ListAPIView,GenericAPIView
from rest_framework.views import APIView

from kiosk_cart.models import  Cart, CartItem, Order, Payment, OrderProduct
from kiosk_stores.models import Merchant_Product, ProductVariation
from subscriptions.models import Merchant_Subcribers
from kroon.users.models import BusinessProfile, User
from helpers.common.decorators import kiosk_pro_merchants
from kiosk_cart.api.views import _company_account
from helpers.common.security import KOKPermission , KOKMerchantPermission
from .serializers import Offline_Checkout_Serializer, Email_Support_Serializer, Offline_Product_Upload
from kiosk_cart.api.views import _user_account , _company_account
from kiosk_categories.models import Category 



# Generating random number...
def order_number():
    """
    the order number generator
    """
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))

def transaction_ref():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=25))

def cart_number():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=45))


class Network_Test (APIView):
    permission_classes = [ AllowAny,]
    def get (self, request, *args, **kwargs):
        return Response({'status':'success','message':'network is connected'}, status=status.HTTP_202_ACCEPTED)
        



class Kiosk_Offline_Checkout (CreateAPIView):
    permission_classes = [ IsAuthenticated, KOKPermission, ]
    serializer_class = Offline_Checkout_Serializer

    def post (self, request, *args, **kwargs):
        # capturing the company account
        company_profile =  _company_account(request)
        worker = _user_account(request)
        # end company profile
        serializer = self.serializer_class( data = request.data )
        if serializer.is_valid():
           
            product = serializer.data.get('offline_checkout')
            response_data = json.loads(json.dumps(product, cls=DjangoJSONEncoder))

            for offline_data in response_data:
                payment_method = offline_data['payment_method']
                amount_paid = offline_data['amount_paid']
                cash_collected = offline_data['cash_collected']
                customers_change = offline_data['customers_change']
                manual_sale_amount = offline_data['manual_sale']
                is_manual_sale = offline_data['is_manual_sale']
                offline_products = offline_data['products']
                created_date = offline_data['created_date']

                # handling the checkout section 
                data = Order()
                data.user = company_profile
                data.order_total = amount_paid
                data.order_number = order_number()
                data.is_ordered = True
                data.worker = worker
                data.created_date = created_date
                data.save()

                current_order = Order.objects.get(order_number = data.order_number, user = company_profile , worker = worker)
                business_name = BusinessProfile.objects.get( user_id = _company_account(request) , active = True)

                # creating payment
                ref = f"KIOSK_OFFLINE_SALE{transaction_ref()}"
                payment_ref = ref 
                payment = Payment.objects.create( user = company_profile, payment_ref = payment_ref, amount_paid = amount_paid, payment_method = payment_method , verified = True, status = "successful", cash_collected = cash_collected , customers_change = customers_change , created_date = created_date )
                current_order.payment = payment
                current_order.save()

                if is_manual_sale:
                    manual_sale = Merchant_Product.objects.get( product_name  = "Manual Sale" )
                    orderproduct = OrderProduct()
                    orderproduct.order_id = data.id
                    orderproduct.payment = payment
                    orderproduct.user = company_profile
                    orderproduct.product_id = manual_sale.id
                    orderproduct.product_price = manual_sale_amount
                    orderproduct.product_total_price = manual_sale_amount
                    orderproduct.ordered = True
                    orderproduct.worker = worker
                    orderproduct.created_date = created_date
                    orderproduct.save()
                    data.products.add(manual_sale.id)


                for items in offline_products:
                    
                    item = Merchant_Product.objects.get( id = items['product'])
                    weight_quantity = item.charge_by_weight
                    product_variation_category = items['product_variation'][0]['variations_category']
                    product_variation_value = items['product_variation'][0]['variation_value']
                    
                    orderproduct = OrderProduct()
                    orderproduct.order_id = data.id
                    orderproduct.payment = payment 
                    orderproduct.user = company_profile
                    orderproduct.product_id = item.id
                    orderproduct.product_price = item.price

                    if weight_quantity:
                        orderproduct.weight_quantity = Decimal( items['quantity'] )
                        orderproduct.product_total_price = Decimal( items['quantity'] ) * item.price
                    else:
                        orderproduct.quantity = items['quantity']
                        orderproduct.product_total_price = Decimal( items['quantity'] ) * item.price

                    orderproduct.ordered = True
                    orderproduct.worker = worker
                    orderproduct.save()

                    # if item.product_variation is not None:
                    variation_id = None
                    
                    try:
                        v_id = ProductVariation.objects.get( product_id = item.id , variations_category = product_variation_category, variation_value = product_variation_value )
                        variation_id = v_id.id
                    except ProductVariation.DoesNotExist:
                        pass
             
                    if variation_id is not None:
                        orderproduct = OrderProduct.objects.get(id = orderproduct.id)
                        orderproduct.variation.add(v_id)
                        orderproduct.save()

                        variation_quantity = ProductVariation.objects.get( product_id = item.id , id = variation_id)
                        if variation_quantity.quantity is not None:
                            if weight_quantity:
                                variation_quantity.weight_quantity -= Decimal(items['quantity'])
                            else:
                                variation_quantity.quantity -= int(items['quantity'])
                            variation_quantity.save()
                        # else:
                            # return Response({'status':'error','message':'Item variation is out of stock',} , status=status.HTTP_400_BAD_REQUEST)
                    
                    # reduce the quantity of the order item
                    try: 
                        product = Merchant_Product.objects.get( id = item.id )
                    except Merchant_Product.DoesNotExist:
                        return Response({'status':'error','message':'product id does not exist'}, status=status.HTTP_201_CREATED)

                    if weight_quantity:
                        product.weight_quantity -= Decimal(items['quantity'])
                    else:
                        product.stock -= int(items['quantity'])
                    product.save()

                    data.products.add(item.id)

            return Response({'status':'success','message':'offline checkout has been uploaded and processed successfully'}, status=status.HTTP_201_CREATED)

            # end of offline checkout

        return Response(serializer.errors,  status=status.HTTP_400_BAD_REQUEST)


class Offline_Product_UPload_View ( CreateAPIView ):
    permission_classes = [ IsAuthenticated, KOKPermission, ]
    serializer_class = Offline_Product_Upload

    def post (self, request, *args, **kwargs):
        company_profile = _company_account(request)

        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            product = serializer.data.get('offline_products')
            response_data = json.loads(json.dumps(product, cls=DjangoJSONEncoder))

            for offline_data in response_data:
                product_sku = offline_data['product_sku']
                product_name = offline_data['product_name']
                price = offline_data['price']
                cost_price = offline_data['cost_price']
                stock = offline_data['stock']
                weight_unit = offline_data['weight_unit']
                out_of_stock_notify = offline_data['out_of_stock_notify']
                low_stock_limit = offline_data['low_stock_limit']
                charge_by_weight = offline_data['charge_by_weight']
                weight_quantity = offline_data['weight_quantity']
                category = offline_data['category']
                products_variation = offline_data['products_variation']
                expire_notify = offline_data['expire_notify']
                expiring_date = offline_data['expiring_date']
                expiry_days_notify = offline_data['expiry_days_notify']
                image = offline_data['image']

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

                try:
                    category = Category.objects.get ( id = category)
                except Category.DoesNotExist:
                    return Response({'status':'error', 'message':'product category cant be found in our database'}, status=status.HTTP_400_BAD_REQUEST)

                if user_plan is not None :
                
                    if user_plan.plan.plan_name == "Basic":
                        count = Merchant_Product.objects.filter( user = company_profile ).count()
                        if count > 7:
                            return Response({'status':'error', 'message':'Your business account has exceeded it product limit kindly upgrade your package.'}, status=status.HTTP_400_BAD_REQUEST)
                            
                    elif user_plan.plan.plan_name == "Kiosk Plus":
                        count = Merchant_Product.objects.filter( user = company_profile ).count()
                        if count > 49:
                            return Response({'status':'error', 'message':'Your business account has exceeded it product limit kindly upgrade your package.'}, status=status.HTTP_400_BAD_REQUEST)
                    else:
                        pass
                else:
                    return Response({'status':'error', 'message':'Your business account has exceeded it product limit kindly upgrade your package.'}, status=status.HTTP_400_BAD_REQUEST)
                
                # user permissions end
                # 
                business_profile = BusinessProfile.objects.get( user = company_profile , active = True )
                 
                product = Merchant_Product.objects.create( product_sku = product_sku , product_name = product_name, price = price , cost_price = cost_price , stock = stock ,weight_quantity = weight_quantity , charge_by_weight = charge_by_weight , category = category , weight_unit = weight_unit , out_of_stock_notify = out_of_stock_notify , low_stock_limit = low_stock_limit , merchant_local_currency = request.user.default_currency_id , user = company_profile , image = image , business_profile = business_profile , expire_notify = expire_notify , expiring_date = expiring_date, expiry_days_notify = expiry_days_notify )
                
                for variation in products_variation:
                    if variation.get("variations_category" ) is not None:
                        variations = ProductVariation()
                        variations.variations_category = variation.get("variations_category" )
                        variations.variation_value = variation.get("variation_value" )
                        variations.quantity = variation.get("quantity" )
                        variations.weight_quantity = variation.get("weight_quantity" )
                        variations.product = product
                        variations.save()
                        
            return Response({'status': 'success','message':'Item has been uplaoded successfully'}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors,  status=status.HTTP_400_BAD_REQUEST)



class KroonAPP_Version (APIView):
    permission_classes = [ AllowAny, KOKPermission, ]

    def get (self, request, *args, **kwargs):
        # returning the app version for kroon
        return Response({'status':'success', 'message':'application version fetched successfully','kroon_version':'1.0.7', 'kiosk_version':'1.0.3'}, status=status.HTTP_201_CREATED)



class Customer_Support_Email (CreateAPIView):
    permission_classes = [ AllowAny, KOKPermission, ]
    serializer_class = Email_Support_Serializer
    def post (self, request, *args, **kwargs):

        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            customer_email = serializer.validated_data.get('customer_email')
            email_subject = serializer.validated_data.get('email_subject')
            message = serializer.validated_data.get('message')

            # sending email to customer care
            send_mail(
                f'{email_subject}',
                f'{message}',
                f'{customer_email}',
                ['support@mykroonapp.com'],
                fail_silently=False,
            )

            return Response({'status':'success', 'message':'support message sent successfully'}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors,  status=status.HTTP_400_BAD_REQUEST)

    
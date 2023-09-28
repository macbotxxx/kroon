from decimal import Decimal
import json
import random
import string
import threading
import requests
from datetime import timedelta, datetime
from datetime import date

from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.generics import  CreateAPIView, ListCreateAPIView, DestroyAPIView, GenericAPIView
from django.core.serializers.json import DjangoJSONEncoder
from rest_framework.views import APIView
from rest_framework import status, serializers
from django.conf import settings
from django.contrib.humanize.templatetags.humanize import intcomma

# django email settings
from django.core import mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from helpers.common.security import KOKPermission, KOKMerchantPermission
from transactions.api.serializers import KroonRequestDetails, KroonTokenRequestSerializer
from transactions.models import KroonTokenRequest
from .serializers import  ProductSerializer, AddToCartSerializer, GetCartSerializer, RemoveItemCartSerializer, CheckOutSerializer, NewAddToCartSerializer
from kiosk_cart.models import  Cart, CartItem, Order, Payment, OrderProduct
from kiosk_stores.models import Merchant_Product, ProductVariation
from kroon.users.models import BusinessProfile, User
from helpers.common.decorators import kiosk_pro_merchants
from notifications.tasks import mobile_push_notification 



# import translation list from kroon  
from transactions.models import Transactions


KIOSK_FCM_SERVER_KEY = settings.KIOSK_FCM_SERVER_KEY
# Generating random number...
def order_number():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))

def transaction_ref():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=25))

def cart_number():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=45))

def _user_account (request):
    try:
        BusinessProfile.objects.get ( user = request.user , active = True)
        user = request.user.name
    except BusinessProfile.DoesNotExist:
        worker = BusinessProfile.objects.select_related("user").filter( workers = request.user )
        if worker:
            user = request.user.name
        else:
            pass
    return user


def _company_account (request):
    try:
        business_profiles = BusinessProfile.objects.get ( user = request.user , active = True )
        business_profile = business_profiles.user
    except BusinessProfile.DoesNotExist:
        checking_business_profile = BusinessProfile.objects.select_related("user").filter( workers = request.user )
        if checking_business_profile:
            for b in checking_business_profile:
                # print(checking_business_profile)
                business_profile = b.user
        else:
            business_profile = None
    return business_profile


def _company_account_in_app (request):
    if request.session.has_key('email'):
        user_email = request.session['email']
        account_user = User.objects.get( email = user_email )
    else:
        user_email = None
    try:
        business_profiles = BusinessProfile.objects.get ( user = account_user , active = True )
        business_profile = business_profiles.user
    except BusinessProfile.DoesNotExist:
        checking_business_profile = BusinessProfile.objects.select_related("user").filter( workers = account_user )
        if checking_business_profile:
            for b in checking_business_profile:
                # print(checking_business_profile)
                business_profile = b.user
        else:
            business_profile = None
    return business_profile



class AddToCartView (ListCreateAPIView):
    permission_classes = [ IsAuthenticated, KOKPermission, KOKMerchantPermission ]
    serializer_class = NewAddToCartSerializer
    serializer_class_details = AddToCartSerializer
    
    def get(self, request, *args, **kwargs):
        company_profile =  _company_account(request)
        worker = _user_account(request)
        total = 0
        all_cart_items = CartItem.objects.filter(user=company_profile)
        serializer = GetCartSerializer(all_cart_items, many=True)
        for cart_item in all_cart_items:
            p = Merchant_Product.objects.get( id = cart_item.product_id )
            if p.charge_by_weight == True:
                quantity = cart_item.product.price * cart_item.weight_quantity
            else:
                quantity = cart_item.product.price * cart_item.quantity

            total += quantity

        grandtotal = total 
        return Response({'status':'success', 'message':'list of all current cart items','grand total':grandtotal, 'data':serializer.data},  status=status.HTTP_200_OK)
      
      
    def post (self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        company_profile =  _company_account(request)
        worker = _user_account(request)

        if serializer.is_valid():
            add_to_cart = serializer.data.get('add_to_cart')
            response_data = json.loads(json.dumps(add_to_cart, cls=DjangoJSONEncoder))
            variations = [] 

            for p in response_data:
                product_id = p['product']

                quantity = p['quantity']
                variation_category = p['product_variation'][0]['variations_category']
                variation_value = p['product_variation'][0]['variation_value']

                try:
                    variation = ProductVariation.objects.get(product_id = product_id , variation_value=variation_value,  variations_category=variation_category)
                    variations.append(variation)
                except ProductVariation.DoesNotExist:
                    variation = None
                    pass

                is_charge_weight = Merchant_Product.objects.get( id = product_id)
                weight_quantity = is_charge_weight.charge_by_weight
                
                is_cart_item_exist = CartItem.objects.filter(product_id=product_id, user = company_profile).exists() #checking if the product and variation exists
                if is_cart_item_exist:
                    cart_item = CartItem.objects.filter(product_id=product_id, user = company_profile ,  worker = worker)

                    if variation_category is not None:
                      
                        try:
                            item = CartItem.objects.get( product_id = product_id, product_variation = variation,  user = company_profile ,  worker = worker )
                            if weight_quantity:
                                item.weight_quantity += int( quantity )
                            else:
                                item.quantity += int( quantity )
                            item.save()

                        except CartItem.DoesNotExist:

                            if weight_quantity:
                                item = CartItem.objects.create(product_id = product_id, weight_quantity = quantity,  user = company_profile,  worker = worker )
                            else:
                                item = CartItem.objects.create(product_id = product_id, quantity = int(quantity),  user = company_profile,  worker = worker )

                            if variation:
                                item.product_variation.clear()
                                item.product_variation.add(variation)
                            item.save()
  
                    else:
                        print('nothing')
                        item = CartItem.objects.get( product_id = product_id , user = company_profile , product_variation = None,  worker = worker )

                        if weight_quantity:
                            item.weight_quantity += int( quantity )
                        else:
                            item.quantity += int(quantity)
                        item.save()

                else:

                    if weight_quantity:
                        cart_item = CartItem.objects.create( product_id = product_id, weight_quantity = quantity,  user = company_profile,  worker = worker )
                    else:
                        quantity = int(quantity)
                        cart_item = CartItem.objects.create(product_id = product_id, quantity = quantity,  user = company_profile,  worker = worker )
                    
                    if variation is not None: #adding product to cart
                        cart_item.product_variation.clear() # clearing the previous product variation
                        cart_item.product_variation.add(variation)
                    cart_item.save() 
                
                # return Response({'status':'error', 'message':'Product id dont not exist'},  status=status.HTTP_201_CREATED)
                
            return Response({'status':'success', 'message':'Product is been added updated successfully'},  status=status.HTTP_201_CREATED) 

        return Response(serializer.errors,  status=status.HTTP_400_BAD_REQUEST)



class RemoveItemCartView (CreateAPIView):
    permission_classes = [ IsAuthenticated, KOKPermission, KOKMerchantPermission ]
    serializer_class = RemoveItemCartSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        company_profile =  _company_account(request)

        
        if serializer.is_valid():
            product_id = serializer.data.get('product')
            try:
                # get the product
                is_cart_item_exist = CartItem.objects.get( product__id = product_id, user = company_profile ) #checking if the product and variation exists
                if is_cart_item_exist.quantity > 1:
                    is_cart_item_exist.quantity -= 1
                    is_cart_item_exist.save()
                    return Response({'status':'error', 'message':'Product quantity is reduced successfully', 'data':self.serializer_class(is_cart_item_exist).data},status=status.HTTP_201_CREATED) 
                else:
                    is_cart_item_exist.delete()
                    return Response({'status':'error', 'message':'Product is been deleted from cart list'},  status=status.HTTP_201_CREATED)
                 
            except CartItem.DoesNotExist:
                return Response({'status': 'error', 'message':'product id does not exist'},  status=status.HTTP_404_NOT_FOUND)

        return Response(serializer.errors,  status=status.HTTP_400_BAD_REQUEST)


class DeleteCartItem (DestroyAPIView):
    permission_classes = [ IsAuthenticated, KOKPermission , KOKMerchantPermission ]
   
    def delete(self, request, *args, **kwargs):
        company_profile =  _company_account(request)

        cart_id = kwargs.get('id')
        try:
            cart_item = CartItem.objects.get(id=cart_id, user=company_profile)
            cart_item.delete()
            return Response({'status':'success', 'message':'Product is been deleted from cart list'},  status=status.HTTP_201_CREATED)
        except CartItem.DoesNotExist:
            return Response({'status':'success', 'message':'cart id does not exist'}, status.HTTP_400_BAD_REQUEST)


class ClearCart (APIView):
    permission_classes = [ IsAuthenticated, KOKPermission , KOKMerchantPermission ]
    
    def get(self, request, *args, **kwargs):
        company_profile =  _company_account(request)

        cart = CartItem.objects.filter(user=company_profile)
        cart.delete()
        return Response({'status':'success', 'message':'cart items is cleared successfully'}, status=status.HTTP_201_CREATED)



class Kiosk_FastCheckout(CreateAPIView):
    permission_classes = [ IsAuthenticated, KOKPermission ]
    serializer_class = KroonTokenRequestSerializer
    serializer_details = KroonRequestDetails


    def post (self, request, *args, **kwargs):
        trans_ref = transaction_ref()
        serializer = KroonTokenRequestSerializer(data=request.data)
        if serializer.is_valid():
            kroon_token = serializer.data.get('amount_in_kroon_token')
            company_profile = _company_account(request)
            user_wallet_id = User.objects.get( email = company_profile )
            request_user = company_profile
            request_user_wallet_id  = user_wallet_id.wallet_id

            # creating token request transaction
            transaction_id = f"KROON_{trans_ref}"
          
            # Recipient Transactional Record History
            Transactions.objects.create(user = request_user ,  recipient = request_user,amount = kroon_token,transactional_id = transaction_id, currency = 'KC', narration = f'{request.user.name} requested for a {kroon_token} kroon token ', status = 'pending',  kroon_balance = request_user.kroon_token,action = 'FAST CHECKOUT')

            tokenRequest = KroonTokenRequest()
            tokenRequest.recipient = request_user
            tokenRequest.amount_in_kroon_token = Decimal(kroon_token)
            tokenRequest.transactional_id = transaction_id
            tokenRequest.wallet_id = request_user_wallet_id
            tokenRequest.action = "FAST CHECKOUT"
            tokenRequest.save()

            return Response({'status':'success', 'message':'fast checkout fees has been generated successfully.', 'data':self.serializer_details(tokenRequest).data},  status=status.HTTP_201_CREATED)

        return Response(serializer.errors,  status=status.HTTP_400_BAD_REQUEST)



class CheckoutView (CreateAPIView):
    permission_classes = [ IsAuthenticated, KOKPermission , KOKMerchantPermission ]
    serializer_class = CheckOutSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        company_profile =  _company_account(request)
        worker = _user_account(request)

        if serializer.is_valid():
            payment_method = serializer.data.get('payment_method')
            amount_paid = serializer.data.get('amount_paid')
            kroon_transaction_ref = serializer.data.get('kroon_transaction_ref')
            cash_collected = serializer.data.get('cash_collected')
            customers_change = serializer.data.get('customers_change')
            manual_sale_amount = serializer.data.get('manual_sale')
            is_manual_sale = serializer.data.get('is_manual_sale')
        
            # if the cart count is less than 1 , then redirect the customer to the store page

            cart_items = CartItem.objects.filter(user=company_profile , worker = worker)
            cart_count = cart_items.count()
            
            if not is_manual_sale:
                if cart_count <= 0:
                    return Response({'status':'error','message':'Cant checkout , Cart is empty'} , status=status.HTTP_404_NOT_FOUND)
                    
            # checking which payment method was used on the checkout process 
            payment_method_list = ['kroon_token']
            if payment_method in payment_method_list:
                Previous_Date = date.today()
                #BUG: adding created date verification to the current date transaction_
                try:
                    Transactions.objects.get( user = company_profile , transactional_id = kroon_transaction_ref , amount = amount_paid , status = 'successful' , created_date__date = Previous_Date)
                except Transactions.DoesNotExist:
                    return Response({'status':'error','message':'kroon payment record is not found'} , status=status.HTTP_404_NOT_FOUND)

                data = Order()
                data.user = company_profile
                data.order_total = amount_paid
                data.order_number = order_number()
                data.is_ordered = True
                data.worker = worker
                data.save()
                current_order = Order.objects.get(order_number = data.order_number, user = company_profile , worker = worker)
                business_name = BusinessProfile.objects.get( user_id = _company_account(request) , active = True)
                
                # creating payment
                ref = f"KIOSK_{transaction_ref()}"
                payment_ref = ref 
                payment = Payment.objects.create( user = company_profile, payment_ref = payment_ref, amount_paid = amount_paid, payment_method = payment_method , verified = True, status = "successful", cash_collected = cash_collected , customers_change = customers_change  )
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
                    orderproduct.save()
                    data.products.add(manual_sale.id)

            
                cart_items = CartItem.objects.filter( user = company_profile, worker = worker)
                for item in cart_items:

                    is_charge_weight = Merchant_Product.objects.get( id = item.product_id)
                    weight_quantity = is_charge_weight.charge_by_weight

                    orderproduct = OrderProduct()
                    orderproduct.order_id = data.id
                    orderproduct.payment = payment
                    orderproduct.user = company_profile
                    orderproduct.product_id = item.product_id
                    orderproduct.product_price = item.product.price

                    if weight_quantity:
                        orderproduct.weight_quantity = item.weight_quantity
                        orderproduct.product_total_price = item.weight_quantity * item.product.price
                    else:
                        orderproduct.quantity = item.quantity
                        orderproduct.product_total_price = item.quantity * item.product.price

                    orderproduct.ordered = True
                    orderproduct.worker = worker
                    orderproduct.save()

                    # if item.product_variation is not None:
                    variation_id = None
                    cart_item = CartItem.objects.get(id=item.id)
                    product_v = cart_item.product_variation.all()
                    for v in product_v:
                        variation_id = v.id
             
                    if variation_id is not None:
                        orderproduct = OrderProduct.objects.get(id = orderproduct.id)
                        orderproduct.variation.set(product_v)
                        orderproduct.save()

                        variation_quantity = ProductVariation.objects.get( product_id = item.product_id , id = variation_id)
                        if variation_quantity.quantity is not None:
                            if weight_quantity:
                                variation_quantity.weight_quantity -= item.weight_quantity
                            else:
                                variation_quantity.quantity -= item.quantity
                            variation_quantity.save()
                    
                    # reduce the quantity of the order item 
                    product = Merchant_Product.objects.get( id = item.product_id )
                    if weight_quantity:
                        product.weight_quantity -= item.weight_quantity
                    else:
                        product.stock -= item.quantity
                        
                    product.save()

                    data.products.add(item.product_id)
                    
                    # cleariing the cart item of the user
                    CartItem.objects.filter(id=item.id).delete()
                
                cartitem = OrderProduct.objects.filter( order__order_number = data.order_number )
                user_profile = User.objects.get ( email = company_profile )
                amount_sold = intcomma(amount_paid)

                # notification section for Kiosk Pro 
                if kiosk_pro_merchants(request) :
                    platform = "kiosk"
                    device_id = f'{user_profile.device_id}'
                    title = "COMPLETED SALE"
                    body = f'A {payment_method} sale of {amount_sold}{user_profile.default_currency_id} has been completed by {worker}'

                    # pushing notifications
                    # sending the mobile notifications
                    mobile_push_notification.delay(device_id = device_id, title = title, body = body , platform = platform )
                    #  sending email to the customer alerting him of the succesful order 
                    subject = f'Kiosk Successful Order - {company_profile.merchant_business_name}' 


                return Response({'status':'success','message':'Checkout is completed successfully', 'order_id':data.order_number} , status=status.HTTP_200_OK)


            else:
                              
                data = Order()
                data.user = company_profile
                data.order_total = amount_paid
                data.order_number = order_number()
                data.is_ordered = True
                data.worker = worker
                data.save()
                current_order = Order.objects.get(order_number = data.order_number, user = company_profile , worker = worker)
                business_name = BusinessProfile.objects.get( user_id = _company_account(request) , active = True)
                
                # creating payment
                ref = f"KIOSK_{transaction_ref()}"
                payment_ref = ref 
                payment = Payment.objects.create( user = company_profile, payment_ref = payment_ref, amount_paid = amount_paid, payment_method = payment_method , verified = True, status = "successful", cash_collected = cash_collected , customers_change = customers_change  )
                
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
                    orderproduct.save()
                    data.products.add(manual_sale.id)

                

                cart_items = CartItem.objects.filter( user = company_profile, worker = worker)
                for item in cart_items:

                    is_charge_weight = Merchant_Product.objects.get( id = item.product_id)
                    weight_quantity = is_charge_weight.charge_by_weight

                    orderproduct = OrderProduct()
                    orderproduct.order_id = data.id
                    orderproduct.payment = payment
                    orderproduct.user = company_profile
                    orderproduct.product_id = item.product_id
                    orderproduct.product_price = item.product.price

                    if weight_quantity:
                        orderproduct.weight_quantity = item.weight_quantity
                        orderproduct.product_total_price = item.weight_quantity * item.product.price
                    else:
                        orderproduct.quantity = item.quantity
                        orderproduct.product_total_price = item.quantity * item.product.price

                    orderproduct.ordered = True
                    orderproduct.worker = worker
                    orderproduct.save()

                    

                    # if item.product_variation is not None:
                    variation_id = None
                    cart_item = CartItem.objects.get(id=item.id)
                    product_v = cart_item.product_variation.all()
                    for v in product_v:
                        variation_id = v.id
             
                    if variation_id is not None:
                        orderproduct = OrderProduct.objects.get(id = orderproduct.id)
                        orderproduct.variation.set(product_v)
                        orderproduct.save()

                        variation_quantity = ProductVariation.objects.get( product_id = item.product_id , id = variation_id)
                        if variation_quantity.quantity is not None:
                            if weight_quantity:
                                variation_quantity.weight_quantity -= item.weight_quantity
                            else:
                                variation_quantity.quantity -= item.quantity
                            variation_quantity.save()
                        # else:
                            # return Response({'status':'error','message':'Item variation is out of stock',} , status=status.HTTP_400_BAD_REQUEST)
                    
                    # reduce the quantity of the order item 
                    product = Merchant_Product.objects.get( id = item.product_id )
                    if weight_quantity:
                        product.weight_quantity -= item.weight_quantity
                    else:
                        product.stock -= item.quantity
                    product.save()

                    data.products.add(item.product_id)
                    
                    # cleariing the cart item of the user
                    CartItem.objects.filter(id=item.id).delete()

                cartitem = OrderProduct.objects.filter( order__order_number = data.order_number )
                user_profile = User.objects.get ( email = company_profile )
                amount_sold = intcomma(amount_paid)

                if kiosk_pro_merchants(request):
                    
                    platform = "kiosk"
                    device_id = f'{user_profile.device_id}'
                    title = "COMPLETED SALE"
                    body = f'A {payment_method} sale of {amount_sold}{user_profile.default_currency_id} has been completed by {worker}'

                    # pushing notifications
                    # sending the mobile notifications
                    mobile_push_notification.delay(device_id = device_id, title = title, body = body , platform = platform )
                    #  sending email to the customer alerting him of the succesful order 
                    subject = f'Kiosk Successful Order - {company_profile.merchant_business_name}'
                    
                    # kiosk_checkout_email.delay( subject = subject , company_profile = company_profile , cartitem = cartitem , current_order = current_order , business_name = business_name , user_profile = user_profile )

                return Response({'status':'success','message':'Checkout is completed successfully', 'order_id':data.order_number} , status=status.HTTP_200_OK)

            return Response({'status':'error','message':'Payment method not found'} , status=status.HTTP_404_NOT_FOUND)
        
        return Response(serializer.errors,  status=status.HTTP_400_BAD_REQUEST)



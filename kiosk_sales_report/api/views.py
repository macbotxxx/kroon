import datetime
import pytz

from rest_framework.response import Response
from decimal import Decimal
from helpers.common.security import KOKPermission , KOKMerchantPermission
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.generics import ListAPIView , CreateAPIView, UpdateAPIView, get_object_or_404
from django.db.models import Q
from rest_framework import  status
from django.db.models import Count , Sum
from django.db.models import Avg
from kroon.users.models import BusinessProfile
from django.utils import timezone
from datetime import timedelta, datetime
from datetime import date
from django_filters import rest_framework as filters

from kroon.users.models import User, UserWrongPinValidate
from kiosk_stores.models import Merchant_Product
from kiosk_cart.models import Order,OrderProduct
from subscriptions.models import Subscription_Plan ,Merchant_Subcribers
from kiosk_cart.models import OrderProduct ,Order ,Payment
from kroon.users.pagination import StandardResultsSetPagination

from .serializers import List_Of_Sales_Serializer, SaleDetailsSerializer , SalesListFilter
from rest_framework.views import APIView

from kiosk_cart.api.views import _company_account, _user_account

utc=pytz.UTC

from datetime import date, datetime, timezone



class List_Of_Sales_Views (ListAPIView):
    permission_classes = [ IsAuthenticated, KOKPermission ]
    serializer_class = List_Of_Sales_Serializer
    queryset = Order.objects.all()
    pagination_class = StandardResultsSetPagination
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = SalesListFilter
    


    def list (self, request, *args, **kwargs):
        company_profile = _company_account(request)
        sales = self.get_queryset().select_related("user", "payment").filter( user = company_profile, is_ordered = True ).order_by('-created_date')
        sales_filter = self.filter_queryset(sales)
        page = self.paginate_queryset(sales_filter)
        serializer = self.serializer_class(page, many=True)
        return self.get_paginated_response(serializer.data)
       

class Sale_detailsView ( APIView ):
    permission_classes = [ IsAuthenticated , KOKPermission ]
    serializer_class = SaleDetailsSerializer

    def post(self, request, *args, **kwargs):
        order_id = kwargs.get('order_id')
        
        sale = OrderProduct.objects.select_related("user", "payment", "order", "product").filter( ordered = True , order__order_number = order_id )

        if not sale.exists():
            return Response({'status':'error','message':'order id does not exist'}, status=status.HTTP_404_NOT_FOUND)

        serializer = SaleDetailsSerializer(sale, many=True)
        return Response({'status':'success','message':'sales details fetched succesfully', 'data':serializer.data}, status = status.HTTP_200_OK)
    

class Refund_Product ( APIView ):
    permission_classes = [ IsAuthenticated , KOKPermission ]
    serializer_class = SaleDetailsSerializer

    def post (self, request, *args, **kwargs):
        order_id = kwargs.get('order_id')
        product_sku = kwargs.get('product_sku')
        product_quantity = kwargs.get('product_quantity')

        # getting the product and validate it 😏
        try:
            # getting the product
            product_info = Merchant_Product.objects.get( product_sku = product_sku )
            # getting the order
            product_order = Order.objects.select_related("user", "payment").get( is_ordered = True , order_number = order_id )

            refund_item = OrderProduct.objects.select_related("user", "payment", "order", "product").get( ordered = True , order__order_number = order_id , product__product_sku = product_sku , refund = False )

        except OrderProduct.DoesNotExist:
            return Response({'status':'error','message':'order or product does not exist in the merchants sales record , or it has already been refund'}, status=status.HTTP_404_NOT_FOUND)

        except Merchant_Product.DoesNotExist:
            return Response({'status':'error','message':'the product sku dont not exist'}, status=status.HTTP_404_NOT_FOUND)

        except Order.DoesNotExist:
            return Response({'status':'error','message':'the order id dont not exist or its incorrect'}, status=status.HTTP_404_NOT_FOUND)
        


        # checking if the product is messured by quantity or by weight
        if refund_item.product.charge_by_weight:
            quantity = Decimal(product_quantity)
            refund_product_price = refund_item.product_price * quantity
            # updating the refund product record
            refund_item.refund_weight_quantity -= quantity
            refund_item.refund_product_price = refund_product_price
            # subtracting the product price from the record
            refund_item.product_total_price -= refund_product_price
            product_order.order_total -= refund_product_price
            # updating the product quantity record
            product_info.weight_quantity += quantity
            # updating payment model 
            payment = Payment.objects.get( payment_ref = refund_item.payment.payment_ref  )
            payment.cash_collected -= refund_product_price
            payment.amount_paid -= refund_product_price
            payment.save()
            
        else:
            quantity = int(product_quantity)
            refund_product_price = refund_item.product_price * quantity
            # updating the refund product record
            refund_item.refund_quantity = quantity
            refund_item.refund_product_price = refund_product_price
            # subtracting the product price from the record
            refund_item.product_total_price -= refund_product_price
            product_order.order_total -= refund_product_price
            # updating the product quantity record
            product_info.stock += quantity
            # updating payment model 
            payment = Payment.objects.get( payment_ref = refund_item.payment.payment_ref  )
            payment.cash_collected -= refund_product_price
            payment.amount_paid -= refund_product_price
            payment.save()

        # refund the product
        refund_item.refund = True
        refund_item.save()

        # update the product
        product_info.save()
        # updating the order
        product_order.save()


        serializer = self.serializer_class(refund_item)

        return Response({'status':'success','message':'ordered product has been refunded succesfully', 'data':serializer.data}, status = status.HTTP_200_OK)
    

class Refund_Order ( APIView ):
    permission_classes = [ IsAuthenticated , KOKPermission ]
    serializer_class = List_Of_Sales_Serializer

    def post (self, request, *args, **kwargs):
        order_id = kwargs.get('order_id')
        # getting the product and validate it
        try:
            refund_order = Order.objects.select_related("user", "payment").get( is_ordered = True , order_number = order_id )

        except Order.DoesNotExist:
            return Response({'status':'error','message':'order has been refund or does not exist in the marchants sales record'}, status=status.HTTP_404_NOT_FOUND)
        

        refund_item = OrderProduct.objects.select_related("user", "payment", "order", "product").filter( ordered = True , order__order_number = order_id )

        for order_info in refund_item:
            # getting the product TODO:
            product_info = Merchant_Product.objects.get( product_sku = order_info.product.product_sku )
            # checking if the product is messured by quantity or by weight
            if order_info.product.charge_by_weight:
                quantity = order_info.refund_weight_quantity
                refund_product_price = order_info.product_price * quantity
                # updating the refund product record
                order_info.refund_weight_quantity -= quantity
                order_info.refund_product_price = refund_product_price
                # subtracting the product price from the record
                order_info.product_total_price -= refund_product_price
                order_info.refund = True
                refund_order.order_total = refund_product_price
                # updating the product quantity record
                product_info.weight_quantity += quantity
                # # refund the product
                refund_order.refund = True
                refund_order.save()
                # update the product
                product_info.save()
                order_info.save()
                
            else:
                quantity = int(order_info.quantity)
                refund_product_price = order_info.product_price * quantity
                # updating the refund product record
                order_info.refund_quantity = quantity
                order_info.refund_product_price = refund_product_price
                # subtracting the product price from the record
                order_info.product_total_price -= refund_product_price
                refund_order.order_total -= refund_product_price
                order_info.refund = True
                # updating the product quantity record
                product_info.stock += quantity
                # # refund the product
                refund_order.refund = True
                refund_order.save()
                # update the product
                product_info.save()
                order_info.save()

        serializer = self.serializer_class(refund_order)

        return Response({'status':'success','message':'ordered sale has been refunded succesfully', 'data':serializer.data}, status = status.HTTP_200_OK)


class Sales_Report (APIView):
    """
    NOTE: this section hold the necessary information for the merchant
    analysis , which is consist of the total sales and all inventory data.
    """

    permission_classes = [ IsAuthenticated, KOKPermission , KOKMerchantPermission ]
    serializer_class = None
    
    def get (self, request, *args, **kwargs):
        company_profile = _company_account(request)
        business_profile = BusinessProfile.objects.get( user = company_profile , active = True )
        card_sales = 0
        cash_sales = 0
        kroon_sales = 0
        total_sales = 0
        daily_card_sales = 0
        daily_cash_sales = 0
        daily_kroon_sales = 0
        daily_total_sales = 0
        inventory_health_check = "Poor"

        #Getting the current date in local time format
        today = datetime.today().date()
        yesterday = today 

            
        # inventory health check
        all_items = Merchant_Product.objects.select_related("user").filter( user = company_profile , business_profile = business_profile)
        items_count = all_items.count()
        if items_count < 0:
            inventory_health_check = "Poor"
        elif items_count > 1:
            inventory_health_check = "Avarage"
        elif items_count > 50:
            inventory_health_check = "Healthy"
        
        inventory_health = inventory_health_check

        # getting all cash payments and also the daily sales 
        sales = Order.objects.select_related("user", "payment").filter( user = company_profile, is_ordered = True , payment__payment_method = "cash_payment" )
        for i in sales:
            cash_sales += i.order_total
        total_cash_sales = Decimal(cash_sales)
        cash_sales_count = sales.count()

        daily_sales = Order.objects.select_related("user", "payment").filter(  user = company_profile, is_ordered = True , payment__payment_method = "cash_payment" , created_date__date = today )
        for i in daily_sales:
            daily_cash_sales += i.order_total
        daily_total_cash_sales = Decimal(daily_cash_sales)
        daily_cash_sales_count = daily_sales.count()


        # getting all card payments
        sales = Order.objects.select_related("user", "payment").filter(  user = company_profile, is_ordered = True , payment__payment_method = "card_payment" )
        for i in sales:
            card_sales += i.order_total
        total_card_sales = Decimal(card_sales)
        card_sales_count = sales.count()

        daily_sales = Order.objects.select_related("user", "payment").filter( user = company_profile, is_ordered = True , payment__payment_method = "card_payment" , created_date__date = today )
        for i in daily_sales:
            daily_card_sales += i.order_total
        daily_total_card_sales = Decimal(daily_card_sales)
        daily_card_sales_count = daily_sales.count()


        # getting all kroon payments
        sales = Order.objects.select_related("user", "payment").filter( user = company_profile, is_ordered = True , payment__payment_method = "kroon_payment" )
        for i in sales:
            kroon_sales += i.order_total
        total_kroon_sales = Decimal(kroon_sales)
        kroon_sales_count = sales.count()

        daily_sales = Order.objects.select_related("user", "payment").filter( user = company_profile, is_ordered = True , payment__payment_method = "kroon_payment" , created_date__date = today)
        for i in daily_sales:
            daily_kroon_sales += i.order_total
        daily_total_kroon_sales = Decimal(daily_kroon_sales)
        daily_kroon_sales_count = daily_sales.count()


         # getting all kroon payments
        sales = Order.objects.select_related("user", "payment").filter( user = company_profile, is_ordered = True , payment__payment_method = "mobile_money_payment" )
        for i in sales:
            kroon_sales += i.order_total
        total_mobile_money_sales = Decimal(kroon_sales)
        mobile_money_sales_count = sales.count()

        daily_sales = Order.objects.select_related("user", "payment").filter( user = company_profile, is_ordered = True , payment__payment_method = "mobile_money_payment" , created_date__date = today)
        for i in daily_sales:
            daily_kroon_sales += i.order_total
        daily_total_mobile_money_sales = Decimal(daily_kroon_sales)
        daily_mobile_money_sales_count = daily_sales.count()


        # getting all ordered items
        sales = Order.objects.select_related("user", "payment").filter( user = company_profile, is_ordered = True )
        all_order_count = sales.count()

        daily_sales = Order.objects.select_related("user", "payment").filter( user = company_profile, is_ordered = True , created_date__date = today )
        daily_all_order_count = daily_sales.count()

        # getting the percentage of the sales
        yesterday_quantity = 0
        yesterday_sale = OrderProduct.objects.select_related("user", "payment", "order", "product").filter( user = company_profile, ordered = True , created_date__date = yesterday)

        for t in yesterday_sale:
            if t.product.charge_by_weight == True:
                yesterday_quantity += t.weight_quantity
            else:
                yesterday_quantity += t.quantity
        yesterday_sale_count = yesterday_quantity
        
        today_quantity = 0
        today_sale_count = 0
        today_sale = OrderProduct.objects.select_related("user", "payment", "order", "product").filter( user = company_profile, ordered = True , created_date__date = today )

        for t in today_sale:
            if t.product.charge_by_weight == True:
                yesterday_quantity += t.weight_quantity
            else:
                yesterday_quantity += t.quantity
        today_sale_count = yesterday_quantity

        # calculating an Avarage
        mic = today_sale.aggregate(Avg("quantity"))
        print(mic)


        quantity = 0
        all_products = Merchant_Product.objects.select_related("user", "category").filter( user = company_profile , business_profile = business_profile )
        for p in all_products:
            if p.charge_by_weight == True:
                quantity += p.weight_quantity
            else:
                quantity += p.stock
        all_products_count = quantity
        


        try:
            daily_sales_percentage = (today_sale_count / all_products_count) * 100
            # yesterday_sale_percentage = (yesterday_sale_count / all_products_count) * 100
            
        except ZeroDivisionError:
            daily_sales_percentage = 0
            yesterday_sale_percentage = 0

        # if yesterday_sale_percentage > daily_sales_percentage:
        #     percentage = format(daily_sales_percentage, '.2f')
        #     sale_percentage = f'-{percentage}'
        # elif yesterday_sale_percentage < daily_sales_percentage:
        #     percentage = format(daily_sales_percentage, '.2f')
        #     sale_percentage = f'+{percentage}'
        # else:
        percentage = format(daily_sales_percentage, '.2f')
        sale_percentage = f'{percentage}'

        
        # stock report
        """
        here goes the stock report section 
        """
        total_uploaded_products = Merchant_Product.objects.select_related("user", "category").filter( user = company_profile , business_profile = business_profile ).count()

        # getting the best selling products  
        most_sold_products = OrderProduct.objects.select_related('user', 'payment', 'products' , 'order').filter(user = company_profile ).values('ordered', 'product__product_name','product__image','product__price','product__cost_price',).annotate(total = Count('ordered') , total_revenue = Sum('product_total_price')).order_by('-ordered')[:5]


        cost_sales_total = 0
        sale_cost_price = 0
        total_sales_cost_price  = OrderProduct.objects.select_related("user", "payment", "order", "product").filter( user = company_profile, ordered = True )

        for t in total_sales_cost_price:
            sale_cost_price += t.product.cost_price
            if t.product.charge_by_weight == True:
                yesterday_quantity += t.weight_quantity
            else:
                yesterday_quantity += t.quantity
        cost_sales_total = yesterday_quantity * sale_cost_price

        


        # calculating all sales 
        total_sales = total_cash_sales + total_card_sales + total_kroon_sales + total_mobile_money_sales
        daily_total_sales = daily_total_cash_sales + daily_total_card_sales + daily_total_kroon_sales

        daily_report_data = {'sale_percentage':{'percentage':sale_percentage},'total_sales':{'kroon_sales':daily_total_kroon_sales, 'cash_sale':daily_total_cash_sales, 'card_sales':daily_total_card_sales,'mobile_money_sales':daily_total_mobile_money_sales ,'total_sales':daily_total_sales},  'sales_count':{'kroon_sales_count': daily_kroon_sales_count, 'card_sales_count':daily_card_sales_count, 'cash_sales_count':daily_cash_sales_count,'mobile_money_sales_count':daily_mobile_money_sales_count }, 'inventory':{'inventory_health':inventory_health,'uploaded_items':items_count, 'all_orders_count':daily_all_order_count} }

        all_report_data = {'total_sales':{'kroon_sales':total_kroon_sales, 'cash_sale':total_cash_sales, 'card_sales':total_card_sales,'mobile_money_sales':total_mobile_money_sales, 'total_sales':total_sales},  'sales_count':{'kroon_sales_count': kroon_sales_count, 'card_sales_count':card_sales_count, 'cash_sales_count':cash_sales_count ,'mobile_money_sales_count':mobile_money_sales_count}, 'inventory':{'inventory_health':inventory_health,'uploaded_items':items_count, 'all_orders_count':all_order_count} } 

        

        data = {'daily_report_data':daily_report_data, 'all_report_data':all_report_data}
        stock_data = {'total_uploaded_products':total_uploaded_products, 'most_sold_products':most_sold_products, 'cost_sales_total':cost_sales_total}

        return Response({'status':'success','message':'All total sales fetched successfully','data':data, 'stock_report':stock_data} , status = status.HTTP_200_OK )




class Business_Financial_Reports ( APIView ):
    """
    This function has been implemented to provide the merchant 
    financial reports and business reports as well.
    it will be appended the a general parameter 
    """
    permission_classes = [ IsAuthenticated, KOKPermission , KOKMerchantPermission ]
    serializer_class = None

    def get (self, request ):
        # append list of business and financial reports
        business_report = []
        financial_report = []

        # getting the best selling products  
        best_sale = OrderProduct.objects.select_related('user', 'payment', 'products' , 'order').filter(user__id = request.user.id , ordered = True ).values('product__product_name').annotate(total = Count('ordered') , total_amount = Sum('product_total_price')).order_by('-total')[:9]

        try:
            user_plan = Merchant_Subcribers.objects.get( user = request.user , active = True )
        except Merchant_Subcribers.DoesNotExist :
            user_plan = None
        day_limit = 2
        if user_plan is not None :
            if user_plan.plan.plan_name == "Basic":
                day_limit = 2
            else:
                day_limit = 14
        else:
            pass


        day_limit = int(day_limit)
        days = []
        daily_cash_sales = []
        daily_card_sales = []
        daily_kroon_sales = []
        daily_mobile_money_sales = []
        daily_sales = []

        for i in range(day_limit):
            Previous_Date = date.today()  - timedelta(days=i)
            # print(Previous_Date.strftime("%b"))
            days.append(Previous_Date.strftime("%d %b"))


            # getting card sales daily
            card_daily_payment_sale = Payment.objects.select_related("user").filter(  user = request.user, verified = True , payment_method ='card_payment' , created_date__date  = Previous_Date).count()
            daily_card_sales.append(card_daily_payment_sale)


            # getting cash sales daily
            cash_daily_payment_sale = Payment.objects.select_related("user").filter(  user = request.user, verified = True , payment_method ='cash_payment' , created_date__date  = Previous_Date).count()
            daily_cash_sales.append(cash_daily_payment_sale)

            # getting kroon sales daily
            kroon_daily_payment_sale = Payment.objects.select_related("user").filter(  user = request.user, verified = True , payment_method ='kroon_payment' , created_date__date  = Previous_Date).count()
            daily_kroon_sales.append(kroon_daily_payment_sale)

            # getting mobile_money sales daily
            mobile_money_daily_payment_sale = Payment.objects.select_related("user").filter(  user = request.user, verified = True , payment_method ='mobile_money_payment' , created_date__date  = Previous_Date).count()
            daily_mobile_money_sales.append(mobile_money_daily_payment_sale)

            # daily sales 
            daily_sales_record = Order.objects.select_related("user", "payment").filter(  user = request.user, is_ordered = True , created_date__date  = Previous_Date ).count()
            daily_sales.append(daily_sales_record)

        # getting all payment sales revenue for each merchant
        merchant_revenue = Payment.objects.select_related('user').filter( user_id = request.user.id ).values( 'payment_method' ).annotate( total_revenue = Sum('amount_paid') ).order_by('-verified')
        # monthly report 
        # months = []
        monthly_data = []
        monthly_financial_data = []

        monthly_sales_data = Order.objects.filter( user = request.user,  is_ordered = True).extra({'created': "to_char(created_date, 'YYYY/MM')"}).values('created').annotate(created_count=Count('id')).order_by('-created')[:10]

        monthly_sales = Order.objects.filter( user = request.user,  is_ordered = True).extra({'created': "to_char(created_date, 'YYYY/MM')"}).values('created').annotate(created_count=Sum('order_total')).order_by('-created')[:10]

        for m in monthly_sales_data:            
            monthly_data.append(m)

        for mn in monthly_sales:
            monthly_financial_data.append(mn)

        business_reports = {
        'daily_sales':daily_sales,
        # daily payment sales_count
        'kroon_daily_payment_sale':daily_kroon_sales,
        'cash_daily_payment_sale':daily_cash_sales,
        'card_daily_payment_sale':daily_card_sales,
        'mobile_money_daily_payment_sale':daily_mobile_money_sales,
        # count
        'best_sale':best_sale,
        'days':days,
        # total revenue
        'merchant_revenue':merchant_revenue,
        'business_monthly_record':monthly_data,   

        }   


        """
        this is the financial report section ... 
        which will also be appended to the response
        """

        # getting the days remite
        day_limit = 20
        days = []
        daily_sales = []

        for i in range(day_limit):
            Previous_Date = date.today()  - timedelta(days=i)
            days.append(Previous_Date.strftime("%d %b"))

            recent_sale = Payment.objects.select_related("user",).filter(  user = request.user, verified = True, created_date__date =  Previous_Date )
            
            total_amount = 0
            for r in recent_sale:
                total_amount += r.amount_paid

            daily_sales.append(total_amount)

        # working on the subscriptions restrictions
     
        
        financial_reports = {
            'recent_sale':daily_sales,
            'days':days,
            'financial_monthly_record':monthly_financial_data,   
        }

        # appending reports 
        business_report.append( business_reports )
        financial_report.append( financial_reports )

        data = { 'business_report':business_report , 'financial_report':financial_report }

        return Response({'status':'successful', 'message':'this shows all the business and financial reports for the current merchant' , 'data':data }, status=status.HTTP_200_OK)
        
    








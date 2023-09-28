# import DRF packages
from decimal import Decimal
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import   ListCreateAPIView,  DestroyAPIView, ListAPIView
from rest_framework import status
from django.conf import settings
from django.db.models import Sum
from datetime import datetime, timedelta
from django.utils import timezone
from django.db.models import Q

# import app models 
from helpers.common.security import KOKPermission, KOKMerchantPermission
from kiosk_business_plan.models import Business_Plan , BusinessPlanExpenses
from kroon.users.models import BusinessProfile
from kiosk_cart.models import OrderProduct

# import serailizers 
from .serializers import BusinessPlanFormSerializers, BusinessPlanIDSerializers, BusinessPlanExpensesSerializer
from kiosk_cart.api.serializers import ProductDetails
from kiosk_categories.api.serializers import Category_Serializer


class BusinessPlanView(ListCreateAPIView):
    permission_classes = [IsAuthenticated,KOKPermission, KOKMerchantPermission,]
    serializer_class = BusinessPlanFormSerializers
    queryset = Business_Plan.objects.all()
    profile_qs = BusinessProfile.objects.all()
    bp_serializer = BusinessPlanIDSerializers

    def post(self, request, *args, **kwargs):
        serializers = self.serializer_class( data = request.data )
        if serializers.is_valid():
            qs = self.profile_qs.get ( user = request.user , active = True)
            expenses = serializers.validated_data.pop('business_expenses')
            
            business_profile = serializers.save(
            user = request.user,
            business_name = qs.business_name,
            business_logo = qs.business_logo,
            business_registration_number = qs.business_registration_number,
            business_contact = qs.business_contact_number,
            business_address = qs.business_address,
            business_owner_name = request.user.name,
            business_owner_contact = request.user.contact_number,
            business_owner_email = request.user.email,
            business_type = qs.business_type,
            )

            # checking if the merchant input any expenses
            for i in expenses:
                if i.get("expenses"):
                    expense = i.get("expenses")
                    expense_amount = i.get("expenses_amount")
                    # save the business plan expenses
                    business_ex = BusinessPlanExpenses()
                    business_ex.user = self.request.user
                    business_ex.business_plan = business_profile
                    business_ex.expenses = expense
                    business_ex.expenses_amount = expense_amount
                    business_ex.save()
                    business_profile.business_expenses.add(business_ex)

            # return response 
            return Response({'status': 'successful', 'message':'merchants business plan has been submitted and been generated successfully', 'data': serializers.data }, status=status.HTTP_201_CREATED)
        
        return Response(serializers.errors , status=status.HTTP_400_BAD_REQUEST)
    

    def get(self, request, *args, **kwargs):
        qs = self.get_queryset().filter( user = request.user )
        serializers = self.bp_serializer(qs , many=True)
        # return response 
        return Response({'status': 'successful', 'message':'merchants business plan has been fetched and been generated successfully', 'data': serializers.data}, status=status.HTTP_201_CREATED)


class BusinessPlanDeleteView(DestroyAPIView):
    permission_classes = [IsAuthenticated,KOKPermission, KOKMerchantPermission,]
    serializer_class = BusinessPlanFormSerializers
    queryset = Business_Plan.objects.all()
    lookup_field = "id"
    


class GeneratedBusinessPlanView(ListAPIView):
    permission_classes = [IsAuthenticated,KOKPermission, KOKMerchantPermission,]
    serializer_class = BusinessPlanFormSerializers
    queryset = Business_Plan.objects.all()

    def get(self, request ,*args, **kwargs):
        report_id = kwargs.pop('report_id')
        date_join = request.user.date_joined
        business_plan_record = self.get_queryset().get( user = request.user , id = report_id  )

        business_category = business_plan_record.business_category
        business_name = business_plan_record.business_name
        business_registration_number = business_plan_record.business_registration_number
        business_contact = business_plan_record.business_contact
        business_address = business_plan_record.business_address
        business_owner_name = business_plan_record.business_owner_name
        business_owner_contact = business_plan_record.business_owner_contact
        business_type = business_plan_record.business_type
        year_of_operation = business_plan_record.year_of_operation
        number_of_employees = business_plan_record.number_of_employees
        period_of_report = business_plan_record.period_of_report
        business_owner_email = business_plan_record.business_owner_email
        business_logo = business_plan_record.business_logo

        if business_logo:
            business_logo_image = business_logo.url
        else:
            business_logo_image = None

        # Getting the days of the month
        days_of_the_month = 30 * int(period_of_report)
        # Calculate the date two months ago from today
        months_ago = timezone.now() - timedelta(days = int(days_of_the_month))
        # Calculate the current date
        current_date = timezone.now()

        print(f'this is the months ago --- {months_ago}===== current day {current_date}')

        business_category_S = Category_Serializer(business_category , many=True ) 

        total_sales_price = 0
        total_cost_price = 0
        total_ordered_items_price = 0
        total_purchase = 0
        total_quantity = 0
        product_selling_price = 0
        sales = OrderProduct.objects.select_related("user", "payment", "order", "product").filter( Q(created_date__gte = months_ago ) & Q(created_date__lte=current_date), ordered = True , user = request.user )
        for s in sales:
            # calculating for the total cost price
            total_cost_price += s.product.cost_price * s.quantity
            total_quantity += s.quantity
            product_selling_price += s.product.price
            total_ordered_items_price += s.product_total_price
        total_purchase = total_ordered_items_price
        # getting the total sales price 
        total_sales_price = total_quantity * s.product.price

        gross_profit_n_loss  = total_sales_price - total_purchase

        total_sales_period = total_purchase #total sales 
        total_cost_of_sales_period = total_cost_price #total cost sale for the merchant
        total_gross_profits_for_period = total_sales_period - total_cost_of_sales_period # calculating the total gross profit for the period the merchant has sold his products
        
        # merchants static response data
        salaries = business_plan_record.salaries * Decimal(business_plan_record.period_of_report)
        data = business_plan_record.data * Decimal(business_plan_record.period_of_report)
        electricity = business_plan_record.electricity * Decimal(business_plan_record.period_of_report)
        fuel = business_plan_record.fuel * Decimal(business_plan_record.period_of_report)
        # merchants static response data - ends here 

        # implementation of the new expenses
        # calculating the merchants total expense 
        expenses = BusinessPlanExpenses.objects.filter ( user = self.request.user , business_plan = report_id )
        all_expenses = 0
        for e in expenses:
            all_expenses += e.expenses_amount
        total_of_all_above_expenses = all_expenses * int(period_of_report)
        expenses_response = BusinessPlanExpensesSerializer( expenses , many=True )
        # expenses implementation ends here 
        # getting the net profit loss 
        net_profit_loss = total_gross_profits_for_period - total_of_all_above_expenses

        max_record = OrderProduct.objects.select_related("user", "payment", "order", "product").filter(Q(created_date__gte = months_ago ) & Q(created_date__lte=current_date), ordered = True , user = request.user ).values("payment__payment_method").annotate(total_revenue=Sum('product_total_price'))

        cash_sales = 0
        card_sales = 0
        kroon_sales = 0
        mobile_payment_sales = 0
       
        for pm in max_record:
            if pm['payment__payment_method'] == "card_payment":
                card_sales += pm['total_revenue']
            if pm['payment__payment_method'] == "cash_payment":
                cash_sales += pm['total_revenue']
            if pm['payment__payment_method'] == "kroon_payment":
                kroon_sales += pm['total_revenue']
            if pm['payment__payment_method'] == "mobile_money_payment":
                mobile_payment_sales += pm['total_revenue']
        
        # best selling 
        best_sold_item = 0 
        best_sold_item_price = 0 
        total_sold = 0 
        s_products = [] 
        best_sold = OrderProduct.objects.select_related("user","order","product", "payment").filter( user = request.user, ordered = True ).annotate(quantity_sum=Sum('quantity')).order_by('-quantity_sum')[:1]
        
        for i in best_sold:
            best_sold_item = i.product 
            best_sold_item_price = i.product.price
            total_sold += i.product_total_price 
            s_products.append( best_sold_item)
        best_sold_item_S = ProductDetails( s_products , many = True ) #using product serialization


        # worst selling 
        worst_sold_item = 0  
        worst_sold_item_price = 0 
        worst_total_sold = 0
        w_products = [] 

        worst_sold = OrderProduct.objects.select_related("user","order","product", "payment").filter( user = request.user, ordered = True ).annotate(quantity_sum=Sum('quantity')).order_by('quantity_sum')[:1]
        for i in worst_sold:
            worst_sold_item =i.product
            worst_sold_item_price = i.product.price
            worst_total_sold += i.product_total_price 
            w_products.append( worst_sold_item )

        Worst_sold_item_S = ProductDetails(w_products , many = True ) #using product serialization

        card_sale_pecentage = 0
        cash_sale_pecentage = 0
        kroon_sale_pecentage = 0
        mobile_money_sale_pecentage = 0

        try:
            card_sale_pecentages = (card_sales / total_ordered_items_price) * 100
            card_sale_pecentage = format(card_sale_pecentages, '.2f')

            cash_sale_pecentages = (cash_sales / total_ordered_items_price) * 100
            cash_sale_pecentage = format(cash_sale_pecentages, '.2f')

            kroon_sale_pecentages = (kroon_sales / total_ordered_items_price) * 100
            kroon_sale_pecentage = format(kroon_sale_pecentages, '.2f')

            mobile_money_sale_pecentages = (mobile_payment_sales / total_ordered_items_price) * 100
            mobile_money_sale_pecentage = format(mobile_money_sale_pecentages, '.2f')
                
        except ZeroDivisionError:
            card_sale_pecentage = 0
            cash_sale_pecentage = 0
            mobile_money_sale_pecentage = 0
            kroon_sale_pecentage = 0

        net_profits_n_Loss =  total_gross_profits_for_period - total_of_all_above_expenses 

        # percentage 
        # year_percentage = (total_ordered_items_price/100) * 15
        # sale_one_year = format(year_percentage, '.2f') 
        # c = sale_one_year * 12

        # sale_two_year = format(year_percentage, '.2f') 

        sale_one_year = total_ordered_items_price * 12
        p = (15 * sale_one_year)/100 
        sale_one_year_percentage = sale_one_year + p
        
        sale_two_year = total_ordered_items_price * 24
        p = (15 * sale_two_year)/100 
        sale_two_year_percentage = sale_two_year + p
        

        cost_of_sale = total_cost_of_sales_period * 12
        p = (15 * cost_of_sale)/100
        cost_of_sale_per_year = cost_of_sale + p

        cost_two_sale = total_purchase * 24
        p = (15 * cost_two_sale)/100 
        cost_of_sale_2_years = cost_two_sale + p

        gross_for_a_year = sale_one_year_percentage - cost_of_sale_per_year
        gross_for_two_year = sale_two_year_percentage - cost_of_sale_2_years

        expensive_for_a_year = total_of_all_above_expenses * 12
        p = (15 * expensive_for_a_year)/100
        expensive_for_a_year_per_year = expensive_for_a_year + p

        expensive_for_two_years = total_of_all_above_expenses * 24
        p = (15 * expensive_for_two_years)/100
        expensive_for_two_year = expensive_for_two_years + p

        net_profit = total_gross_profits_for_period - total_of_all_above_expenses

        net_profit_per = net_profit * 12
        p = (15 * net_profit_per)/100
        net_profit_a_year = net_profit_per + p

        net_profit_per_2 = net_profit * 24
        p = (15 * net_profit_per_2)/100
        net_profit_two_year = net_profit_per_2 + p
    
      
        
        business_plan = {
        'business_name':business_name,
        'business_logo':business_logo_image,
        'business_registration_number':business_registration_number,
        'business_contact':business_contact,
        'business_address':business_address,
        'business_owner_name':business_owner_name,
        'business_owner_contact':business_owner_contact,
        'business_type':business_type,
        'year_of_operation':year_of_operation,
        'number_of_employees':number_of_employees,
        'period_of_report':period_of_report,
        'business_owner_email':business_owner_email,
        'total_sales_period':total_sales_period,
        'total_cost_of_sales_period':total_cost_of_sales_period,
        'total_gross_profits_for_period':total_gross_profits_for_period,
        'expenses':expenses_response.data,
        'salaries':salaries,
        'data':data,
        'electricity':electricity,
        'fuel':fuel,
        'total_of_all_above_expenses':total_of_all_above_expenses,
        'net_profit_loss':net_profit_loss,
        'cash_sales':cash_sales,
        'mobile_payment_sales':mobile_payment_sales,
        'kroon_sales':kroon_sales,
        'card_sales':card_sales,
        'card_sale_pecentage':card_sale_pecentage,
        'cash_sale_pecentage':cash_sale_pecentage,
        'kroon_sale_pecentage':kroon_sale_pecentage,
        'mobile_money_sale_pecentage':mobile_money_sale_pecentage,
        'best_sold_item':best_sold_item_S.data,
        'best_sold_item_price':best_sold_item_price,
        'worst_sold_item':Worst_sold_item_S.data,
        'worst_sold_item_price':worst_sold_item_price,
        'total_sold':total_sold,
        'worst_total_sold':worst_total_sold,
        'total_ordered_items_price':total_ordered_items_price,
        'total_purchase':total_purchase,
        'gross_profit_n_loss':gross_profit_n_loss,
        'net_profits_n_Loss':net_profits_n_Loss,
        'date_join':date_join,
        'business_category':business_category_S.data,
        'sale_one_year_percentage':sale_one_year_percentage,
        'sale_two_year_percentage':sale_two_year_percentage,
        'cost_of_sale_per_year':cost_of_sale_per_year,
        'cost_of_sale_2_years':cost_of_sale_2_years,
        'gross_for_a_year':gross_for_a_year,
        'gross_for_two_year':gross_for_two_year,
        'expensive_for_a_year_per_year':expensive_for_a_year_per_year,
        'expensive_for_two_year':expensive_for_two_year,
        'net_profit':net_profit,
        'net_profit_a_year':net_profit_a_year,
        'net_profit_two_year':net_profit_two_year,
        
        }

        # print(business_plan)
        # return response 
        return Response({'status': 'successful', 'message':'merchants business plan has been  been generated successfully', 'data': business_plan}, status=status.HTTP_201_CREATED)

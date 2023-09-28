from decimal import Decimal
from django.shortcuts import redirect, render
from django.db.models import Sum
from django.contrib.auth.decorators import login_required

from kiosk_cart.models import OrderProduct
from kiosk_stores.models import Merchant_Product
from subscriptions.models import Subscription_Plan ,Merchant_Subcribers

from .forms import BusinessPlanForm
from .models import Business_Plan
from kroon.users.models import BusinessProfile

# Create your views here.

@login_required()
def create_business_plan (request):
    user_profile = BusinessProfile.objects.get ( user = request.user , active = True)

    title = f'Create Your Business Report'
    description = f'This section requires your information or expections , which is stored and gives you the projected image of a great future for your business.'
    form_title = f'Business Details'
    submit_button = f'Click To Generate Business Plan'
    form = BusinessPlanForm()
    if request.method == 'POST':
        form = BusinessPlanForm( request.POST, request.FILES )
        if form.is_valid():
            user_record = BusinessProfile.objects.get ( user = request.user , active = True)
            form.instance.user = request.user
            form.instance.business_name = user_record.business_name
            form.instance.business_logo = user_record.business_logo
            form.instance.business_registration_number = user_record.business_registration_number
            form.instance.business_contact = user_record.business_contact_number
            form.instance.business_address = user_record.business_address
            form.instance.business_owner_name = request.user.name
            form.instance.business_owner_contact = request.user.contact_number
            form.instance.business_owner_email = request.user.email
            form.instance.business_type = user_record.business_type
            form.save()
            return redirect('business_plan')

    try:
        user_plan = Merchant_Subcribers.objects.get( user = request.user , active = True )
    except Merchant_Subcribers.DoesNotExist :
        user_plan = None

    context = {
        'form': form,
          # contents
        'title':title,
        'description':description,
        'form_title':form_title,
        'submit_button':submit_button,
        'user_plan':user_plan,
        'user_profile':user_profile,
    }
    return render(request, 'kiosk_merchant_dash/business_plan.html', context)


@login_required()
def business_plan (request):

    date_join = request.user.date_joined

    business_plan_record = Business_Plan.objects.filter( user = request.user ).order_by('-created_date')[:1]

    for b in business_plan_record:
        pass
    
    business_category = b.business_category
    business_name = b.business_name
    business_registration_number = b.business_registration_number
    business_contact = b.business_contact
    business_address = b.business_address
    business_owner_name = b.business_owner_name
    business_owner_contact = b.business_owner_contact
    business_type = b.business_type
    year_of_operation = b.year_of_operation
    number_of_employees = b.number_of_employees
    period_of_report = b.period_of_report
    business_owner_email = b.business_owner_email
    business_logo = b.business_logo


    total_sales_price = 0
    total_cost_price = 0
    total_ordered_items_price = 0
    total_purchase = 0
    total_quantity = 0
    sales = OrderProduct.objects.select_related("user", "payment", "order", "product").filter( ordered = True , user = request.user )
    for s in sales:
        total_sales_price += s.product_total_price
        total_cost_price += s.product.cost_price
        total_quantity += s.quantity
        total_ordered_items_price += s.product_total_price
    total_purchase = total_cost_price * total_quantity

    gross_profit_n_loss  = total_sales_price - total_purchase
    

        
    salaries = b.salaries * Decimal(b.period_of_report)
    data = b.data * Decimal(b.period_of_report)
    electricity = b.electricity * Decimal(b.period_of_report)
    fuel = b.fuel * Decimal(b.period_of_report)

    total_of_all_above_expenses = salaries + data + electricity + fuel


    total_sales_period = total_sales_price
    total_cost_of_sales_period = total_purchase
    total_gross_profits_for_period = total_sales_price - total_cost_price

    net_profit_loss = total_gross_profits_for_period - total_of_all_above_expenses
   
    # cash sales starts here 
    cash_sales = 0
    cash_sale = OrderProduct.objects.select_related("user", "payment", "order", "product").filter( ordered = True , user = request.user, payment__payment_method = 'cash_payment' )
    for c in cash_sale:
        cash_sales += c.product_total_price
    # cash sales ends here

    # card sales starts here
    card_sales = 0
    card_sale = OrderProduct.objects.select_related("user", "payment", "order", "product").filter( ordered = True , user = request.user, payment__payment_method = 'card_payment' )
    for c in card_sale:
        card_sales += c.product_total_price
    # card sales ends here

    # kroon sales starts here 
    kroon_sales = 0
    kroon_sale = OrderProduct.objects.select_related("user", "payment", "order", "product").filter( ordered = True , user = request.user, payment__payment_method = 'kroon_payment' )
    for c in kroon_sale:
        kroon_sales += c.product_total_price
    # kroon sales ends here
    
    # mobile_money sales start here
    mobile_payment_sales = 0
    mobile_money_sale = OrderProduct.objects.select_related("user", "payment", "order", "product").filter( ordered = True , user = request.user, payment__payment_method = 'mobile_money_payment' )
    for c in mobile_money_sale:
        mobile_payment_sales += c.product_total_price
    # mobile_money sales ends here
    
    # best selling 
    best_sold_item = 0 
    best_sold_item_price = 0 
    total_sold = 0 
    best_sold = OrderProduct.objects.select_related("user","order","product", "payment").filter( user = request.user, ordered = True ).annotate(quantity_sum=Sum('quantity')).order_by('-quantity_sum')[:1]
    for i in best_sold:
        best_sold_item = i.product
        best_sold_item_price = i.product.price
        total_sold = i.product_total_price * i.quantity

    # worst selling 
    worst_sold_item = 0  
    worst_sold_item_price = 0 
    worst_total_sold = 0
    worst_sold = OrderProduct.objects.select_related("user","order","product", "payment").filter( user = request.user, ordered = True ).annotate(quantity_sum=Sum('quantity')).order_by('quantity_sum')[:1]
    for i in worst_sold:
        worst_sold_item = i.product
        worst_sold_item_price = i.product.price
        worst_total_sold = i.product_total_price * i.quantity
    
    all_products = Merchant_Product.objects.select_related("user", "category").filter( user = request.user ).count()
    
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
  

    
    context = {
       'business_name':business_name,
       'business_logo':business_logo,
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
       'best_sold_item':best_sold_item,
       'best_sold_item_price':best_sold_item_price,
       'worst_sold_item':worst_sold_item,
       'worst_sold_item_price':worst_sold_item_price,
       'total_sold':total_sold,
       'worst_total_sold':worst_total_sold,
       'total_ordered_items_price':total_ordered_items_price,
       'total_purchase':total_purchase,
       'gross_profit_n_loss':gross_profit_n_loss,
       'net_profits_n_Loss':net_profits_n_Loss,
       'date_join':date_join,
       'business_category':business_category,
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
    return render(request, 'kiosk_merchant_dash/business_plan_record.html', context)


@login_required()
def my_business_record(request):
    my_records = Business_Plan.objects.filter( user = request.user)
    user_profile = BusinessProfile.objects.get ( user = request.user , active = True)

    try:
        user_plan = Merchant_Subcribers.objects.get( user = request.user , active = True )
    except Merchant_Subcribers.DoesNotExist :
        user_plan = None

    context = {
        'my_records':my_records,
        'user_plan':user_plan,
        'user_profile':user_profile,
    }
    return render(request, 'kiosk_merchant_dash/my_business_record.html', context)


@login_required()
def business_record_detail (request, *args, **kwargs):
    plan_id = kwargs.get('plan_id')
   
    business_plan_record = Business_Plan.objects.get( user = request.user, id = plan_id )
    
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


    total_sales_price = 0
    total_cost_price = 0
    total_ordered_items_price = 0
    total_purchase = 0
    total_quantity = 0
    sales = OrderProduct.objects.select_related("user", "payment", "order", "product").filter( ordered = True , user = request.user )
    for s in sales:
        total_sales_price += s.product_total_price
        total_cost_price += s.product.cost_price
        total_quantity += s.quantity
        total_ordered_items_price += s.product_total_price
        period_cost_of_sales = s.product.cost_price * s.quantity
        print(period_cost_of_sales)
    total_purchase = total_cost_price * total_quantity

    gross_profit_n_loss  = total_sales_price - total_purchase
    

        
    salaries = business_plan_record.salaries * Decimal(business_plan_record.period_of_report)
    data = business_plan_record.data * Decimal(business_plan_record.period_of_report)
    electricity = business_plan_record.electricity * Decimal(business_plan_record.period_of_report)
    fuel = business_plan_record.fuel * Decimal(business_plan_record.period_of_report)

    total_of_all_above_expenses = salaries + data + electricity + fuel


    total_sales_period = total_sales_price
    total_cost_of_sales_period = total_cost_price
    total_gross_profits_for_period = total_sales_price - total_cost_price

    net_profit_loss = total_gross_profits_for_period - total_of_all_above_expenses
   
    # cash sales starts here 
    cash_sales = 0
    cash_sale = OrderProduct.objects.select_related("user", "payment", "order", "product").filter( ordered = True , user = request.user, payment__payment_method = 'cash_payment' )
    for c in cash_sale:
        cash_sales += c.product_total_price
    # cash sales ends here

    # card sales starts here
    card_sales = 0
    card_sale = OrderProduct.objects.select_related("user", "payment", "order", "product").filter( ordered = True , user = request.user, payment__payment_method = 'card_payment' )
    for c in card_sale:
        card_sales += c.product_total_price
    # card sales ends here

    # kroon sales starts here 
    kroon_sales = 0
    kroon_sale = OrderProduct.objects.select_related("user", "payment", "order", "product").filter( ordered = True , user = request.user, payment__payment_method = 'kroon_payment' )
    for c in kroon_sale:
        kroon_sales += c.product_total_price
    # kroon sales ends here
    
    # mobile_money sales start here
    mobile_payment_sales = 0
    mobile_money_sale = OrderProduct.objects.select_related("user", "payment", "order", "product").filter( ordered = True , user = request.user, payment__payment_method = 'mobile_money_payment' )
    for c in mobile_money_sale:
        mobile_payment_sales += c.product_total_price
    # mobile_money sales ends here
    
    # best selling 
    best_sold_item = 0
    best_sold_item_price = 0
    total_sold = 0 
    best_sold = OrderProduct.objects.select_related("user","order","product", "payment").filter( user = request.user, ordered = True ).annotate(quantity_sum=Sum('quantity')).order_by('-quantity_sum')[:1]
    for i in best_sold:
        best_sold_item = i.product
        best_sold_item_price = i.product.price
        total_sold = i.product_total_price * i.quantity

    # worst selling
    worst_sold_item = 0  
    worst_sold_item_price = 0
    worst_total_sold = 0  
    worst_sold = OrderProduct.objects.select_related("user","order","product", "payment").filter( user = request.user, ordered = True ).annotate(quantity_sum=Sum('quantity')).order_by('quantity_sum')[:1]
    for i in worst_sold:
        worst_sold_item = i.product
        worst_sold_item_price = i.product.price
        worst_total_sold = i.product_total_price * i.quantity
    
    # all_products = Merchant_Product.objects.select_related("user", "category").filter( user = request.user ).count()
    
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

    # net_profits_n_Loss =  total_gross_profits_for_period - total_of_all_above_expenses 

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

    context = {
        'business_logo':business_logo,
       'business_name':business_name,
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
       'best_sold_item':best_sold_item,
       'best_sold_item_price':best_sold_item_price,
       'worst_sold_item':worst_sold_item,
       'worst_sold_item_price':worst_sold_item_price,
       'total_sold':total_sold,
       'worst_total_sold':worst_total_sold,
       'total_ordered_items_price':total_ordered_items_price,
       'total_purchase':total_purchase,
       'gross_profit_n_loss':gross_profit_n_loss,   
       'business_category':business_category,
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

    return render(request, 'kiosk_merchant_dash/business_plan_pdf.html', context )


@login_required()
def delete_plan(self, request, *args, **kwargs):
    plan_id = kwargs.get('plan_id')
    business_plan_record = Business_Plan.objects.get( user = request.user, id = plan_id ).delete()
    if business_plan_record:
        return redirect('my_business_record')
    


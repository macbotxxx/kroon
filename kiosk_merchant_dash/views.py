import pytz
import requests
import json
import datetime

from decimal import Decimal
from django.forms import FloatField
from django.http import HttpResponse
from datetime import timedelta, datetime
from datetime import date
from django.conf import settings
from django.db.models import Count
from django.contrib import messages
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Q
from django.db.models import Sum
from django.db.models.functions import TruncMonth
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm

from kiosk_cart.models import OrderProduct ,Order ,Payment
from kiosk_stores.models import Merchant_Product
from subscriptions.models import Subscription_Plan ,Merchant_Subcribers
from helpers.common.disable_account import Delete_Accounts

from .forms import Email_VerificationForm, MerchantSignupForm, OTPVerificationForm, KYC_Form, Edit_Business_Profile , Business_Language_Form
from kroon.users.models import User, BusinessProfile
from locations.models import Country, Language
from helpers.common.decorators import allowed_accounts

utc=pytz.UTC

# from datetime import date, datetime, timezone



# Create your views here.

KOK_AUTH_KEYS = settings.KOK_AUTH_KEYS
register_url = "https://www.mykroonapp.com/kroon-opt/api/v1/email-opt/"
verify_otp = "https://www.mykroonapp.com/kroon-opt/api/v1/verify-otp/"



def email_verification (request):
    # this holds the email input for verification
    form = Email_VerificationForm()
    if request.method == 'POST':
        form = Email_VerificationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            
            # verifying if user is already a user 
            try:
                User.objects.get( email = email )
                messages.info(request, f"Your email address has been registered by a user , kindly login to your account , using the registered email.")
                return redirect(email_verification)
            except User.DoesNotExist:
                pass

            # sending and otp pin
            url = f'{register_url}'

            payload = json.dumps({
            "email": f'{email}',
            "platform": "kiosk"
            })
            headers = {
            'Content-Type': 'application/json',
            'KOK-Authentication-Token': KOK_AUTH_KEYS
            }

            response = requests.request("POST", url, headers=headers, data=payload)
            response_data = response.json()
            status = response_data['status']

            # saving session from email verification
            request.session['email'] = email
            
            if status == 'success':
                return redirect(otp_verification)
            else:
                messages.info(request, f"{response_data['message']}")

    context = {
        'form': form,
    }

    return render(request, 'kiosk_merchant_dash/auth_page/email_verification.html', context)


def otp_verification (request):
    # the otp verification code 
    form = OTPVerificationForm()
    if request.method == 'POST':
        form = OTPVerificationForm(request.POST)
        if form.is_valid():
            otp = form.cleaned_data.get('otp')
            email = request.session['email']
            # sending and otp pin
            url = f'{verify_otp}'

            payload = json.dumps({
            "email": f'{email}',
            "otp_pin": f'{otp}',
            "platform": "kiosk"
            })
            headers = {
            'Content-Type': 'application/json',
            'KOK-Authentication-Token': KOK_AUTH_KEYS
            }

            response = requests.request("POST", url, headers=headers, data=payload)
            response_data = response.json()
            status = response_data['status']
            request.session['email_verification'] = False

            if status == "success":
                request.session['email_verification'] = True
                return redirect(registration_merchant)
            else:
                request.session['email_verification'] = False
                messages.info(request, f"{response_data['message']}")

    context = {
        'form': form,
    }
    return render(request, 'kiosk_merchant_dash/auth_page/register.html', context)


def warning(request):
    return render(request, 'kiosk_merchant_dash/warning.html')


def registration_merchant (request):
    # this hold the merchant registration pages
    print(request.session['email_verification'])
    if request.session['email_verification']:
        pass
    else:
        messages.info(request, f"Kindlty verify your email address before proceeding with the merchant registration.")
        return redirect(email_verification)

    form = MerchantSignupForm()
    if request.method == 'POST':
        form = MerchantSignupForm(request.POST)
        if form.is_valid():
            form.save(request)
            request.session['email_verification'] = False
            return redirect("index_page")
    context = {
        'form': form,
    }
    return render(request, 'kiosk_merchant_dash/auth_page/register.html', context)


@login_required()
@allowed_accounts()
def index_page (request):
    total_sales = 0   
    daily_total_sale = 0
    total_daily_sales = 0
   

    # checking if the login user has registered
    # their business profile
    #Getting the current date in local time format
    current_time = datetime.now()

    yesterday = current_time.day - 1
    try:
        worker = BusinessProfile.objects.get( user = request.user , active = True )
        pass
    except BusinessProfile.DoesNotExist:
        worker = BusinessProfile.objects.filter( workers = request.user )
        if worker:
            return redirect('kyc_form')
        else:
            return redirect('kyc_form')

    worker_count = 0
    category_count = 0
    counts = BusinessProfile.objects.get( user = request.user , active = True )
    worker_count += counts.workers.count()
    category_count += counts.business_category.count()

    # getting the percentage of the sales
    yesterday_quantity = 0
    yesterday_sale = OrderProduct.objects.select_related("user", "payment", "order", "product").filter( user = request.user, ordered = True , created_date__day = yesterday)

    for y in yesterday_sale:
        yesterday_quantity += y.quantity
    yesterday_sale_count = yesterday_quantity
    

    today_quantity = 0
    today_sale = OrderProduct.objects.select_related("user", "payment", "order", "product").filter( user = request.user, ordered = True , created_date__day = current_time.day)

    for t in today_sale:
        yesterday_quantity += t.quantity
    today_sale_count = yesterday_quantity


    quantity = 0
    all_products = Merchant_Product.objects.select_related("user", "category").filter( user = request.user )
    for p in all_products:
        quantity += int(p.stock)
    all_products_count = quantity
    product_count = all_products.count()

    try:
        daily_sales_percentage = (today_sale_count / all_products_count) * 100
        yesterday_sale_percentage = (yesterday_sale_count / all_products_count) * 100
        
    except ZeroDivisionError:
        daily_sales_percentage = 0
        yesterday_sale_percentage = 0

    if yesterday_sale_percentage > daily_sales_percentage:
        percentage = format(daily_sales_percentage, '.2f')
        sale_percentage = f'-{percentage}'
    elif yesterday_sale_percentage < daily_sales_percentage:
        percentage = format(daily_sales_percentage, '.2f')
        sale_percentage = f'+{percentage}'
    else:
        percentage = format(daily_sales_percentage, '.2f')
        sale_percentage = f'{percentage}'

     # getting all card payments
    recent_sales = Order.objects.select_related("user", "payment").filter(  user = request.user, is_ordered = True  )[:5]

    sales = Order.objects.select_related("user", "payment").filter(  user = request.user, is_ordered = True  )
    for i in sales:
        total_sales += i.order_total
    total_sale = Decimal(total_sales)
    order_count = sales.count()
    

    daily_sales = Order.objects.select_related("user", "payment").filter( user = request.user, is_ordered = True  , created_date__day = current_time.day)
    for i in daily_sales:
        total_daily_sales += i.order_total
    daily_total_sale = Decimal(total_daily_sales)
    daily_count = daily_sales.count()
    
    user_profile = BusinessProfile.objects.get ( user = request.user , active = True )


    context = {
        'sale_percentage':sale_percentage,
        'total_sale':total_sale,
        'daily_total_sale':daily_total_sale,
        'order_count':order_count,
        'product_count':product_count,
        'recent_sales':recent_sales,
        'daily_count':daily_count,
        'worker_count':worker_count,
        'category_count':category_count,
        'user_profile':user_profile,
    }


    return render(request, 'kiosk_merchant_dash/index.html' , context)



@login_required()
@allowed_accounts()
def kyc_form (request):
    form = KYC_Form()
    if request.method == 'POST':
        form = KYC_Form(request.POST, request.FILES)
        if form.is_valid():
            form.instance.user = request.user
            make_default = form.cleaned_data.get( 'default' )
            if make_default:
                # checking if the business profile exists already
                try:
                    default_business_profile = BusinessProfile.objects.get( user = request.user, active = True )
                    default_business_profile.active = False
                    default_business_profile.save()

                except BusinessProfile.DoesNotExist:
                    form.instance.active = True

            if BusinessProfile.objects.filter ( user = request.user , active = True ).count() > 0:
                form.instance.active = False
            else:
                form.instance.active = True
            user_profile = User.objects.get ( email = request.user.email )
            user_profile.merchant_business_name = form.cleaned_data.get('business_name')
            user_profile.save()
            form.save()
            
            return redirect('index_page')

    context = {
        'form':form,
    }

    return render(request, 'kiosk_merchant_dash/kyc.html', context)



@login_required()
@allowed_accounts()
def all_products(request):

    all_product = Merchant_Product.objects.select_related("user", "category").filter( user = request.user )
    user_profile = BusinessProfile.objects.get ( user = request.user , active = True )

     # pagination
    paginator = Paginator(all_product, 100) # Show 25 contacts per page.
    page_number = request.GET.get('page')
    all_product = paginator.get_page(page_number)
    context = {
        'all_product':all_product,
        'user_profile':user_profile,
    }
    return render(request, 'kiosk_merchant_dash/all_products.html', context)


@allowed_accounts()
@login_required()
def all_sales (request):
    sales = Order.objects.select_related("user", "payment").filter(  user = request.user, is_ordered = True  )
    user_profile = BusinessProfile.objects.get ( user = request.user , active = True )

    paginator = Paginator(sales, 100) # Show 25 contacts per page.
    page_number = request.GET.get('page')
    sales = paginator.get_page(page_number)

    context = {
        'sales':sales,
        'user_profile':user_profile,

    }
    return render(request, 'kiosk_merchant_dash/sales.html', context)


@allowed_accounts()
@login_required()
def sale_details (request, order_id):
    sale = OrderProduct.objects.select_related("user", "payment", "order", "product").filter( ordered = True , order__order_number = order_id )

    if not sale.exists():
        return HttpResponse('item does not exist')
    for s in sale:
        user = s.user
    total = Order.objects.select_related("user", "payment", ).get( is_ordered = True , order_number = order_id )
    business_profile = BusinessProfile.objects.get (user = user, active = True)

    context = {
        'sale':sale,
        'total':total,
        'business_profile':business_profile,
        'user_profile':business_profile,
    }
    
    return render(request, 'kiosk_merchant_dash/sales_details.html', context)


@allowed_accounts()
@login_required()
def delete_product (request, product_id):    
    product = Order.objects.select_related("user", "payment").get(  user = request.user, is_ordered = True, id = product_id  )
    product.delete()
    
    messages.info(request, f"Order history has been delete from your account")
    return redirect('all_sales')
    

def invoice(request , order_id):

    sale = OrderProduct.objects.select_related("user", "payment", "order", "product").filter( ordered = True , order__order_number = order_id )
    if not sale.exists():
        return HttpResponse('item does not exist')
    for s in sale:
        user = s.user
    total = Order.objects.select_related("user", "payment", ).get( is_ordered = True , order_number = order_id )
    business_profile = BusinessProfile.objects.get (user = user, active = True)

    context = {
        'sale':sale,
        'total':total,
        'business_profile':business_profile,
    }
    return render(request, 'kiosk_merchant_dash/invoice.html', context)



@login_required()
def business_analytics(request):

    # orders been sold monthly and weakly

    # getting the best selling products  
    best_sale = OrderProduct.objects.select_related('user', 'payment', 'products' , 'order').filter(user__id = request.user.id , ordered = True ).values('ordered', 'product__product_name').annotate(total = Count('ordered')).order_by('-total')[:9]

    # day_daily_payment_sale = Payment.objects.select_related("user").filter(Q(payment_method = 'kroon_payment') | Q(payment_method = 'card_payment') | Q(payment_method = 'cash_payment'),  user = request.user, verified = True).extra({'day': "to_char(created_date, 'DD MONTH')"}).values('day').annotate(sales_count=Count('id')).order_by('-day')[:8]
   
    # print(day_daily_payment_sale)

    # payment method total count - DAILY
    kroon_monthly_payment_sale = Order.objects.select_related("user", "payment").filter(  user = request.user, is_ordered = True ,payment__payment_method = "kroon_payment" ).extra({'day': "to_char(created_date, 'MONTH')"}).values('day').annotate(sales_count=Count('id')).order_by('-day')[:10]

    cash_monthly_payment_sale = Order.objects.select_related("user", "payment").filter(  user = request.user, is_ordered = True ,payment__payment_method = "cash_payment" ).extra({'day': "to_char(created_date, 'MONTH')"}).values('day').annotate(sales_count=Count('id')).order_by('-day')[:10]

    card_monthly_payment_sale = Order.objects.select_related("user", "payment").filter(  user = request.user, is_ordered = True ,payment__payment_method = "card_payment" ).extra({'day': "to_char(created_date, 'MONTH')"}).values('day').annotate(sales_count=Count('id')).order_by('-day')[:10]
    
    month_payment_sale = Order.objects.select_related("user", "payment").filter(  user = request.user, is_ordered = True  ).extra({'month': "to_char(created_date, 'MONTH')"}).values('month').annotate(sales_count=Count('id')).order_by('-month')[:10]

    # Current_Date = datetime. datetime. today()
    # Previous_Date = datetime.datetime.today() - datetime.timedelta(days=1)

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

    monthly_sales = Order.objects.filter( user = request.user,  is_ordered = True).extra({'created': "to_char(created_date, 'YYYY/MM')"}).values('created').annotate(created_count=Count('id')).order_by('-created')[:10]


    # getting all payment sales revenue for each merchant
    merchant_revenue = Payment.objects.select_related('user').filter( user_id = request.user.id ).values('verified','user__name', 'user__merchant_business_name', 'payment_method' ).annotate( total_revenue = Sum('amount_paid'), total = Count('verified') ).order_by('-verified')


    
    # working on the subscriptions restrictions
    try:
        user_plan = Merchant_Subcribers.objects.get( user = request.user , active = True )
    except Merchant_Subcribers.DoesNotExist :
        user_plan = None

    user_profile = BusinessProfile.objects.get ( user = request.user , active = True )


    context = {
        'daily_sales':daily_sales,
        'monthly_sales':monthly_sales,

        # daily payment sales_count
        'kroon_daily_payment_sale':daily_kroon_sales,
        'cash_daily_payment_sale':daily_cash_sales,
        'card_daily_payment_sale':daily_card_sales,
        'mobile_money_daily_payment_sale':daily_mobile_money_sales,

        # 'day_daily_payment_sale':day_daily_payment_sale,
    
        # # monthly payment sales_count
        # 'kroon_monthly_payment_sale':kroon_monthly_payment_sale,
        # 'cash_monthly_payment_sale':cash_monthly_payment_sale,
        # 'card_monthly_payment_sale':card_monthly_payment_sale,

        # count
       
        'best_sale':best_sale,
        'days':days,

        # total revenue
        'merchant_revenue':merchant_revenue,

        # subscriptions
        'user_plan':user_plan,
        'user_profile':user_profile,
    }

    return render(request, 'kiosk_merchant_dash/business_analytics.html', context)



@allowed_accounts()
@login_required()
def financial_analytics(request):
    monthly_sales = Order.objects.filter( user = request.user,  is_ordered = True).extra({'created': "to_char(created_date, 'YYYY/MM')"}).values('created').annotate(created_count=Sum('order_total')).order_by('-created')[:10]
    # json_result = json.dumps(monthly_sales, cls=DjangoJSONEncoder)


    # getting all payment sales revenue for each merchant
    total_sales_revenue = Payment.objects.select_related('user').filter( user_id = request.user.id , verified = True ).values('verified','user__name', 'user__merchant_business_name', 'payment_method' ).annotate( total_revenue = Sum('amount_paid'), total = Count('verified') ).order_by('-verified')

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
    try:
        user_plan = Merchant_Subcribers.objects.get( user = request.user , active = True )
    except Merchant_Subcribers.DoesNotExist :
        user_plan = None

    user_profile = BusinessProfile.objects.get ( user = request.user , active = True )
    
    
    context = {
        'monthly_sales':monthly_sales,
        'recent_sale':daily_sales,
        'days':days,

        # subscriptions
        'user_plan':user_plan,
        'user_profile':user_profile,
        'total_sales_revenue':total_sales_revenue,
    }

    return render(request, 'kiosk_merchant_dash/financial_analytics.html', context)


@allowed_accounts()
@login_required()
def account_settings (request):
    user_profile = BusinessProfile.objects.get ( user = request.user , active = True )
    business_form = Edit_Business_Profile( instance = user_profile )
    
    if request.method == 'POST':
        business_form = Edit_Business_Profile (request.POST, request.FILES , instance = user_profile)
        if business_form.is_valid():
            business_form.save()
            # updating the merchant account business name
            merchant_business = User.objects.get( email = request.user.email )
            merchant_business.merchant_business_name = business_form.cleaned_data.get('business_name')
            merchant_business.save()
            # endhere 
            messages.info(request, f"Your business profile has been updated successfully.")

    context = {
        'business_form': business_form,
        'user_profile':user_profile,

    }
    return render(request, 'kiosk_merchant_dash/settings.html', context)


@allowed_accounts()
@login_required()
def account_settings_password (request):
    user_profile = BusinessProfile.objects.get ( user = request.user , active = True )
    user_password = PasswordChangeForm(request.user)

    if request.method == 'POST':
        user_password = PasswordChangeForm(request.user, request.POST)
        if user_password.is_valid():
            user = user_password.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('account_settings_password')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        user_password = PasswordChangeForm(request.user)

    context = {
        'user_password':user_password,
        'user_profile':user_profile,
    }
    return render(request, 'kiosk_merchant_dash/settings_password.html', context)


@login_required()
def account_settings_theme (request, *args, **kwargs):
    user_profile = BusinessProfile.objects.get ( user = request.user , active = True )
    
    context = {    
        'user_profile':user_profile,
    }
    return render(request, 'kiosk_merchant_dash/settings_theme.html', context)


@allowed_accounts()
@login_required()
def activate_theme (request):
    user_profile = BusinessProfile.objects.get ( user = request.user , active = True )
    if user_profile.web_light_mode:
        user_profile.web_light_mode = False
    else:
        user_profile.web_light_mode = True

    user_profile.save()
    messages.error(request, 'Your business account theme has been activated')
    return redirect('account_settings_theme')


    

@allowed_accounts()
@login_required()
def account_settings_language (request):
    user_profile = BusinessProfile.objects.get ( user = request.user , active = True )
    language_form = Business_Language_Form()

    if request.method == 'POST': 
        language_form = Business_Language_Form( request.POST )
        if language_form.is_valid():
            language = language_form.cleaned_data.get('language')
            try:
                lan_iso2 = Language.objects.get( language_name = language )
            except Language.DoesNotExist :
                messages.error(request, 'Please correct the error below.')
            user_profile.business_default_language = lan_iso2.language_ISO2
            user_profile.save() 
            messages.error(request, 'Your business account language has been updated successfully')

    context = {
        'user_profile':user_profile,
        'language_form':language_form,
    }
    return render(request, 'kiosk_merchant_dash/settings_language.html', context)


@allowed_accounts()
@login_required()
def delete_my_account(request):
    user_profile = BusinessProfile.objects.get ( user = request.user , active = True )
    if request.method == 'POST':
        # # deleting the user record
        delete_user_account = Delete_Accounts()
        response_data = delete_user_account.kiosk_delete_account(request.user , request.user.id)
        return redirect('index_page')
        
    context = {
        'user_profile':user_profile,
    }
    return render(request, 'kiosk_merchant_dash/settings_delete_account.html', context)



@login_required()
def switchAccountMerchant( request):
        # switching to a merchant account
        switch_merchant_account = User.objects.get( id = request.user.id)
        switch_merchant_account.account_type = "merchant"
        switch_merchant_account.save()
        return redirect('index_page')


@login_required()
def switchBusinessAccountMerchant( request , *args, **kwargs):
    business_id = kwargs.get('business_id')
    # updating the previously saved business accounts
    try:
        business_account = BusinessProfile.objects.get( user = request.user , active = True)
        business_account.active = False
        business_account.save()
    except BusinessProfile.DoesNotExist:
        pass

    # switching to a business account
    switch_business_account = BusinessProfile.objects.get(user = request.user , id = business_id )
    switch_business_account.active = True
    switch_business_account.save()
    return redirect('index_page')












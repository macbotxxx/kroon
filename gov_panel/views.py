# import sections 
from decimal import Decimal
import json
import os
import random
import string
import csv
import pytz

# django packages 
from django.utils import timezone
from django.shortcuts import render, redirect
from django.http import JsonResponse
from datetime import timedelta, datetime
from django.core.paginator import Paginator
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.core.files.storage import default_storage as storage 
from django.db.models import Count , Sum
from datetime import date
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.contrib.auth.models import Group, Permission
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models.functions import TruncDay


# django email settings
from django.core import mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from helpers.common.decorators import admin_only, allowed_user
from helpers.common.currency_converter import usd_currency_converter


from kroon.users.models import User, BusinessProfile
from locations.models import Country , Country_Province
from ads.models import Ads
from notifications.models import NewsFeed
from .forms import Onboarding_Users_Form , Push_Notifications_Form , Publish_NewsFeed_Form
from kiosk_worker.forms import VerifyEmail, WorkerSignupForm, WorkerVerifyOtp , Gov_Worker_SignupForm
from kroon_otp.models import OPTs

from .models import Onboarding_Users_CSV, Action_logs, Government_Organizations
from kiosk_cart.models import Order,OrderProduct , Payment
from .filters import Merchants_Filters , Business_Filters
from .tasks import publishing_newfeed , merchant_onboarding_process
from kiosk_stores.models import Merchant_Product

utc=pytz.UTC



def opt_code():
    return ''.join(random.choices(string.digits, k=6))



def password_geenrate():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

def ref_code():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=9))



# Create your views here.

@login_required()
@allowed_user(allowed_roles = ['Gov_Worker', 'Gov_Super_Admin'])
def index(request):
    list_of_province = Country_Province.objects.select_related('country').filter(country=request.user.country_of_residence)

    if request.user.country_of_residence.iso2 == "NG":
        jobs = BusinessProfile.objects.filter( user__government_registered = True ).values('business_name',).annotate(total_workers=Count('workers') ).order_by('-active')

        all_active_user = User.objects.select_related('country_of_residence', 'country_province', 'on_boarding_user', 'bank_details').filter( government_registered = True )

    else:
        jobs = BusinessProfile.objects.filter( user__on_boarding_user = request.user ).values('business_name',).annotate(total_workers=Count('workers') ).order_by('-active')

        all_active_user = User.objects.select_related('country_of_residence', 'country_province', 'on_boarding_user', 'bank_details').filter( on_boarding_user = request.user , is_active = True )

    job_created_count = 0
    for job in jobs:
        job_created_count += job['total_workers']


    users_count = all_active_user.count()
    # gender count
    country_gender_male = all_active_user.filter( gender = 'male').count()
    country_gender_female  = all_active_user.filter( gender = 'female').count()
   
   
    province_list = []
    for i in list_of_province:
        if request.user.country_of_residence.iso2 == "NG":

            province_users = User.objects.select_related('country_of_residence', 'country_province').filter(country_province = i.id, government_registered = True).count()
    
            province_merchant_sales = Order.objects.select_related("user", "payment").filter( user__country_province = i.id,user__government_registered = True, is_ordered = True ).count()

            total_sales = OrderProduct.objects.select_related('user', 'payment', 'order', 'product').filter( user__government_registered = True , user__country_province = i.id, ordered = True )

        else:
            
            province_users = User.objects.select_related('country_of_residence', 'country_province').filter(country_province = i.id, on_boarding_complete = True).count()
    
            province_merchant_sales = Order.objects.select_related("user", "payment").filter( user__country_province = i.id,user__on_boarding_complete = True, is_ordered = True ).count()

            total_sales = OrderProduct.objects.select_related('user', 'payment', 'order', 'product').filter( user__on_boarding_complete = True , user__country_province = i.id, ordered = True )


        total_sale = 0 
        cost_of_sales_province = 0

        # merchant sales via province 
        for c in total_sales:
            total_sale += c.product_total_price
        # merchant cost of sales via province
        for c in total_sales:
            cost_of_sales_province += c.product.cost_price

        note = {'province_count':province_users , 'province':i.province , 'province_merchant_sales':province_merchant_sales , 'sales':total_sale , 'cost_of_sales_province':cost_of_sales_province}
        province_list.append(note)

        # remote_username = request.META.get('USER')
        # remote_ipaddr = request.META.get('REMOTE_ADDR')
        # remote_os = request.META.get('HTTP_USER_AGENT')

        # print(remote_username)
        # print(remote_ipaddr)
        # print(remote_os)


    province_all = Country_Province.objects.all()

    context = {
        'province':province_list,
        'province_all':province_all,
        'country_gender_male':country_gender_male,
        'country_gender_female':country_gender_female,
       'job_created_count':job_created_count,
       'all_active_user':users_count,


    }
    return render(request , 'gov_panel/index.html', context)



# Onboarding of user and user details
# start here 
@login_required()
@allowed_user(allowed_roles = ['Gov_Worker', 'Gov_Super_Admin'])
def gov_users_on_boarding (request):
    form = Onboarding_Users_Form()

    # storing onboarding doc
    if request.method == 'POST':
        form = Onboarding_Users_Form(request.POST , request.FILES)
        if form.is_valid():
            form.instance.on_boarding_user = request.user
            file = form.cleaned_data.get('on_boarding_user_file')
            form.save()
            # Onboarding
            users_csv_file = Onboarding_Users_CSV.objects.filter( on_boarding_user = request.user , on_boarding_complete = False ).order_by('-created_date')[0:1]
            for i in users_csv_file:
                new_file = i.on_boarding_user_file.name
                with storage.open(new_file, 'r') as f:
                    csvf = csv.reader(f)
                    # validating through onboarding csv file  
                    try:
                        for id,first_name,last_name,email,business_name,province, *__ in csvf:
                            # generating unique password 
                            pass
                        # executing the onbaording process 
                        # merchant_onboarding_process.delay()
                        messages.info(request, f"Your users onboarding has been processed Successfully , if the is any issue with  onboarding , kindly report to the customer service .")
                    except:
                        i.delete()
                        messages.info(request, f"the file is cant be access kindly follow the steps provided")
                    # valdiating ends here 
                
    context = {
        "form":form,
    }
    return render(request , 'gov_panel/onboarding.html', context)



@login_required()
@allowed_user(allowed_roles = ['Gov_Worker', 'Gov_Super_Admin'])
def gov_users_list (request ):
    if request.user.country_of_residence.iso2 == "NG":
        all_gov_users = User.objects.select_related('country_of_residence', 'country_province', 'on_boarding_user', 'bank_details',).filter(  government_registered = True  )
        nigerian_users = User.objects.select_related('country_of_residence', 'country_province', 'on_boarding_user', 'bank_details',).filter( country_of_residence__iso2 = "NG" ).count()
        # gender count
        country_gender_male = all_gov_users.filter( gender = 'male').count()
        country_gender_female  = all_gov_users.filter( gender = 'female').count()
        # calculating the currency convert 
        merchants_revenue = Order.objects.select_related("user", "payment").filter( user__government_registered = True , is_ordered = True )
        total_revenue = 0
        for i in merchants_revenue:
            total_revenue += i.order_total
        currency = request.user.default_currency_id
    else:
        all_gov_users = User.objects.select_related('country_of_residence', 'country_province', 'on_boarding_user', 'bank_details',).filter( on_boarding_complete = True , country_of_residence = request.user.country_of_residence  )
        nigerian_users = 0
        total_revenue = 0
        country_gender_male = 0
        currency = None
        country_gender_female = 0
    
    user_count = all_gov_users.count()
    # filter 
    filters_store = Merchants_Filters(request.GET, queryset=all_gov_users)
    all_gov_users = filters_store.qs

    # filters 
    filter_b = Merchants_Filters()
    # pagination
    paginator = Paginator(all_gov_users, 100) # Show 200 contacts per page.
    page_number = request.GET.get('page')
    all_gov_users = paginator.get_page(page_number)

    

    context = {
        
        'all_gov_users':all_gov_users,
        'user_count':user_count,
        'filters_store':filters_store,
        'nigerian_users':nigerian_users,
        'total_revenue':total_revenue,
        'currency':currency,
        'country_gender_male':country_gender_male,
        'country_gender_female':country_gender_female,
    }
    return render(request , 'gov_panel/gov_users_list.html', context)



@login_required()
@allowed_user(allowed_roles = ['Gov_Worker', 'Gov_Super_Admin'])
def gov_onboarding_progess (request ):
    progress_list = Onboarding_Users_CSV.objects.select_related('on_boarding_user').filter( on_boarding_user = request.user )
    context = {
        'progress_list':progress_list,
    }
    return render(request, 'gov_panel/onboarding_process.html',context)


@login_required()
@allowed_user(allowed_roles = ['Gov_Worker', 'Gov_Super_Admin'])
def gov_users_details (request , id ):
    gov_user = User.objects.get( id = id)
    context = {
        "gov_user":gov_user,
    }

    return render(request , 'gov_panel/gov_users_details.html', context )



@login_required()
@allowed_user(allowed_roles = ['Gov_Worker', 'Gov_Super_Admin'])
def gov_push_notification (request ):
    # getting all the newsfeed 
    newsfeed = NewsFeed.objects.filter( gov_post = True )
    # pagination to the newsfeed
    paginator = Paginator(newsfeed, 100) # Show 100 contents per page.
    page_number = request.GET.get('page')
    newsfeed = paginator.get_page(page_number)

    context = {
        'newsfeed':newsfeed,
    }
    return render(request , 'gov_panel/push_notification.html', context )



@login_required()
@allowed_user(allowed_roles = ['Gov_Worker', 'Gov_Super_Admin'])
def gov_publish_notification ( request ):
    # access news feed form
    form = Publish_NewsFeed_Form()
    if request.method == 'POST':
        form = Publish_NewsFeed_Form(request.POST, request.FILES)
        # form validation
        if form.is_valid():
            form.instance.platform = "kroon kiosk" 
            form.instance.gov_post = True
            form.instance.publisher = request.user.name
            form.save()
            form.instance.news_feed_country.add(request.user.country_of_residence.id) 

            # passing the notification massage
            messages.info(request, f"News Feed has been uplaoded successfully , awaiting for approval")
            # redirect to the list of newsfeed 
            return redirect("gov_push_notification")
            
    context = {
        'form':form,
    }
    return render(request , 'gov_panel/publish_newsfeed.html', context )



@login_required()
@allowed_user(allowed_roles = ['Gov_Worker', 'Gov_Super_Admin'])
def gov_edit_newsfeed ( request , id ):
    # editing newsfeed 
    qs = NewsFeed.objects.get( id = id )
    form = Publish_NewsFeed_Form( instance = qs )
    if request.method == 'POST':
        form = Publish_NewsFeed_Form( request.POST , request.FILES , instance = qs )
        if form.is_valid():
            form.save()
            # passing the notification massage
            messages.info(request, f"News Feed has been uplaoded successfully , awaiting for approval")
            # redirect to the list of newsfeed 
            return redirect("gov_push_notification")
    context = {
        'form':form,
    }
    return render(request , 'gov_panel/publish_newsfeed.html', context )



@login_required()
@allowed_user(allowed_roles = ['Gov_Worker', 'Gov_Super_Admin'])
def gov_newsfeed_approval ( request , id ):
    # current date time 
    current_date = timezone.now()
    # publishing date 
    publishing_date = timezone.now() + timedelta(minutes=3)
    # updating the status for the news feed
    qs = NewsFeed.objects.get( id = id )
    qs.publishing_time = publishing_date
    qs.approved_date = current_date
    qs.save()
    # publishing action
    publishing_newfeed.delay()
    # passing the notification massage
    messages.info(request, f"News Feed has been approved successfully ")
    # redirect to the list of newsfeed 
    return redirect("gov_push_notification")



@login_required()
@allowed_user(allowed_roles = ['Gov_Worker', 'Gov_Super_Admin'])
def gov_newsfeed_delete ( request , id ):
    # deleting the news feed
    qs = NewsFeed.objects.get( id = id )
    qs.delete() 
    # passing the notification massage
    messages.info(request, f"News Feed has been deleted successfully ")
    # redirect to the list of newsfeed 
    return redirect("gov_push_notification")



@login_required()
@allowed_user(allowed_roles = ['Gov_Worker', 'Gov_Super_Admin'])
def gov_push_ads (request ):
    form = Push_Notifications_Form()
    
    if request.method == 'POST':
        form = Push_Notifications_Form(request.POST, request.FILES)
        if form.is_valid():
            form.instance.platform = "kroon_kiosk" 
            form.save()
            form.instance.ad_country.add(request.user.country_of_residence.id)

            messages.info(request, f" Ads has been push successfully , waiting for approval by the administrator ")

    context = {
        "form": form,
    }
    return render(request , 'gov_panel/push_ads.html', context )




@login_required()
@allowed_user(allowed_roles = ['Gov_Worker', 'Gov_Super_Admin'])
def gov_push_ads_list (request ):
    gov_ads = Ads.objects.filter( ad_country = request.user.country_of_residence )
    form = Push_Notifications_Form()

    context = {
        "gov_ads": gov_ads,
        "form":form,
    }
    return render(request , 'gov_panel/push_ads_list.html', context )




@login_required()
@allowed_user(allowed_roles = ['Gov_Worker', 'Gov_Super_Admin'])
def gov_merchant_report (request ):

    best_merchants = Order.objects.select_related('user', 'payment').filter( user__on_boarding_user = request.user ).values('is_ordered', 'user__name', 'user__merchant_business_name', 'user__id').annotate(total=Count('is_ordered') , total_revenue = Sum('order_total')).order_by('-total')[:7]

    jobs = BusinessProfile.objects.filter( user__on_boarding_user = request.user ).values('business_name',).annotate(total_workers=Count('workers') ).order_by('-active')

    job_created_count = 0
    for job in jobs:
        job_created_count += job['total_workers']

    all_active_user = User.objects.select_related('country_of_residence', 'country_province', 'on_boarding_user', 'bank_details').filter( on_boarding_user = request.user , is_active = True )

    users_count = all_active_user.count()
    # gender count
    country_gender_male = all_active_user.filter( gender = 'male').count()
    country_gender_female  = all_active_user.filter( gender = 'female').count() 

    # revenue by province 

    total_merchants_sales = Order.objects.select_related('user', 'payment').filter( user__on_boarding_user = request.user , is_ordered = True).count()

     # getting the best selling products  
    best_selling_product = OrderProduct.objects.select_related('user', 'payment', 'products' , 'order').filter(user__on_boarding_user = request.user  ).values('ordered', 'product__product_name').annotate( total = Count('ordered')).order_by('-total')[:9]


    day_limit = 20
    new_total = 0
    days = []
    daily_sales = []
    for i in range(day_limit):
        Previous_Date = date.today()  - timedelta(days=i)
        days.append(Previous_Date.strftime("%d %b"))

        recent_sale = Order.objects.select_related('user', 'payment').filter( user__on_boarding_user = request.user, is_ordered = True, created_date__date =  Previous_Date )
        
        total_amount = 0
        for r in recent_sale:
            total_amount += r.order_total
            new_total = total_amount

        daily_sales.append(total_amount)

    list_of_province = Country_Province.objects.select_related('country').filter(country=request.user.country_of_residence)
   
   
    province_list = []
    for i in list_of_province:
        p_users = User.objects.select_related('country_of_residence', 'country_province').filter(country_province = i.id, on_boarding_complete = True)

        province_users = p_users.count()
        users_gender_male = p_users.filter( gender = 'male').count()
        users_gender_female  = p_users.filter( gender = 'female').count()

        m_products = Merchant_Product.objects.select_related("user").filter( user__country_province = i.id,user__on_boarding_complete = True ).count()

        province_merchant_sales = Order.objects.select_related("user", "payment").filter( user__country_province = i.id,user__on_boarding_complete = True, is_ordered = True ).count()

        total_sales = OrderProduct.objects.select_related('user', 'payment', 'order', 'product').filter( user__on_boarding_complete = True , user__country_province = i.id, ordered = True )
        total_sale = 0 
        cost_of_sales_province = 0

        # merchant sales via province 
        for c in total_sales:
            total_sale += c.product_total_price
        # merchant cost of sales via province
        for c in total_sales:
            cost_of_sales_province += c.product.cost_price

        sales_profit = total_sale - cost_of_sales_province
        state = "legion"

        note = {
            'province_count':province_users ,
            'province':i.province,
            'province_merchant_sales':province_merchant_sales , 
            'sales':total_sale , 
            'cost_of_sales_province':cost_of_sales_province , 
            'male':users_gender_male , 
            'female':users_gender_female,
            'm_products':m_products,
            'sales_profit':sales_profit,
            'state':state,
            }
        province_list.append(note)


    context = {
        'province':province_list,
       'list_of_province':list_of_province,
       'best_merchants':best_merchants,
       'all_active_user':users_count,
       'total_merchants_sales':total_merchants_sales,
       'days':days,
       'daily_sales':daily_sales,
       'total_amount':total_amount,
       'new_total':new_total,
       'best_selling_product':best_selling_product,
       'job_created_count':job_created_count,
       'country_gender_male':country_gender_male,
       'country_gender_female':country_gender_female,

    }
    return render(request , 'gov_panel/merchant_report.html', context )



@login_required()
@allowed_user(allowed_roles = ['Gov_Worker', 'Gov_Super_Admin'])
def gov_province_report ( request , id ):
    province = id

    best_merchants = Order.objects.select_related('user', 'payment').filter( user__on_boarding_user = request.user , user__country_province = province ).values('is_ordered', 'user__name', 'user__merchant_business_name', 'user__id').annotate(total=Count('is_ordered') , total_revenue = Sum('order_total')).order_by('-total')[:7]

    jobs = BusinessProfile.objects.filter( user__on_boarding_user = request.user , user__country_province = province ).values('business_name',).annotate(total_workers=Count('workers') ).order_by('-active')

    job_created_count = 0
    for job in jobs:
        job_created_count += job['total_workers']

    all_active_user = User.objects.select_related('country_of_residence', 'country_province', 'on_boarding_user', 'bank_details').filter( on_boarding_user = request.user , is_active = True , country_province = province )

    users_count = all_active_user.count()
    # gender count
    country_gender_male = all_active_user.filter( gender = 'male').count()
    country_gender_female  = all_active_user.filter( gender = 'female').count() 

    # revenue by province 

    total_merchants_sales = Order.objects.select_related('user', 'payment').filter( user__on_boarding_user = request.user , user__country_province = province ,is_ordered = True).count()

     # getting the best selling products  
    best_selling_product = OrderProduct.objects.select_related('user', 'payment', 'products' , 'order').filter(user__on_boarding_user = request.user , user__country_province = province ).values('ordered', 'product__product_name').annotate( total = Count('ordered')).order_by('-total')[:9]


    day_limit = 20
    new_total = 0
    days = []
    daily_sales = []
    for i in range(day_limit):
        Previous_Date = date.today()  - timedelta(days=i)
        days.append(Previous_Date.strftime("%d %b"))

        recent_sale = Order.objects.select_related('user', 'payment').filter( user__on_boarding_user = request.user, is_ordered = True, created_date__date =  Previous_Date , user__country_province = province )
        
        total_amount = 0
        for r in recent_sale:
            total_amount += r.order_total
            new_total = total_amount

        daily_sales.append(total_amount)

    list_of_province = Country_Province.objects.select_related('country').filter(country=request.user.country_of_residence )
   
   
    province_list = []
    for i in list_of_province:
        p_users = User.objects.select_related('country_of_residence', 'country_province').filter(country_province = i.id, on_boarding_complete = True)

        province_users = p_users.count()
        users_gender_male = p_users.filter( gender = 'male').count()
        users_gender_female  = p_users.filter( gender = 'female').count()

        m_products = Merchant_Product.objects.select_related("user").filter( user__country_province = i.id,user__on_boarding_complete = True ).count()

        province_merchant_sales = Order.objects.select_related("user", "payment").filter( user__country_province = i.id,user__on_boarding_complete = True, is_ordered = True ).count()

        total_sales = OrderProduct.objects.select_related('user', 'payment', 'order', 'product').filter( user__on_boarding_complete = True , user__country_province = i.id, ordered = True )
        total_sale = 0 
        cost_of_sales_province = 0

        # merchant sales via province 
        for c in total_sales:
            total_sale += c.product_total_price
        # merchant cost of sales via province
        for c in total_sales:
            cost_of_sales_province += c.product.cost_price

        sales_profit = total_sale - cost_of_sales_province
        state = "legion"

        note = {
            'province_count':province_users ,
            'province':i.province,
            'province_merchant_sales':province_merchant_sales , 
            'sales':total_sale , 
            'cost_of_sales_province':cost_of_sales_province , 
            'male':users_gender_male , 
            'female':users_gender_female,
            'm_products':m_products,
            'sales_profit':sales_profit,
            'state':state,
            }
        province_list.append(note) 



    current_province = Country_Province.objects.get( id=province)
    best_merchants = Order.objects.select_related('user', 'payment').filter( user__on_boarding_user = request.user , user__country_province = province ).values('is_ordered', 'user__name', 'user__merchant_business_name').annotate(total=Count('is_ordered') , total_revenue = Sum('order_total')).order_by('-total')[:7]


    day_limit = 20
    new_total = 0
    days = []
    daily_sales = []
    for i in range(day_limit):
        Previous_Date = date.today()  - timedelta(days=i)
        days.append(Previous_Date.strftime("%d %b"))

        recent_sale = Order.objects.select_related('user', 'payment').filter( user__on_boarding_user = request.user, is_ordered = True, created_date__date =  Previous_Date , user__country_province = province )
        
        total_amount = 0
        for r in recent_sale:
            total_amount += r.order_total
            new_total = total_amount

        daily_sales.append(total_amount)

    # calculating the currency convert 
    merchants_revenue = Order.objects.select_related("user", "payment").filter( user__on_boarding_user = request.user, is_ordered = True , user__country_province = province )
    province_total_revenue = 0
    for i in merchants_revenue:
        province_total_revenue += i.order_total
    currency = request.user.default_currency_id
    converted_revenue = usd_currency_converter( currency = currency , amount = province_total_revenue)


    all_gov_users = User.objects.select_related('country_of_residence', 'country_province', 'on_boarding_user', 'bank_details',).filter( on_boarding_complete = True , country_of_residence = request.user.country_of_residence , country_province = id )
    user_count = all_gov_users.count()
    # filter 
    filters_store = Merchants_Filters(request.GET, queryset=all_gov_users)
    all_gov_users = filters_store.qs
    # pagination
    paginator = Paginator(all_gov_users, 100) # Show 200 contacts per page.
    page_number = request.GET.get('page')
    all_gov_users = paginator.get_page(page_number)

    context = {
       'province_report': True,
       'total_revenue_ZAR': province_total_revenue ,  
       'total_revenue_USD': converted_revenue,
       'current_province':current_province,

       'province':province_list,
       'list_of_province':list_of_province,
       'best_merchants':best_merchants,
       'all_active_user':users_count,
       'total_merchants_sales':total_merchants_sales,
       'days':days,
       'daily_sales':daily_sales,
       'total_amount':total_amount,
       'new_total':new_total,
       'best_selling_product':best_selling_product,
       'job_created_count':job_created_count,
       'country_gender_male':country_gender_male,
       'country_gender_female':country_gender_female,

       "all_gov_users":all_gov_users,
        "user_count":user_count,
        'filters_store':filters_store,

    }
    return render(request , 'gov_panel/mm.html', context   )
    

# Onboarding of user and user details
# start here 


@login_required()
@allowed_user(allowed_roles = ['Gov_Worker', 'Gov_Super_Admin'])
def pdf (request):
    """
    this pdf function holds the national report for the states
    or province which will be generated by the government. 
    """
    today = datetime.now()
    # onboarding_dates = Onboarding_Users_CSV.objects.filter ( on_boarding_user__country_of_residence = request.user.country_of_residence )[:1]
    # for onboarding_date in onboarding_dates:
    #     onboarding_date_start = onboarding_date.on_boarding_complete_date
   

    best_merchants = Order.objects.select_related('user', 'payment').filter( user__on_boarding_user = request.user ).values('is_ordered', 'user__name', 'user__merchant_business_name', 'user__id').annotate(total=Count('is_ordered') , total_revenue = Sum('order_total')).order_by('-total')[:7]

    all_active_user = User.objects.select_related('country_of_residence', 'country_province', 'on_boarding_user', 'bank_details').filter( on_boarding_user = request.user , is_active = True ).count()

    total_merchants_sales = Order.objects.select_related('user', 'payment').filter( user__on_boarding_user = request.user , is_ordered = True)


    total_cost_sales = OrderProduct.objects.select_related('user', 'payment', 'order', 'product').filter( user__on_boarding_user = request.user , ordered = True )

    revenue = 0
    cost_of_sales = 0

    # getting the total cost and revenue
    for i in total_merchants_sales:
        revenue += i.order_total

    for c in total_cost_sales:
        cost_of_sales += c.product.cost_price

    # endhere 
    
    # getting all payment sales revenue for each merchant
    payment_qs = Payment.objects.select_related('user').filter( user__on_boarding_user = request.user , verified = True )

    sales_payments_type = payment_qs.values('verified', 'payment_method' ).annotate( total_revenue = Sum('amount_paid'), total = Count('verified') ).order_by('-verified')

    # best selling category of all national payments
    best_selling_category = total_cost_sales.values('ordered', 'product__category__category' ).annotate( total_revenue = Sum('product_total_price'), total = Count('ordered') , total_merchants = Count('user') ).order_by('-total_merchants')[:5]

    # province performance 
    Provincial_Performance = total_cost_sales.values('ordered', 'user__country_province__province' ).annotate( total_revenue = Sum('product_total_price'), total = Count('ordered') ).order_by('-ordered')[:5]

    list_of_province = Country_Province.objects.select_related('country').filter(country=request.user.country_of_residence)

    province_data = []

    for i in list_of_province:
        province_users = User.objects.select_related('country_of_residence', 'country_province').filter(country_province = i.id, on_boarding_user = request.user).count()
  
        province_merchant_sales = Order.objects.select_related("user", "payment").filter( user__country_province = i.id,user__on_boarding_user = request.user, is_ordered = True ).count()

        total_sales = OrderProduct.objects.select_related('user', 'payment', 'order', 'product').filter( user__on_boarding_user = request.user , user__country_province = i.id, ordered = True ).values('ordered' ).annotate( total_sale = Sum('product_total_price') , cost_of_sales_province = Sum('product__cost_price') ).order_by('-ordered')

        # best selling category of all national payments
        province_best_selling_category = OrderProduct.objects.select_related('user', 'payment', 'order', 'product').filter( user__on_boarding_user = request.user ,user__country_province = i.id, ordered = True ).values('ordered', 'product__category__category' ).annotate( total_revenue = Sum('product_total_price'), total = Count('ordered') , total_merchants = Count('user') ).order_by('-total_merchants')[:5]


        # best selling category of the current province 
        province_sales_payments_type = Payment.objects.select_related('user').filter( user__on_boarding_user = request.user , verified = True , user__country_province = i.id ).values('verified', 'payment_method' ).annotate( total_revenue = Sum('amount_paid'), total = Count('verified') ).order_by('-verified')

        # general province or state report 
        province_report = { 'province':i.province , 'total_merchants':province_users, 'total_sales':total_sales , 'province_id':i.id , 'province_sales_payments_type':province_sales_payments_type , 'province_best_selling_category':province_best_selling_category }

        province_data.append(province_report)

    # print(province_data)

    total_merchants_sales_count = total_merchants_sales.count()


    # context here
    context = {
        'today':today,
        # 'from_date':onboarding_date_start,
        'best_merchants': best_merchants,
        'all_active_user': all_active_user,
        'total_merchants_sales': total_merchants_sales,
        'total_merchants_sales_count':total_merchants_sales_count,
        'revenue':revenue,
        'cost_of_sales':cost_of_sales,
        'sales_payments_type':sales_payments_type,
        'best_selling_category':best_selling_category,
        'province_data':province_data,
        'list_of_province':list_of_province,
    }
    # context here 
    return render(request , 'gov_panel/pdf_report.html', context )


@login_required()
@allowed_user(allowed_roles = ['Gov_Worker', 'Gov_Super_Admin'])
def onboarding_process (request):
    users_csv_file = Onboarding_Users_CSV.objects.select_related('on_boarding_user').filter( on_boarding_complete = False )
    for i in users_csv_file:
        onboarding_user = i.on_boarding_user
        new_file = i.on_boarding_user_file.name
        with storage.open(new_file, 'r') as f:
            csvf = csv.reader(f)
            data = []
        
            try:
                for id,first_name,last_name,email,business_name,province, *__ in csvf:
                    # generating unique password 
                    password = password_geenrate()
                    # getting each province ID 
                    user_province = Country_Province.objects.get( id = province )
                    
                    checking_user = User.objects.filter(email=email)
                    if checking_user:
                        pass
                    else:
                        wallet_id = ref_code()

                        user = User(
                            email=email,
                            first_name=first_name, 
                            last_name=last_name,
                            name = first_name + ' ' + last_name,
                            merchant_business_name=business_name,
                            account_type = "merchant",
                            wallet_id = wallet_id,
                            country_of_residence = onboarding_user.country_of_residence,
                            country_province = user_province,
                            default_currency_id = onboarding_user.default_currency_id,
                            on_boarding_user = onboarding_user,
                            on_boarding_complete = True,
                            accept_terms = True,
                            agreed_to_data_usage = True,
                            )
                        user.set_password(password)
                        data.append(user)
                User.objects.bulk_create(data)
                i.on_boarding_complete = True
                i.on_boarding_complete_date = datetime.now()
                i.save()
                return JsonResponse ('users registration is handled', safe = False)
            except ValueError:
                users_csv_file.delete()
                return JsonResponse ('users transfer not handled', safe = False)
            
    return JsonResponse ('users registration', safe = False)


@login_required()
@allowed_user(allowed_roles = ['Gov_Worker', 'Gov_Super_Admin'])
def gov_store_list (request ):
    if request.user.country_of_residence.iso2 == "NG":
        all_gov_stores = BusinessProfile.objects.select_related('user').filter( user__government_registered = True  )

        nigerian_users = BusinessProfile.objects.select_related('user').filter( user__country_of_residence__iso2 = "NG" ).count()

        # gender count
        country_gender_male = all_gov_stores.filter(  user__gender = 'male').count()
        country_gender_female  = all_gov_stores.filter(  user__gender = 'female').count()

        # calculating the currency convert 
        merchants_revenue = Order.objects.select_related("user", "payment").filter( user__government_registered = True , is_ordered = True )
        total_revenue = 0
        for i in merchants_revenue:
            total_revenue += i.order_total
        currency = request.user.default_currency_id

    else:
        all_gov_stores = BusinessProfile.objects.select_related('user').filter( user__on_boarding_complete = True , user__country_of_residence = request.user.country_of_residence )
        nigerian_users = 0
        total_revenue = 0
        country_gender_male = 0
        currency = None
        country_gender_female = 0
    user_count = all_gov_stores.count()

     # filter 
    filters_store = Business_Filters(request.GET, queryset=all_gov_stores)
    all_gov_stores = filters_store.qs
   
    # pagination
    paginator = Paginator(all_gov_stores, 100) # Show 200 contacts per page.
    page_number = request.GET.get('page')
    all_gov_stores = paginator.get_page(page_number)

    context = {
        "all_gov_stores":all_gov_stores,
        "user_count":user_count,
        'filters_store':filters_store,
        'nigerian_users':nigerian_users,
        'total_revenue':total_revenue,
        'currency':currency,
        'country_gender_male':country_gender_male,
        'country_gender_female':country_gender_female,
       
    }
    return render(request , 'gov_panel/list_of_stores.html', context)




@login_required()
@allowed_user(allowed_roles = ['Gov_Worker', 'Gov_Super_Admin'])
def gov_store_details (request , id ):
    # # getting the merchant business account
    try:
        store_details = BusinessProfile.objects.select_related('user').get( id = id  )
        store_products = Merchant_Product.objects.select_related('user', 'business_profile', 'category').filter( business_profile = store_details )
    except BusinessProfile.DoesNotExist:
        return redirect(gov_store_list)
    
    store_id = id 
    
    # # pagination
    # paginator = Paginator(store_products, 100) # Show 200 contacts per page.
    # page_number = request.GET.get('page')
    # store_products = paginator.get_page(page_number)

    # # getting the user ID 
    # user_id = store_details.user.id

    # # getting all payment sales revenue for each merchant
    # merchant_revenue = Payment.objects.select_related('user').filter(  user_id = user_id  ).values('verified','user__name', 'user__merchant_business_name', 'payment_method' ).annotate( total_revenue = Sum('amount_paid'), total = Count('verified') ).order_by('-verified')
    # # Serialize and attach the chart data to the template context
    # # Serialize and attach the chart data to the template context
    # as_json = json.dumps(list(merchant_revenue), cls=DjangoJSONEncoder)
    # print(as_json)
    # print(merchant_revenue)
    # # extra_context = extra_context or {"chart_data": as_json}


    # # getting the best selling products  
    # best_selling_product = OrderProduct.objects.select_related('user', 'payment', 'products' , 'order').filter(user__id = user_id  ).values('ordered', 'product__product_name').annotate(total = Count('ordered')).order_by('-total')[:9]

    # # getting merchant workers if any 
    # try:
    #     worker = BusinessProfile.objects.filter( user__id = user_id, active = True )
    # except BusinessProfile.DoesNotExist:
    #     worker = None

    # # getting merchants daily sales 
    # day_limit = 20
    # new_total = 0
    # days = []
    # daily_sales = []
    # for i in range(day_limit):
    #     Previous_Date = date.today()  - timedelta(days=i)
    #     days.append(Previous_Date.strftime("%d %b"))

    #     recent_sale = Order.objects.select_related('user', 'payment').filter( user = id, is_ordered = True, created_date__date =  Previous_Date )
        
    #     total_amount = 0
    #     for r in recent_sale:
    #         total_amount += r.order_total
    #         new_total = total_amount

    #     daily_sales.append(total_amount)

    # print(daily_sales)
    
    context = {
        'store_details':store_details,
        'store_id': store_id
        # 'store_products':store_products,
        # 'merchant_revenue':merchant_revenue,
        # 'best_selling_product':best_selling_product,
        # 'worker':worker,
        # 'daily_sales':daily_sales,
        # 'days':days,
    }
    return render(request , 'gov_panel/store_details/details.html', context)




@login_required()
@allowed_user(allowed_roles = ['Gov_Worker', 'Gov_Super_Admin'])
def store_revenue (request , id ):
    store_id = id 
    # # getting the merchant business account
    try:
        store_details = BusinessProfile.objects.select_related('user').get( id = id  )
        store_products = Merchant_Product.objects.select_related('user', 'business_profile', 'category').filter( business_profile = store_details )
    except BusinessProfile.DoesNotExist:
        return redirect(gov_store_list)
    
    m_products = Merchant_Product.objects.select_related("user").filter( user = store_details.user,user__on_boarding_complete = True ).count()

    province_merchant_sales = Order.objects.select_related("user", "payment").filter( user = store_details.user,user__on_boarding_complete = True, is_ordered = True ).count()

    total_sales = OrderProduct.objects.select_related('user', 'payment', 'order', 'product').filter( user__on_boarding_complete = True , user = store_details.user, ordered = True )
    total_sale = 0 
    cost_of_sales_province = 0

    # merchant sales via province 
    for c in total_sales:
        total_sale += c.product_total_price
    # merchant cost of sales via province
    for c in total_sales:
        cost_of_sales_province += c.product.cost_price

    sales_profit = total_sale - cost_of_sales_province

    best_selling_product = OrderProduct.objects.select_related('user', 'payment', 'products' , 'order').filter(user = store_details.user  ).values('ordered', 'product__product_name').annotate(total = Count('ordered')).order_by('-total')[:9]

    total_cost_sales = OrderProduct.objects.select_related('user', 'payment', 'order', 'product').filter( user = store_details.user  , ordered = True )

    currency = store_details.user.default_currency_id

    # best selling category of all national payments
    best_selling_category = total_cost_sales.values('ordered', 'product__category__category', 'user__default_currency_id' ).annotate( total_revenue = Sum('product_total_price'), total = Count('ordered') , total_merchants = Count('user') ).order_by('-total_merchants')[:5]

    # getting merchants daily sales 
    day_limit = 20
    new_total = 0
    days = []
    daily_sales = []
    for i in range(day_limit):
        Previous_Date = date.today()  - timedelta(days=i)
        days.append(Previous_Date.strftime("%d %b"))

        recent_sale = Order.objects.select_related('user', 'payment').filter( user = store_details.user, is_ordered = True, created_date__date =  Previous_Date )
        
        total_amount = 0
        for r in recent_sale:
            total_amount += r.order_total
            new_total = total_amount

        daily_sales.append(total_amount)

    print(best_selling_category)

    # getting all payment sales revenue for each merchant
    merchant_revenue = Payment.objects.select_related('user').filter(  user_id = store_details.user.id  ).values('verified','user__name', 'user__merchant_business_name', 'payment_method' ).annotate( total_revenue = Sum('amount_paid'), total = Count('verified') ).order_by('-verified')
    # Serialize and attach the chart data to the template context
    # Serialize and attach the chart data to the template context
    # as_json = json.dumps(list(merchant_revenue), cls=DjangoJSONEncoder)
    # print(as_json)
    # print(merchant_revenue)
    # extra_context = extra_context or {"chart_data": as_json}

    # getting merchant workers if any 
    try:
        worker = BusinessProfile.objects.filter( user__id = store_details.user.id, active = True )
    except BusinessProfile.DoesNotExist:
        worker = None
    total_amount = 0
    sales = Order.objects.select_related("user", "payment").filter(  user = store_details.user, is_ordered = True  )
    for i in sales:
        total_amount += i.order_total
    total_amount = Decimal(total_amount)

    
    
    context = {
        'store_id': store_id,
        'm_products':m_products,
        'sales_profit':sales_profit,
        'total_sale':total_sale,
        'cost_of_sales_province':cost_of_sales_province,
        'best_selling_product':best_selling_product,
        'best_selling_category':best_selling_category,
        'daily_sales':daily_sales,
        'days':days,
        'daily_sales':daily_sales,
        'currency':currency,
        'merchant_revenue':merchant_revenue,
        'worker':worker,
        'total_amount':total_amount,



    }
    return render(request , 'gov_panel/store_details/financial.html', context )



@login_required()
@allowed_user(allowed_roles = ['Gov_Worker', 'Gov_Super_Admin'])
def store_products_list (request , id ):
    store_id = id 
    # # getting the merchant business account
    try:
        store_details = BusinessProfile.objects.select_related('user').get( id = id  )
        store_products = Merchant_Product.objects.select_related('user', 'business_profile', 'category').filter( business_profile = store_details )
    except BusinessProfile.DoesNotExist:
        return redirect(gov_store_list)
    
    m_products = Merchant_Product.objects.all().filter( user = store_details.user.id )
    # pagination
    paginator = Paginator(m_products, 100) # Show 200 contacts per page.
    page_number = request.GET.get('page')
    m_products = paginator.get_page(page_number)

    context = {
        'm_products':m_products,
        'store_id':store_id
    }
    return render(request , 'gov_panel/store_details/products.html', context )
    

@login_required()
@allowed_user(allowed_roles = ['Gov_Worker', 'Gov_Super_Admin'])
def store_workers (request , id ):
    store_id = id 
    # # getting the merchant business account
    try:
        store_details = BusinessProfile.objects.select_related('user').get( id = id  )
        store_products = Merchant_Product.objects.select_related('user', 'business_profile', 'category').filter( business_profile = store_details )
    except BusinessProfile.DoesNotExist:
        return redirect(gov_store_list)
    
    # getting merchant workers if any 
    try:
        worker = BusinessProfile.objects.filter( user__id = store_details.user.id, active = True )
    except BusinessProfile.DoesNotExist:
        worker = None

    context = {
        'store_id':store_id,
        'worker':worker,

    }
    return render(request , 'gov_panel/store_details/worker.html', context )
    



@login_required()
@allowed_user(allowed_roles = ['Gov_Worker', 'Gov_Super_Admin'])
def store_by_province (request , id ):
    try:
        qs = Country_Province.objects.get (id = id )
    except qs.DoesNotExist:
        return redirect(gov_store_list)
    if request.user.country_of_residence.iso2 == "NG":
        all_gov_stores = BusinessProfile.objects.select_related('user').filter( user__government_registered = True , user__country_province = id)

        nigerian_users = BusinessProfile.objects.select_related('user').filter( user__country_of_residence__iso2 = "NG" ).count()

        # gender count
        country_gender_male = all_gov_stores.filter(  user__gender = 'male').count()
        country_gender_female  = all_gov_stores.filter(  user__gender = 'female').count()

        # calculating the currency convert 
        merchants_revenue = Order.objects.select_related("user", "payment").filter( user__government_registered = True , is_ordered = True )
        total_revenue = 0
        for i in merchants_revenue:
            total_revenue += i.order_total
        currency = request.user.default_currency_id

    else:
        all_gov_stores = BusinessProfile.objects.select_related('user').filter( user__country_province = id , user__country_of_residence = request.user.country_of_residence )
        nigerian_users = 0
        total_revenue = 0
        country_gender_male = 0
        currency = None
        country_gender_female = 0


    user_count = all_gov_stores.count()
     # filter 
    filters_store = Business_Filters(request.GET, queryset=all_gov_stores)
    all_gov_stores = filters_store.qs

    # pagination
    paginator = Paginator(all_gov_stores, 100) # Show 200 contacts per page.
    page_number = request.GET.get('page')
    all_gov_stores = paginator.get_page(page_number)


    context = {
        'qs':qs,
        "all_gov_stores":all_gov_stores,
        "user_count":user_count,
        'filters_store':filters_store,
        'nigerian_users':nigerian_users,
        'total_revenue':total_revenue,
        'currency':currency,
        'country_gender_male':country_gender_male,
        'country_gender_female':country_gender_female,
    }
    return render(request , 'gov_panel/list_of_stores.html', context)



@login_required()
@allowed_user(allowed_roles = ['Gov_Worker', 'Gov_Super_Admin'])
def users_by_province ( request , id  ):
    try:
        qs = Country_Province.objects.get ( id = id )
    except qs.DoesNotExist:
        return redirect(gov_store_list)
    
    if request.user.country_of_residence.iso2 == "NG":
        all_gov_users = User.objects.select_related('country_of_residence', 'country_province', 'on_boarding_user', 'bank_details',).filter( government_registered = True, country_province = id )

        nigerian_users = User.objects.select_related('country_of_residence', 'country_province', 'on_boarding_user', 'bank_details',).filter( country_of_residence__iso2 = "NG" ).count()
        # gender count
        country_gender_male = all_gov_users.filter( gender = 'male').count()
        country_gender_female  = all_gov_users.filter( gender = 'female').count()
        # calculating the currency convert 
        merchants_revenue = Order.objects.select_related("user", "payment").filter( user__government_registered = True , is_ordered = True , user__country_province = id)
        total_revenue = 0
        for i in merchants_revenue:
            total_revenue += i.order_total
        currency = request.user.default_currency_id

    else:
        all_gov_users = User.objects.select_related('country_of_residence', 'country_province', 'on_boarding_user', 'bank_details',).filter( on_boarding_complete = True , country_of_residence = request.user.country_of_residence , country_province = id )

    user_count = all_gov_users.count()
    # filter 
    filters_store = Merchants_Filters(request.GET, queryset=all_gov_users)
    all_gov_users = filters_store.qs
    # pagination
    paginator = Paginator(all_gov_users, 100) # Show 200 contacts per page.
    page_number = request.GET.get('page')
    all_gov_users = paginator.get_page(page_number)

    context = {
        "all_gov_users":all_gov_users,
        "user_count":user_count,
        'qs':qs,
        'filters_store':filters_store,
        'nigerian_users':nigerian_users,
        'total_revenue':total_revenue,
        'currency':currency,
        'country_gender_male':country_gender_male,
        'country_gender_female':country_gender_female,
    }
    return render(request , 'gov_panel/gov_users_list.html', context)


@login_required()
@allowed_user(allowed_roles = ['Gov_Worker', 'Gov_Super_Admin'])
def nasme_users ( request , id  ):
    try:
        qs = Government_Organizations.objects.get ( id = id )
    except qs.DoesNotExist:
        return redirect(gov_store_list)
    
    all_gov_users = User.objects.select_related('country_of_residence', 'country_province', 'on_boarding_user', 'bank_details',).filter( government_registered = True, government_organization_name = id )

    nigerian_users = User.objects.select_related('country_of_residence', 'country_province', 'on_boarding_user', 'bank_details',).filter( country_of_residence__iso2 = "NG" ).count()
    # gender count
    country_gender_male = all_gov_users.filter( gender = 'male').count()
    country_gender_female  = all_gov_users.filter( gender = 'female').count()
    # calculating the currency convert 
    merchants_revenue = Order.objects.select_related("user", "payment").filter( user__government_registered = True , is_ordered = True , user__government_organization_name = id)
    total_revenue = 0
    for i in merchants_revenue:
        total_revenue += i.order_total
    currency = request.user.default_currency_id
   

    user_count = all_gov_users.count()
    # filter 
    filters_store = Merchants_Filters(request.GET, queryset=all_gov_users)
    all_gov_users = filters_store.qs
    # pagination
    paginator = Paginator(all_gov_users, 100) # Show 200 contacts per page.
    page_number = request.GET.get('page')
    all_gov_users = paginator.get_page(page_number)

    context = {
        "all_gov_users":all_gov_users,
        "user_count":user_count,
        'qs':qs,
        'filters_store':filters_store,
        'nigerian_users':nigerian_users,
        'total_revenue':total_revenue,
        'currency':currency,
        'country_gender_male':country_gender_male,
        'country_gender_female':country_gender_female,
    }
    return render(request , 'gov_panel/gov_users_list.html', context)


@login_required()
@allowed_user(allowed_roles = ['Gov_Worker', 'Gov_Super_Admin'])
def gov_workers (request ):
        
    
    try:
        worker = User.objects.filter( groups__name = "Gov_Worker" )
    except worker.DoesNotExist:
        worker = None

    context = {
        'worker':worker,
    }
    return render(request, 'gov_panel/workers.html', context)



@login_required()
@allowed_user(allowed_roles = ['Gov_Worker', 'Gov_Super_Admin'])
def verify_gov_worker ( request ):

    title = f'Gov Worker Email Verification'
    description = f'This section requires your worker email address for verification, if the email address is registered with any of our platforms , their details will automatically be verified .'
    form_title = f'Email Verification'
    submit_button = f'Click To Verify Email'

    # end worker restriction
     
    form = VerifyEmail()
    if request.method == 'POST':
        form = VerifyEmail(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            opt_pin = opt_code()

            # try:
            #     worker_id = User.objects.get( email = email )
            #     messages.info(request, f"{email} is already registered as a worker on kroon kiosk platform.")
            #     return HttpResponseRedirect(request.path_info)
            # except User.DoesNotExist:
            #     pass


            try:
                user_info = User.objects.get( email = email )
                request.session['email'] = user_info.email

                # send an otp to the worker requestiing the merchant to
                # provide it so to enable the successful worker registeration
                # checking if the user already have an otp
                OPTs.objects.filter(email=email).delete()
                OPTs.objects.create(email=email,otp_code= opt_pin)
                #  sending email to the customer alerting him of the succesful transfer 
                subject = 'Kiosk OTP Verification'
                html_message = render_to_string(
                    'kiosk_emails/otp.html',
                    {

                    'user': "Dear",
                    'opt': opt_pin,
                    'content': f"Your account is about to be registered as a government worker , kindly provide the following PIN to confirm your action which will be performed by your employer , note! some personal information will be displayed to the employer for clearifications, you can ignore this message if you havent applied for any position — this OTP code will expire in 5 minutes:",

                    } 
                )
                plain_message = strip_tags(html_message)
                from_email = f"{settings.EMAIL_HOST_USER}" 
            
                to = email
                mail.send_mail(subject, plain_message, from_email, [to], html_message = html_message)
                # store otp 

                return redirect('verify_gov_worker_opt')

            except User.DoesNotExist:
                request.session['email'] = email
                # send an otp to the worker requestiing the merchant to
                # provide it so to enable the successful worker registeration
                # checking if the user already have an otp
                OPTs.objects.filter(email=email).delete()
                OPTs.objects.create(email=email,otp_code= opt_pin)
                #  sending email to the customer alerting him of the succesful transfer 
                subject = 'Kiosk OTP Verification'
                html_message = render_to_string(
                    'kiosk_emails/otp.html',
                    {

                    'user': "Dear",
                    'opt': opt_pin,
                    'content': f"Your account is about to be registered as a government worker , kindly provide the following PIN to confirm your action which will be performed by your employer , note! some personal information will be displayed to the employer for clearifications, you can ignore this message if you havent applied for any position — this OTP code will expire in 5 minutes:",

                    } 
                )
                plain_message = strip_tags(html_message)
                from_email = f"{settings.EMAIL_HOST_USER}" 
            
                to = email
                mail.send_mail(subject, plain_message, from_email, [to], html_message = html_message)
                # store otp 

                return redirect('verify_gov_worker_opt')

                # return redirect('gov_register_worker')

    context = {
        'form': form,
        # contents
        'title':title,
        'description':description,
        'form_title':form_title,
        'submit_button':submit_button,

        }
    return render(request , 'gov_panel/verify_gov_worker.html', context)



@login_required()
@allowed_user(allowed_roles = ['Gov_Worker', 'Gov_Super_Admin'])
def verify_gov_worker_opt ( request ):

    title = f'Worker Code Verification'
    description = f'This section requires your worker code for verification, if the code  is valid , their information will be displayed to you for verification.'
    form_title = f'Worker Code Verification'
    submit_button = f'Click To Verify Worker Code'

    form = WorkerVerifyOtp()
    if request.method == 'POST':
        form = WorkerVerifyOtp(request.POST)
        if form.is_valid():
            otp_pin = form.cleaned_data.get('code')

            if request.session['email'] == None:
                return redirect( verify_gov_worker )
            email = request.session.get('email')

            # validating OTP pin 
            if email:
                try:
                    check_otp = OPTs.objects.get( otp_code = otp_pin, email = email )
                except OPTs.DoesNotExist:
                    messages.info(request, f"OTP pin is invalid, kindly check your input.")
                    return HttpResponseRedirect(request.path_info)
                
                #checking and verifying if the pin is invalid or expired  
                current_time = datetime.now()
                # check_otp_duration = utc.localize(check_otp.duration)
                current_time = utc.localize(current_time)
                
                if check_otp.duration < current_time:
                    messages.info(request, f"OTP pin has expired")
                    return HttpResponseRedirect(request.path_info)
                else:
                    check_otp.delete()
                    messages.info(request, f"OTP pin is valid")
                    try:
                        User.objects.get( email = email )
                        print('already user')
                        return redirect('gov_add_workers')
                    except User.DoesNotExist:
                        print('new user')
                        return redirect('gov_register_worker')

            else:
                messages.info(request, f"Opt pin is invalid or expired")
                return HttpResponseRedirect(request.path_info)

    context = {
        'form': form,
        # contents
        'title':title,
        'description':description,
        'form_title':form_title,
        'submit_button':submit_button,

       
    }
    
    return render(request, 'gov_panel/verify_worker_otp.html', context )



@login_required()
@allowed_user(allowed_roles = ['Gov_Worker', 'Gov_Super_Admin'])
def gov_register_worker (request):
   
    title = f'Create Workers Account'
    description = f'This section creates your workers account which will automatically create an account for our platforms such as Kroon and Kroon Kiosk, if kroon app is been allowed in your region , your workers can easily make use of kroon app.'
    form_title = f'Account Creation'
    submit_button = f'Click To Register'

    if request.session['email'] == None:
        return redirect('verify_gov_worker')

    form = Gov_Worker_SignupForm()
    if request.method == 'POST':
        form = Gov_Worker_SignupForm(request.POST)
        if form.is_valid():
            form.instance.default_currency_id = request.user.default_currency_id
            form.instance.on_boarding_user = request.user
            form.instance.on_boarding_complete = True
            form.instance.email_details = True
            form.instance.accept_terms = True
            form.instance.agreed_to_data_usage = True
            form.instance.email_verification = True
            form.instance.name = form.cleaned_data['first_name'] + " " + form.cleaned_data['last_name']
            form.instance.groups.add(Group.objects.get( name = "Gov_Worker" ))
            form.save(request)
            # adding the new worker the companys account as a worker 
            # merchant_business = BusinessProfile.objects.get( user = request.user, active = True )
            # merchant_business.workers.add(user)
            # Sending login details to the government worker that is registered 
            email = request.session['email']
            name = form.cleaned_data['first_name'] + " " + form.cleaned_data['last_name']
            default_password = form.cleaned_data.get('password1')
            # email notification for topup_payment
            subject = 'Login Details - Kroon Kiosk'
            html_message = render_to_string(
                'emails/onboarding_mail.html',
                {
                'name': name,
                'email':email,
                'default_password':default_password,
                } 
            )
            plain_message = strip_tags(html_message)
            from_email = f"{settings.EMAIL_HOST_USER}" 
            to = email
            mail.send_mail(subject, plain_message, from_email, [to], html_message = html_message)


            request.session['email'] = None
            messages.info(request, f"Worker has been added successfully")
            return redirect(gov_workers)

    context = {
        'form': form,
        # contents
        'title':title,
        'description':description,
        'form_title':form_title,
        'submit_button':submit_button,
      
        }

    return render(request, 'gov_panel/verify_gov_worker.html', context)


@login_required()
@allowed_user(allowed_roles = ['Gov_Worker', 'Gov_Super_Admin'])
def gov_add_workers (request):
    """
    this function stores alreaduy registered users to the join the 
    government workers.
    """
    
    if request.session['email'] == None:
        return redirect('verify_gov_worker')

    email = request.session.get('email')
    user_profile_set = User.objects.get ( email = email )

    if request.method == 'POST':
        # adding the new worker the companys account as a worker
        user_profile_set.groups.add(Group.objects.get( name = "Gov_Worker" ))
        user_profile_set.save()
        request.session['email'] = None
        messages.info(request, f"{user_profile_set} has been added as a government worker successfully ")
        return redirect('gov_workers')


    context = {
        'user_profile_set':user_profile_set,
    }

    return render(request, 'gov_panel/gov_add_worker.html', context)
    


@login_required()
@allowed_user(allowed_roles = ['Gov_Worker', 'Gov_Super_Admin'])
def broswer_logs (request):
    
    return render(request, 'gov_panel/broswers_log.html', context = None )


@login_required()
@allowed_user(allowed_roles = ['Gov_Worker', 'Gov_Super_Admin'])
def gov_actions_logs (request):
    # getting all the list of gov worker action logs 
    gov_action_logs = Action_logs.objects.all().order_by('-created_date')[:20]
    # log context 
    context = {
        'gov_action_logs':gov_action_logs,
    }
    return render(request, 'gov_panel/action_logs.html', context )
    

@login_required()
@allowed_user(allowed_roles = ['Gov_Worker', 'Gov_Super_Admin'])
def gov_remove_workers ( request , email ):
    # getting the worker email 
    worker_email = email
    print(worker_email)
    if worker_email is not None:
        try:
            worker_account = User.objects.get( email = worker_email , groups = (Group.objects.get( name = "Gov_Worker" )) )
        except User.DoesNotExist:
            messages.info(request, f"{worker_email} vvvis not a government worker or cant be found ")
            return redirect('gov_workers')
        
        worker_account.groups.remove(Group.objects.get( name = "Gov_Worker" ))
        worker_account.save()
        messages.info(request, f"{worker_email} is been removed as a government worker")
        return redirect('gov_workers')
    
    else:
        messages.info(request, f"{worker_email} is not a government worker or cant be found ")
        return redirect('gov_workers')


@login_required()
@allowed_user(allowed_roles = ['Gov_Worker', 'Gov_Super_Admin'])
def gov_account_settings ( request ):
    user_password = PasswordChangeForm(request.user)

    if request.method == 'POST':
        user_password = PasswordChangeForm(request.user, request.POST)
        if user_password.is_valid():
            user = user_password.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return HttpResponseRedirect(request.path_info)
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        user_password = PasswordChangeForm(request.user)

    context = {
        'user_password':user_password,
    }
    return render(request, 'gov_panel/change_password.html', context )
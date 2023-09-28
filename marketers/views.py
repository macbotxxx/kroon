import re
import requests
import json

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.conf import settings
from django.core.paginator import Paginator
from ads.models import Ads
from locations.models import Country

# django email settings
from django.core import mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
import threading

from kroon.users.models import User
from helpers.common.decorators import admin_only, allowed_user
from .forms import General_Push_Notification_Mobile,Email_Notification,General_Push_Notification_Mobile_Per_Country, Email_Notification_Per_Country, general_ad_form, general_news_feed

from transactions.models import  Transactions
from payments.models import Payment_Topup



import string
import random

import datetime
import pytz

utc=pytz.UTC

from datetime import datetime, timezone


FCM_SERVER_KEY = settings.FCM_SERVER_KEY


# Create your views here.
@login_required()
@allowed_user(allowed_roles = ['Marketers'])
def marketer_index (request):
    """
    kroon marketers are incharge of the ads and many functionalities
    here is the index page for marketers dashbaord
    """
    user_count_per_country = User.objects.values('country_of_residence__iso2', 'country_of_residence__name').annotate(number=Count('id')).order_by('country_of_residence')
    
    print(user_count_per_country)

    total_user_count = User.objects.all().count()
    total_active_users = User.objects.filter(is_active = True).count()
    total_nonactive_count = User.objects.filter(is_active = False).count()

    user_month = User.objects.all().extra({'created': "to_char(date_joined, 'YYYY/MM')"}).values('created').annotate(created_count=Count('id')).order_by('-created')

    user_this_month =User.objects.all().extra({'created': "to_char(date_joined, 'YYYY/MM')"}).values('created').annotate(created_count=Count('id')).order_by('-created')[:1]

    print(user_this_month)

    context = {

        'user_count_per_country':user_count_per_country,
        'total_user_count':total_user_count,
        'total_active_users':total_active_users,
        'total_nonactive_count':total_nonactive_count,
        'user_month':user_month,
        'user_this_month':user_this_month,
    }

    return render(request, 'marketers/index.html', context)

# Create your views here.
@login_required()
@allowed_user(allowed_roles = ['Marketers'])
def users_index (request):
    """
    kroon marketers are incharge of the ads and many functionalities
    here is the index page for marketers dashbaord
    """
    user_count_per_country = User.objects.values('country_of_residence__iso2', 'country_of_residence__name').annotate(
        number=Count('id')
    ).order_by('country_of_residence')
    
    print(user_count_per_country)

    total_user_count = User.objects.all().count()
    total_active_users = User.objects.filter(is_active = True).count()
    total_male_users = User.objects.filter(is_active = True, gender = 'male').count()
    total_female_users = User.objects.filter(is_active = True, gender = 'female').count()
    total_nonactive_count = User.objects.filter(is_active = False).count()

    current_month = datetime.month
    user_month =User.objects.all().extra({'created': "to_char(date_joined, 'YYYY/MM')"}).values('created').annotate(created_count=Count('id')).order_by('-created')

    print(user_month)

    context = {
        'user_count_per_country':user_count_per_country,
        'total_user_count':total_user_count,
        'total_active_users':total_active_users,
        'total_nonactive_count':total_nonactive_count,
        'total_male_users':total_male_users,
        'total_female_users':total_female_users,
        'user_month':user_month,
    }

    return render(request, 'marketers/users_info.html', context)



"""
this section hold the user details and to send personal notifications
either through email or mobile push notifications
""" 

@login_required()
@allowed_user(allowed_roles = ['Marketers'])
def user_details (request, user_id):
    """
    this view shows user details which the user id needs to be passed
    """
    user_details = User.objects.get(id = user_id)
    context = {
        'user_details': user_details
        }

    return render(request, 'marketers/user_details.html', context)


@login_required()
@allowed_user(allowed_roles = ['Marketers'])
def personal_push_notifications (request, user_id):
    """
    this section sends personal notifications to the user
    """

    form = General_Push_Notification_Mobile()

    if request.method == 'POST':
        form = General_Push_Notification_Mobile(request.POST)
        if form.is_valid():
            title = form.cleaned_data.get('title')
            message = form.cleaned_data.get('message')

            # getting all kroon and kiosk users 
            user_device = User.objects.get(id = user_id)
         
            # FCM push-notifications
            serverToken = f'{FCM_SERVER_KEY}'
            deviceToken = f'{user_device.device_id}'
            headers = {
                    'Content-Type': 'application/json',
                    'Authorization': 'key=' + serverToken,
                }
            body = {
                    'notification': {
                                    'title': f'{title}',
                                    'body': f'Hey {user_device.name}, {message} #KroonMan' ,
                                    'sound': 'default',
                                    },
                    'to':deviceToken,
                    'priority': 'high',
                    #   'data': dataPayLoad,
                    }
            response = requests.post("https://fcm.googleapis.com/fcm/send",headers = headers, data=json.dumps(body))

    context = {
        'form': form
        }

    return render(request, 'marketers/personal_notify.html', context)
    

@login_required()
@allowed_user(allowed_roles = ['Marketers'])
def general_email_notification (request):
    """
    send personal email
    """

    form = Email_Notification()

    if request.method == 'POST':
        form = Email_Notification(request.POST, request.FILES)
        if form.is_valid():
            subject = form.cleaned_data.get('subject')
            header = form.cleaned_data.get('header')
            content = form.cleaned_data.get('content')

            user_details = User.objects.all()
            for i in user_details:

                #  sending email to the customer alerting him of the succesful transfer 
                subject = f'{subject}'
                html_message = render_to_string(
                    'marketers/marketer_email.html',
                    {
                    'header':header,
                    'content':content,
                    } 
                )
                plain_message = strip_tags(html_message)
                from_email = f"{settings.EMAIL_HOST_USER}" 
                to = i.email
                mail.send_mail(subject, plain_message, from_email, [to], html_message = html_message)

    context = {
        'form': form,

        }

    return render(request, 'marketers/general_email.html', context)
    

@login_required()
@allowed_user(allowed_roles = ['Marketers'])
def general_email_notification_per_country (request):
    """
    send personal email
    """

    form = Email_Notification_Per_Country()

    if request.method == 'POST':
        form = Email_Notification_Per_Country(request.POST, request.FILES)
        if form.is_valid():
            country = form.cleaned_data['country']
            subject = form.cleaned_data.get('subject')
            header = form.cleaned_data.get('header')
            content = form.cleaned_data.get('content')

            for c in country:

                user_details = User.objects.filter( country_of_residence = c.id )
                for i in user_details:

                    #  sending email to the customer alerting him of the succesful transfer 
                    subject = f'{subject}'
                    html_message = render_to_string(
                        'marketers/marketer_email.html',
                        {
                        'header':header,
                        'content':content,
                        } 
                    )
                    plain_message = strip_tags(html_message)
                    from_email = f"{settings.EMAIL_HOST_USER}" 
                    to = i.email
                    mail.send_mail(subject, plain_message, from_email, [to], html_message = html_message)

    context = {
        'form': form,

        }

    return render(request, 'marketers/email_per_country.html', context)

@login_required()
@allowed_user(allowed_roles = ['Marketers'])
def send_personal_email (request, user_id):
    """
    send personal email
    """
    user_details = User.objects.get(id = user_id)
    form = Email_Notification()

    if request.method == 'POST':
        form = Email_Notification(request.POST, request.FILES)
        if form.is_valid():
            subject = form.cleaned_data.get('subject')
            header = form.cleaned_data.get('header')
            content = form.cleaned_data.get('content')

            #  sending email to the customer alerting him of the succesful transfer 
            subject = f'{subject}'
            html_message = render_to_string(
                'marketers/marketer_email.html',
                {
                'header':header,
                'content':content,
                } 
            )
            plain_message = strip_tags(html_message)
            from_email = f"{settings.EMAIL_HOST_USER}" 
            to = user_details.email
            mail.send_mail(subject, plain_message, from_email, [to], html_message = html_message)

    context = {
        'form': form,
        'user_details':user_details,
        }

    return render(request, 'marketers/personal_email.html', context)


# =================================================================
# MARKETERS MOBILE PUSH NOTIFICATIONS 
# START HERE


@login_required()
@allowed_user(allowed_roles = ['Marketers'])
def general_push_notifications(request):
    """
    this hold the general push notifications ( mobile notifications )
    """
    form = General_Push_Notification_Mobile()

    if request.method == 'POST':
        form = General_Push_Notification_Mobile(request.POST)
        if form.is_valid():
            title = form.cleaned_data.get('title')
            message = form.cleaned_data.get('message')

            # getting all kroon and kiosk users 
            all_user = User.objects.all()
            
            for i in all_user:
                
                # FCM push-notifications
                serverToken = f'{FCM_SERVER_KEY}'
                deviceToken = f'{i.device_id}'
                headers = {
                        'Content-Type': 'application/json',
                        'Authorization': 'key=' + serverToken,
                    }
                body = {
                        'notification': {
                                        'title': f'{title}',
                                        'body': f'Hey {i.name}, {message} #KroonMan' ,
                                        'sound': 'default',
                                        },
                        'to':deviceToken,
                        'priority': 'high',
                        #   'data': dataPayLoad,
                        }
                response = requests.post("https://fcm.googleapis.com/fcm/send",headers = headers, data=json.dumps(body))


    context = {
        'form':form,
        }

    return render(request, 'marketers/mobile_notification/general.html', context)


@login_required()
@allowed_user(allowed_roles = ['Marketers'])
def push_notification_per_country(request):
    """
    push notification per country section
    """
    form = General_Push_Notification_Mobile_Per_Country()

    if request.method == 'POST':
        form = General_Push_Notification_Mobile_Per_Country(request.POST)
        if form.is_valid():
            country = form.cleaned_data['country']
            title = form.cleaned_data.get('title')
            message = form.cleaned_data.get('message')
            
            for c in country:

                # getting all kroon and kiosk users 
                all_user = User.objects.filter( country_of_residence = c.id)
                print(all_user)
                
                for i in all_user:
                    
                    # FCM push-notifications via mobile
                    serverToken = f'{FCM_SERVER_KEY}'
                    deviceToken = f'{i.device_id}'
                    headers = {
                            'Content-Type': 'application/json',
                            'Authorization': 'key=' + serverToken,
                        }
                    body = {
                            'notification': {
                                            'title': f'{title}',
                                            'body': f'Hey {i.name}, {message} #KroonMan' ,
                                            'sound': 'default',
                                            },
                            'to':deviceToken,
                            'priority': 'high',
                            #   'data': dataPayLoad,
                            }
                    response = requests.post("https://fcm.googleapis.com/fcm/send",headers = headers, data=json.dumps(body))
                    print(response)

    context = {
        'form': form,
    }

    return render(request, 'marketers/mobile_notification/country.html', context)


# =================================================================
# MARKETERS MOBILE PUSH NOTIFICATIONS 
# END HERE

@login_required()
@allowed_user(allowed_roles = ['Marketers'])
def list_of_all_active_users (request):
    """
    this is the section for personal push notifications
    """
    list_of_users = User.objects.all()
    user_count = list_of_users.count()

    # pagination
    paginator = Paginator(list_of_users, 100) # Show 25 contacts per page.
    page_number = request.GET.get('page')
    list_of_users = paginator.get_page(page_number)

    context = {
        'list_of_users':list_of_users,
        'user_count':user_count,
        }

    return render(request, 'marketers/mobile_notification/personal.html', context)


@login_required()
# @allowed_user(allowed_roles = ['Marketers'])
def marketer_statment (request):
    """
    kroon marketers are incharge of the ads and many functionalities
    here is the index page for marketers dashbaord
    """

    # # getting all pending transactions
    # pending_transactions = Payment_Topup.objects.filter( status='pending' )
    # print(pending_transactions)
    # #checking and verifying if the pin is invalid or expired  
    # current_time = datetime.now()
    # # check_otp_duration = utc.localize(check_otp.duration)
    # current_time = utc.localize(current_time)
    # for i in pending_transactions:
    #     if i.pending_duration is not None:
    #         if i.pending_duration < current_time:
    #             # updating the transactional table status to cancelled
    #             update_transaction = Transactions.objects.get ( transactional_id = i.payment_ref)
    #             update_transaction.status = 'cancelled'
    #             update_transaction.save()

    #             # updating the payment transaction status
    #             i.status = 'cancelled'
    #             i.save()
    #         else:
    #             print('pending')
    #     else:
    #         print('not expired')
    return render(request, 'marketers/statement.html')




#=======================================================================
# News feed and ads feed
@login_required()
@allowed_user(allowed_roles = ['Marketers'])
def general_ads (request):
    form = general_ad_form()

    if request.method == 'POST':
        form = general_ad_form(request.POST, request.FILES)
        if form.is_valid():
            form.save()
             
    context = {
        'form': form,
    }

    return render(request, 'marketers/ads_n_newsfeed/ads_per_country.html', context )


@login_required()
@allowed_user(allowed_roles = ['Marketers'])
def general_news_feed_views (request):
    form = general_news_feed()

    if request.method == 'POST':
        form = general_ad_form(request.POST, request.FILES)
        if form.is_valid():
            form.save()
             
    context = {
        'form': form,
    }

    return render(request, 'marketers/ads_n_newsfeed/ads_per_country.html', context )


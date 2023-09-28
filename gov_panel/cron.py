 # Onboarding
import random
import string
import csv
import threading

import csv, urllib.request
import requests
from contextlib import closing
import codecs

from django.core import mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.http import JsonResponse
from django.core.mail import send_mail
from django.core.files.storage import default_storage as storage
from django.conf import settings 
from django.utils import timezone
import requests


from helpers.common.push_notification import mobile_push_notification


from datetime import timedelta, datetime
from kroon.users.models import User
from gov_panel.models import Onboarding_Users_CSV
from locations.models import Country , Country_Province
from .models import Onboarding_Users_CSV
from notifications.models import NewsFeed


def password_geenrate():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))


def ref_code():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=9))




def merchant_onboarding_process():
    """
    This is process is initiated to register users using the cvs file,
    been uplaoded by the merchant onboarding system.
    """

    users_csv_file = Onboarding_Users_CSV.objects.select_related('on_boarding_user').filter( on_boarding_complete = False ).order_by('-created_date')[0:1]

    for i in users_csv_file: 
        file_name = i.on_boarding_user_file.name 
        onboarding_user = i.on_boarding_user
        url = f'https://test-server-space.nyc3.digitaloceanspaces.com/kroon-kiosk-test-static/{file_name}'
        
        with closing(requests.get(url, stream=True)) as r:
            f = csv.reader(codecs.iterdecode(r.iter_lines(), 'utf-8'))
            try:
                for id,first_name,last_name,email,business_name,province, *__ in f:
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
                            generated_password = password,
                            )
                        user.set_password(password)
                        # data.append(user)
                        user.save()
                # User.objects.bulk_create(data)
                # updating the onboarding status to True
                i.on_boarding_complete = True
                i.on_boarding_complete_date = timezone.now()
                i.save()
                # max onboarding process ends here 
                return JsonResponse('users registration is handled', safe=False)
            
            except:
                # this exception is taken action if the file is not the initial format
                # users_csv_file.delete()
                return JsonResponse('users transfer not handled', safe=False)
 
    return JsonResponse('error' , safe=False)


    # for i in users_csv_file:
    #     file_name = i.on_boarding_user_file.name
        
    #     url_link  = "https://test-server-space.nyc3.digitaloceanspaces.com/kroon-kiosk-test-static/onboarding_users/file_7.csv"
    #     headers = {
    #         # "Authorization": f"Bearer {self.PAYSTACK_SECRET_KEY}",
    #         'Content-Type': 'text/csv',
    #         }

            
    #     response = requests.get(url_link, headers=headers)
    #     onboarding_user = i.on_boarding_user
    #     # reading and extracting details from the file
    #     new_file = response.text 
    #         # print(new_file)
    #     with open(new_file, 'r') as f:
    #         csvf = csv.reader(f)
    #         # data = []
    #         # print(csvf)
    
    #         try:
    #             for id,first_name,last_name,email,business_name,province, *__ in csvf:
    #                 # generating unique password 
    #                 password = password_geenrate()
    #                 # print(password)
    #                 # getting each province ID 
    #                 user_province = Country_Province.objects.get( id = province )
                    
    #                 checking_user = User.objects.filter(email=email)
    #                 if checking_user:
    #                     pass
    #                 else:
    #                     wallet_id = ref_code()

    #                     user = User(
    #                         email=email,
    #                         first_name=first_name, 
    #                         last_name=last_name,
    #                         name = first_name + ' ' + last_name,
    #                         merchant_business_name=business_name,
    #                         account_type = "merchant",
    #                         wallet_id = wallet_id,
    #                         country_of_residence = onboarding_user.country_of_residence,
    #                         country_province = user_province,
    #                         default_currency_id = onboarding_user.default_currency_id,
    #                         on_boarding_user = onboarding_user,
    #                         on_boarding_complete = True,
    #                         accept_terms = True,
    #                         agreed_to_data_usage = True,
    #                         generated_password = password,
    #                         )
    #                     user.set_password(password)
    #                     # data.append(user)
    #                     user.save()
    #             # User.objects.bulk_create(data)
    #             # updating the onboarding status to True
    #             i.on_boarding_complete = True
    #             i.on_boarding_complete_date = timezone.now()
    #             i.save()
    #             # max onboarding process ends here 
    #             return JsonResponse ('users registration is handled', safe = False)
    #         except:
    #             # this exception is taken action if the file is not the initial format
    #             users_csv_file.delete()
    #         return JsonResponse ('users transfer not handled', safe = False)
  



def send_account_details():
    """
    email notification will be sent to the onboarded merchants
    which the email contains the necessary information for registration and 
    completing the onboarding process.
    """
    # Getting the users that has been onboarded
    # but havent been sent their login details
    all_users = User.objects.select_related('country_of_residence', 'country_province', 'on_boarding_user', 'bank_details').filter(email_details = False , on_boarding_complete = True )[:2]
    
    for merchant in all_users:
        email = merchant.email
        name = merchant.name
        default_password = merchant.generated_password
        # update the account detail action
        update_action = User.objects.get(email = email )
        update_action.email_details = True
        update_action.save()

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
    return JsonResponse ('users registration', safe = False)



def publishing_newfeed():
    """
    this publishing function is called after some mins 
    """ 
    # current datetime 
    current_datetime = timezone.now()
    # getting all news feed that the current time is greater than
    # the publishing time ........
    qs = NewsFeed.objects.filter( status = False , gov_post = True )
    for q in qs:
        if q.publishing_time < current_datetime:
            # send a push notification to the merchants
            merchant_qs = User.objects.select_related( 'country_of_residence', 'country_province', 'on_boarding_user', 'bank_details', ).filter( on_boarding_complete = True )
            for merchants in merchant_qs:
                # pushing mobile notifications 
                platform = "kiosk" # the options are.... kroon or kiosk...
                device_id = f'{merchants.device_id}'
                title = f"{q.title}"
                body = f"{q.content}"
                device_type = f"{merchants.device_type}"
                mobile_push_notification(device_id = device_id, title = title, body = body , platform = platform , device_type = device_type )

                # updating newsfeed status
                q.status = True
                q.save()

        else:
            return JsonResponse ('no news feed', safe = False)
        

def push_newsfeed():
    pass

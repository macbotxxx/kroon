from decimal import Decimal
import random
import string

from datetime import datetime, timedelta
from django.http import JsonResponse
from rest_framework import  status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.generics import ListAPIView, CreateAPIView, ListCreateAPIView
from faker import Faker
from kroon.users.models import User, UserAddress , BusinessProfile
from locations.models import Country , Country_Province
from kiosk_categories.models import Category
from simulation.products.products import Products_List

from .models import Simulate_Account


fake = Faker()

def ref_code():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=9))

def wallet_id_generator():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=2))

def random_string_generator(size=8,chars=string.ascii_lowercase + string.digits):
      return ''.join(random.choice(chars) for _ in range(size))

def random_date():
    start_date = datetime(2020, 1, 1)
    end_date = datetime(2022, 12, 31)

    random_days = random.randint(0, (end_date - start_date).days)
    return start_date + timedelta(days=random_days)


def present_random_date():
    start_date = datetime(2023, 4, 22)
    end_date = datetime(2023, 5, 4)

    random_days = random.randint(0, (end_date - start_date).days)
    return start_date + timedelta(days=random_days)




def simulate_Account_Cron ():
    country_iso2 = Simulate_Account.objects.filter( submitted = True , processing_status = False, completed = False )
    for i in country_iso2:
        country_iso = i.country_iso2
        account_limit = i.number_of_merchants
        user_id = User.objects.get( id = i.user_id )
        
        wallet_id = ref_code()
        products = Products_List()
        
        
        for r in range(account_limit):
            country_of_resisdence = Country.objects.get( iso2 = country_iso )
            country_province = random.choice( Country_Province.objects.filter( country = country_of_resisdence ))

            business_category = random.choice(Category.objects.all())
            wallet_id = ref_code()
            wallet_id_new = wallet_id_generator()
            random_days = random_date()            
            first_name=fake.first_name()
            last_name=fake.last_name()
            fake_email = fake.ascii_email()
            ranstr = random_string_generator()

            # checking if the wallet id address exists
            if User.objects.filter( wallet_id = wallet_id ).exists():
                wallet_id = f"{wallet_id_new}{wallet_id}"
            else:
                wallet_id = wallet_id

            # checking if the email address exists
            if User.objects.filter( email = fake_email ).exists():
                email = f"{ranstr}{fake_email}"
            else:
                email=fake_email
                
            address=fake.address()
            company=fake.company()
            gender_list = ['male', 'female']
            gender = random.choice(gender_list)
            phone_number = random.randint(103412, 913413821)
            if User.objects.filter( contact_number = phone_number ).exists():
                phone_number = f"{ranstr}{phone_number}"
            else:
                phone_number=phone_number
            

            user = User(
                email=email,
                first_name=first_name, 
                last_name=last_name,
                name = first_name + ' ' + last_name,
                merchant_business_name=company,
                account_type = "merchant",
                country_of_residence = country_of_resisdence,
                country_province = country_province,
                default_currency_id=country_of_resisdence.currency,
                wallet_id = wallet_id,
                on_boarding_complete = True,
                accept_terms = True,
                gender = gender,
                contact_number = phone_number,
                agreed_to_data_usage = True,
                simulate_account=True,
                created_date = random_days,
                on_boarding_complete_date = random_days,
                on_boarding_user = user_id,

                )
            user.set_password("M080341i")
            user.save()

            types = [
                'Retail Store',
                'Electronics',
            ]

            business_types = random.choice(types)
            b_profile = BusinessProfile(
                user = user,  
                business_name = company, 
                business_contact_number = phone_number, 
                business_address = address, 
                business_type = business_types, 
                active = True, 
                created_date = random_days,
                )
            # businesp.append(b_profile)
            b_profile.save()
            b_profile.business_category.add(business_category)

            i.action_count += 1
            i.save()

        
        # BusinessProfile.objects.bulk_create(businesp)
        # User.objects.bulk_create(data)

        return JsonResponse ('this action has completed successfully ', safe =False)
    
    return JsonResponse ('this action has completed successfully ', safe =False)





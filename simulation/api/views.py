import csv
from decimal import Decimal
import random
import string
# import pandas as pd
import csv, urllib.request
import requests
from contextlib import closing
import codecs


from datetime import datetime, timedelta
from django.utils import timezone

from django.http import HttpResponse
import requests
from rest_framework import  status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, CreateAPIView, ListCreateAPIView
from faker import Faker
from kroon.users.models import User, UserAddress , BusinessProfile
from locations.models import Country , Country_Province
from kiosk_categories.models import Category
from kiosk_stores.models import Merchant_Product
from .serializers import Simulate_Account_Serializer, Simulate_Product_Serializer
from kiosk_cart.models import  Cart, CartItem, Order, Payment, OrderProduct
from simulation.products.products import Products_List
from gov_panel.models import Onboarding_Users_CSV, Action_logs
from django.core.files.storage import default_storage as storage 
from promotional_codes.models import Discount_Code , Government_Promo_Code
from subscriptions.models import Subscription_Plan
from drf_yasg.utils import swagger_auto_schema


fake = Faker()

def ref_code():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=9))

def wallet_id_generator():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=2))

def random_string_generator(size=8,chars=string.ascii_lowercase + string.digits):
      return ''.join(random.choice(chars) for _ in range(size))

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

def password_geenrate():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))


# Function to generate random date between 2020 and 2022
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


class Simulate_Account_View ( CreateAPIView ):
    permission_classes = [AllowAny,]
    serializer_class = Simulate_Account_Serializer

    def create (self , request, *args, **kwargs):
        serializer = self.serializer_class( data = request.data )
        if serializer.is_valid():
            country_iso = serializer.validated_data.get('country_of_residence')
            account_limit = serializer.validated_data.get('account_limit')
            print(country_iso['iso2'])
            
            wallet_id = ref_code()
            data = []
            businesp = []

            products = Products_List()

            for i in range(account_limit):
                country_of_resisdence = Country.objects.get( iso2 = country_iso['iso2'] )
                country_province = random.choice( Country_Province.objects.filter( country = country_of_resisdence ))


                business_category = random.choice(Category.objects.all())
                wallet_id = ref_code()
                wallet_id_new = wallet_id_generator()
                random_days = random_date()

                
                name = fake.user_name()
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
                phone_number = random.randint(103416, 913413821)
               


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
                    on_boarding_user = request.user,

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


            # BusinessProfile.objects.bulk_create(businesp)
            # User.objects.bulk_create(data)

            return Response({'status': 'success'})
        
        return Response(serializer.errors)




class Simulate_Products ( CreateAPIView ):
    permission_classes = [AllowAny,]
    serializer_class = Simulate_Product_Serializer

    def create (self , request, *args, **kwargs):
        serializer = self.serializer_class( data = request.data )
        if serializer.is_valid():
            country_iso = serializer.validated_data.get('country_of_residence')
            country_of_resisdence = Country.objects.get( iso2 = country_iso['iso2'] )

            simulated_accounts = User.objects.filter(country_of_residence = country_of_resisdence , simulate_account = True )
        
            m_products = []
            for i in range(10):
                
                for s in simulated_accounts:
                    
                    random_days = random_date()
                    random_count = random.randint(1, 27)
                    product_cost_price = random.randint(4500, 6000)
                    product_price = random.randint(6500, 8000)
                    products_lists = Products_List()
                    products = products_lists.electronics[random_count]

                    user_profile = User.objects.get(id = s.id )
                    business_profile = BusinessProfile.objects.get(user = user_profile )
                    b_category = Category.objects.get( id = 1 )

                    products = Merchant_Product(
                    user = user_profile, 
                    business_profile = business_profile , 
                    product_sku = f"sku-{product_price}" , 
                    product_name = products ,
                    category = b_category, 
                    price = product_price, 
                    cost_price = product_cost_price, 
                    merchant_local_currency = country_of_resisdence.currency, 
                    stock = random_count, 
                    out_of_stock_notify = 1, 
                    is_available = True,
                    created_date = random_days,
                    )

                    m_products.append(products)

            Merchant_Product.objects.bulk_create(m_products)

            return Response({'status': 'success'})
        
        return Response(serializer.errors)



class Simulate_Sales(CreateAPIView):
    permission_classes = [AllowAny,]
    serializer_class = Simulate_Product_Serializer

    def create (self , request, *args, **kwargs):
        serializer = self.serializer_class( data = request.data )
        if serializer.is_valid():
            country_iso = serializer.validated_data.get('country_of_residence')
            country_of_resisdence = Country.objects.get( iso2 = country_iso['iso2'] )
            period = kwargs.get('period')

            simulated_accounts = User.objects.filter(country_of_residence = country_of_resisdence , simulate_account = True )

            m_products = []
            for i in range(5):
                
                for s in simulated_accounts:
                    
                    if period == "present_random_date":
                        random_days = present_random_date()
                    else:
                        random_days = random_date()
                    print(random_days)

                    random_count = random.randint(1, 7)
                    product_cost_price = random.randint(4500, 6000)
                    product_price = random.randint(6500, 8000)
                    products_lists = Products_List()
                    products = products_lists.electronics[random_count]

                    user_profile = User.objects.get(id = s.id )
                    business_profile = BusinessProfile.objects.get(user = user_profile )

                    # capturing the company account
                    company_profile =  business_profile
                    worker = user_profile
                    # end company profile
                    pay_methods = ['cash_payment', 'bank_payment', 'mobile_money_payment','local_bank_transfer']
                    payment_method = random.choice(pay_methods)

                    manual_sales_options = ['True', 'False',]
                    is_manual_sale = random.choice(manual_sales_options)


                    payment_method = payment_method
                    amount_paid = product_price
                    cash_collected = product_price
                    customers_change = 0
                    manual_sale_amount = product_cost_price
                    is_manual_sale = is_manual_sale
                    offline_products = Merchant_Product.objects.filter(user =user_profile )[:random_count]
                    created_date = random_days

                    # handling the checkout section 
                    data = Order()
                    data.user = worker
                    data.order_total = amount_paid
                    data.order_number = order_number()
                    data.is_ordered = True
                    data.worker = worker
                    data.created_date = created_date
                    data.save()

                    current_order = Order.objects.get(order_number = data.order_number, user = worker , worker = worker)

                    # creating payment
                    ref = f"KIOSK_S_SALE{transaction_ref()}"
                    payment_ref = ref 
                    payment = Payment.objects.create( user = worker, payment_ref = payment_ref, amount_paid = amount_paid, payment_method = payment_method , verified = True, status = "successful", cash_collected = cash_collected , customers_change = customers_change , created_date = created_date )
                    current_order.payment = payment
                    current_order.save()

                    if is_manual_sale:
                        manual_sale = Merchant_Product.objects.get( product_name  = "Manual Sale" )
                        orderproduct = OrderProduct()
                        orderproduct.order_id = data.id
                        orderproduct.payment = payment
                        orderproduct.user = worker
                        orderproduct.product_id = manual_sale.id
                        orderproduct.product_price = manual_sale_amount
                        orderproduct.product_total_price = manual_sale_amount
                        orderproduct.ordered = True
                        orderproduct.worker = worker
                        orderproduct.created_date = created_date
                        orderproduct.save()
                        data.products.add(manual_sale.id)


                    for items in offline_products:
                        
                        item = Merchant_Product.objects.get( id = items.id )
                        
                        orderproduct = OrderProduct()
                        orderproduct.order_id = data.id
                        orderproduct.payment = payment 
                        orderproduct.user = worker
                        orderproduct.product_id = item.id
                        orderproduct.product_price = item.price
                        orderproduct.quantity = item.stock
                        orderproduct.product_total_price = Decimal( item.stock ) * item.price

                        orderproduct.ordered = True
                        orderproduct.worker = worker
                        orderproduct.save()

                        # reduce the stock of the order item
                        try: 
                            product = Merchant_Product.objects.get( id = item.id )
                        except Merchant_Product.DoesNotExist:
                            return Response({'status':'error','message':'product id does not exist'}, status=status.HTTP_201_CREATED)

                        product.stock -= int(item.stock)
                        product.save()
                        data.products.add(item.id)

                return Response({'status': 'success'})
        
        return Response(serializer.errors)


class Delete_Simulate_Accounts (CreateAPIView):
    permission_classes = [AllowAny,]
    serializer_class = Simulate_Product_Serializer

    def create (self , request, *args, **kwargs):
        serializer = self.serializer_class( data = request.data )
        if serializer.is_valid():
            country_iso = serializer.validated_data.get('country_of_residence')
            country_of_resisdence = Country.objects.get( iso2 = country_iso['iso2'] )
            period = kwargs.get('period')

            simulated_accounts = User.objects.filter(country_of_residence = country_of_resisdence , simulate_account = True )

            simulated_accounts.delete()

            return Response({'status': 'success'})
        
        return Response(serializer.errors)
    

class Create_Users_CSv (CreateAPIView):
    permission_classes = [AllowAny,]
    serializer_class = Simulate_Product_Serializer

    def create (self , request, *args, **kwargs):
        
        # response = HttpResponse(content_type='text/csv') 
        
        # reg_num = 30
        # response['Content-Disposition'] = 'attachment; filename="file.csv"'
        # writer = csv.writer(response)  
        # for i in range(reg_num):
        #     first_name=fake.first_name()
        #     last_name=fake.last_name()
        #     fake_email = fake.ascii_email() 
        #     company=fake.company()
        #     province_id = random.randint(1,1)
        #     writer.writerow([f'{province_id}', f'{first_name}', f'{last_name}', f'{first_name}{fake_email}', f'{first_name}{last_name}{province_id}',f'{province_id}'])  
        # return response

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
                    return Response('users registration is handled')
                except:
                    # this exception is taken action if the file is not the initial format
                    # users_csv_file.delete()
                    return Response('users transfer not handled')
        return 'error'
        


class GenerateNasmePromoCode ( ListAPIView ):
    permission_classes = [AllowAny,]
    serializer_class = Simulate_Product_Serializer

    def list( self, request,*args, **kwargs ):
        # for i in range(1, 1096):
        #     formatted_number = f"{i:05}"
        #     if formatted_number <= '01096':
        #         Discount_Code.objects.create(discount_code = f"NL/{formatted_number}")
        #         plan_code = Subscription_Plan.objects.get(slug_plan_name = "kiosk_pro")

        #         Government_Promo_Code.objects.create(promo_code = f"NL/{formatted_number}", code_plan = plan_code)
        #     else:
        #         break

        

        return Response(f"code generated")

from decimal import Decimal
import requests
import json
from django.conf import settings
from django.core.mail import send_mail
from rest_framework.generics import CreateAPIView, get_object_or_404

from kroon.users.models import User 
from kroon_kyc.models import KycApplication , MarchantKycApplication
from kroon_token.models import PurchaseTokenFees
from .currency_converter import currency_converter
from virtual_cards.models import Virtual_Cards_Details , All_Cards_Transactions
from payments.models import Payment_Topup
from transactions.models import Transactions


if settings.TEST_PAYMENT:
    FLUTTERWAVE_SECRET_KEY = settings.FLUTTERWAVE_SECRET_KEY_TEST
else:
    FLUTTERWAVE_SECRET_KEY = settings.FLUTTERWAVE_SECRET_KEY


# CREATE VIRTUAL CARD 
# ================================================================

class Virtual_Card:

    """
    this hold the full functionalities of the virtual card interface
    including the creating , funding , blocking and terminating virtual cards
    """

    def create_virtual_card ( request, prefund_amount , currency , user_id ):
        """
        Create a virtual card using the users information
        """

        url = "https://api.flutterwave.com/v3/virtual-cards/"
        callback_url = "https://kroonapp.xyz/webhook/push-webhook/"

        # getting user info from kyc 
        # user_details = KycApplication.objects.get( user_id = user_id )
        # checking the kyc according to the user account type
        user_info = User.objects.get(id=user_id)

        if user_info.account_type == "merchant":
            user_details = MarchantKycApplication.objects.get( user_id = user_id )
        elif user_info.account_type == "personal":
            user_details = KycApplication.objects.get( user_id = user_id )

        billing_name = f"{user_details.legal_first_names} {user_details.legal_last_names}"
        billing_address = f"{user_details.street_or_flat_number} , { user_details.street_name} "
        billing_city = f"{user_details.city}"
        billing_state = f"{user_details.state}"
        billing_postal_code = f"{user_details.zip_code}"
        billing_country = f"{user_details.kyc_country.iso2}"
        billing_state = f"{user_details.state}"
        first_name = f"{user_details.legal_first_names}"
        last_name = f"{user_details.legal_last_names}"
        date_of_birthx = f"{user_details.birth_date}"
        date_of_birth = date_of_birthx.replace('-', '/')
        email = f"{user_details.email}"
        phone = f"{user_details.user.contact_number}"
        if user_details.user.gender == 'male':
            title = "Mr"
            gender ="M"
        else:
            title = "Mrs"
            gender ="F"
            
        payload = json.dumps({
        "currency": f"{currency}",
        "amount": f"{prefund_amount}",
        "debit_currency": "NGN",
        "billing_name": billing_name,
        "billing_address": billing_address,
        "billing_city": billing_city,
        "billing_state": billing_state,
        "billing_postal_code": billing_postal_code,
        "billing_country": billing_country,
        "first_name": first_name,
        "last_name": last_name,
        "date_of_birth": date_of_birth,
        "email": email,
        "phone": phone,
        "title": title,
        "gender": gender,
        "callback_url": callback_url
        })
     

        headers = {
        'Authorization': f"Bearer {FLUTTERWAVE_SECRET_KEY}",
        'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload).json()
        return response


    # CREATE VIRTUAL CARD ENDS HERE
    # ================================================================


    def fund_virtual_card ( request, fund_amount , user_id , card_id ):
        url = f"https://api.flutterwave.com/v3/virtual-cards/{card_id}/fund"

        payload = json.dumps({
        "debit_currency": "NGN",
        "amount": fund_amount
        })
        headers = {
        'Authorization': f"Bearer {FLUTTERWAVE_SECRET_KEY}",
        'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload).json()
        return response



    def block_unblock_virtual_card (request, card_id , status_action  ):
        url = f"https://api.flutterwave.com/v3/virtual-cards/{card_id}/status/{status_action}"

        payload={}
        headers = {
        'Authorization': f"Bearer {FLUTTERWAVE_SECRET_KEY}",
        }

        response = requests.request("PUT", url, headers=headers, data=payload).json()
        print(response)
        return response
        
        
    def terminate_virtual_card ( request , card_id  ):
        url = f"https://api.flutterwave.com/v3/virtual-cards/{card_id}/terminate"

        payload={}
        headers = {
        'Authorization': f"Bearer {FLUTTERWAVE_SECRET_KEY}",
        }

        response = requests.request("PUT", url, headers=headers, data=payload).json()
        print(response)
        return response




# CREATE USER INFORMATION FOR VIRTUAL CARD 
# ================================================================

def store_users_virtual_card_details( create_card , user_id , card_design ):
    """
    this strores the user information used in creating the virtual card
    """
    xamount= f"{create_card['amount']}"
    amount = xamount.replace(',', '')
    user = User.objects.get( id = user_id )
    user_virtual_card_details = Virtual_Cards_Details()
    user_virtual_card_details.user = user
    user_virtual_card_details.card_id = create_card['id']
    user_virtual_card_details.card_design = card_design
    user_virtual_card_details.account_id = create_card['account_id']
    user_virtual_card_details.amount = Decimal(amount)
    user_virtual_card_details.currency = create_card['currency']
    user_virtual_card_details.card_hash = create_card['id']
    user_virtual_card_details.card_pan = create_card['card_pan']
    user_virtual_card_details.masked_pan = create_card['masked_pan']
    user_virtual_card_details.city = create_card['city']
    user_virtual_card_details.state = create_card['state']
    user_virtual_card_details.postal_code = create_card['zip_code']
    user_virtual_card_details.cvv = create_card['cvv']
    user_virtual_card_details.expiration = create_card['expiration']
    user_virtual_card_details.send_to = create_card['send_to']
    user_virtual_card_details.bin_check_name = create_card['bin_check_name']
    user_virtual_card_details.card_type = create_card['card_type']
    user_virtual_card_details.name_on_card = create_card['name_on_card']
    user_virtual_card_details.created_date = create_card['created_at']
    user_virtual_card_details.is_active = create_card['is_active']
    user_virtual_card_details.save()

    # adding card to user profile 
    user_info = User.objects.get(id=user_id)
    user_info.virtual_cards.add(user_virtual_card_details)

    # store the records 
    All_Cards_Transactions.objects.create( 
    user = user,
    # transactional_id = transactional_id,
    card_id = create_card['id'],
    gateway_reference = "VIRTUAL CARD INITIALIZED",
    balance = Decimal(amount) ,
    currency = create_card['currency'],
    # debited_amount = debited_amount,
    credited_amount = Decimal(amount),
    payment_type = create_card['card_type'],
    narration = "VIRTUAL CARD CREATED SUCCESSFUL",
    transactional_date = create_card['created_at'],
    action = create_card['is_active'],
    status = "successful"
    )


def fund_card_amount (  card_id , fund_amount , user_id , payment_method ):
    try:
        card = Virtual_Cards_Details.objects.get( user_id = user_id , card_id = card_id )
        balance = card.amount
        card.amount += Decimal(fund_amount)
        card.save()

         # store the records 
        All_Cards_Transactions.objects.create( 
        user = card.user,
        # transactional_id = transactional_id,
        card_id = card_id,
        gateway_reference = "VIRTUAL CARD FUNDED",
        balance = Decimal(balance) ,
        currency = card.currency,
        # debited_amount = debited_amount,
        credited_amount = Decimal(fund_amount),
        payment_type = payment_method,
        narration = "VIRTUAL CARD FUNDED SUCCESSFUL",
        transactional_date = card.created_date,
        action = True,
        status = "successful"
        )

    except Virtual_Cards_Details.DoesNotExist:
        pass


def status_action_virtual_card ( card_id, status_action ):
    try:
        card = Virtual_Cards_Details.objects.get( card_id = card_id , is_active = True )
        if status_action == 'block':
            card.block = True
        elif status_action == 'unblock':
            card.block = False
        elif status_action == 'terminate':
            card.block = True
            card.is_active = False

        card.save()
    except Virtual_Cards_Details.DoesNotExist:
        response = {'status':'error', 'message':'Card has been block or terminated', 'data':''}
        return response

   
    
# CREATE USER INFORMATION FOR VIRTUAL CARD  ENDS HERE
# ================================================================



# TRANSACTIONS VERIFICATION FOR PREFUND PAYMENT USING CARD
# ================================================================

def verify_card_payment ( payment_ref , currency , user_id , card_id , card_design ):
    """
    this verifies the card transaction using the payment ref , which on successful
    payment the user virtual card will be created.
    """
    # verifying payment reference
    try:
        payment = Payment_Topup.objects.get (payment_ref=payment_ref , settled = False)
    except Payment_Topup.DoesNotExist:
        response = {'status':'error', 'message':'Transactional reference is not found or its has been settled', 'data':''}
        return response


    verified = payment.verify_payment_flutterwave()
    if verified['verified']:
        amount = verified['amount']
        currency = verified['currency']
        payment.settled = True
        payment.save()

        if card_id is None:
            # applying for virtual card 
            prefund_amount = amount
            card_process = Virtual_Card()
            create_card = card_process.create_virtual_card( prefund_amount , currency , user_id)
            if create_card['status'] == "error":
                pass
            else:
                # storing users virtual cards details
                card_details = create_card['data']
                store_users_virtual_card_details( card_details , user_id , card_design )
                # storing card records 

            return create_card
        
        else:
            # funding the virtual card
            fund_amount = f"{amount}"
            payment_method = "Card Payment"
            card_process = Virtual_Card()
            fund_card = card_process.fund_virtual_card( fund_amount , user_id , card_id )
            if fund_card['status'] == "error":
                pass
            elif fund_card['status'] == "success":
                # storing users virtual cards details
                fund_card_amount( card_id , fund_amount , user_id , payment_method)

            return fund_card
            
    else:
        response = {'status':'error', 'message':'payment not found', 'data':''}
        return response


# TRANSACTIONS VERIFICATION FOR PREFUND PAYMENT USING CARD ENDS HERE
# ================================================================




# VIRTUAL CARD CREATION USING KROON BALANCE
# ================================================================


def kroon_method_virtual_card( request , currency , card_design):
    """
    to create a virtual card using kroon balance
    """
    user_kroon_balance = User.objects.get ( id=request.user.id )
    kroon_amount = user_kroon_balance.kroon_token
    user_currency = user_kroon_balance.default_currency_id
    # getting the country code and fee
    country_virtual_card_fee = PurchaseTokenFees.objects.get( country = user_kroon_balance.country_of_residence )
    converter =  currency_converter(currency = user_currency)

    if currency == 'USD':
        prefund_amount = 3 #this is charge amount in USD
        #converting the kroon to tranding currency
        card_fee = format(Decimal(converter) * country_virtual_card_fee.virtual_card_fees, '.0f')
        # prefund amount is to be fund to the virtual card by defualt is 3USD
        calculated_prefund_fee = format(converter * 3 , '.0f' )
        kroon_fee = Decimal(calculated_prefund_fee) + Decimal(card_fee)

    elif currency == 'NGN':
        #this is charge amount in local currency NGN
        prefund_amount = 1000
        #converting the kroon to tranding currency
        card_fee = format(Decimal(converter) * country_virtual_card_fee.virtual_card_fees, '.0f')
        kroon_fee = Decimal(prefund_amount) + Decimal(card_fee)

    else:
        pass


    # chekcinig if virtual card charge is available
    if  kroon_amount >= kroon_fee:
        total_kroon = kroon_amount - kroon_fee
        user_kroon_balance.kroon_token = total_kroon
        
        # applying for virtual card
        user_id = user_kroon_balance.id
        card_process = Virtual_Card()
        create_card = card_process.create_virtual_card( prefund_amount , currency , user_id)
        if create_card['status'] == "error":
            pass
        else:
            user_kroon_balance.save()
            # storing users virtual cards details
            card_details = create_card['data']
            store_users_virtual_card_details( card_details , user_id , card_design)
            # storing card record

        return create_card

    else:
        response = {'status':'error', 'message':'insufficent balance , virtual card not created successfully', 'data':''}
        return response



# VIRTUAL CARD CREATION USING KROON BALANCE ENDS HERE 
# ================================================================




# TO FUND A VIRTUAL CARD USING KROON BALANCE
# ================================================================

def kroon_fund_virtual_card ( amount , user_id , card_id):
    """
    to fund a virtual card using kroon balance, this will be triggered 
    when ever a user wants to create a virtual card using his/her kroon balance.
    """
    user_kroon_balance = User.objects.get ( id = user_id)
    kroon_amount = user_kroon_balance.kroon_token

    # chekcinig if virtual card charge is available
    if  kroon_amount >= amount:
        total_kroon = kroon_amount - amount
        user_kroon_balance.kroon_token = total_kroon
        
        # funding virtual card from kroon balance
        fund_amount = f"{amount}"
        payment_method = "Kroon Payment"
        user_id = user_kroon_balance.id
        card_process = Virtual_Card()
        fund_card = card_process.fund_virtual_card( fund_amount , user_id , card_id  )
        if fund_card['status'] == "error":
            pass
        elif fund_card['status'] == "success":
            user_kroon_balance.save()
            # storing users virtual cards details
            fund_card_amount( card_id , fund_amount , user_id , payment_method )
        
        return fund_card

    else:
        response = {'status':'error', 'message':'insufficent balance , virtual card not created successfully', 'data':''}
        return response


# TO FUND A VIRTUAL CARD USING KROON BALANCE ENDS HERE
# ================================================================
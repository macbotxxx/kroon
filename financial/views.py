from decimal import Decimal
from django.shortcuts import render
from django.db.models import Q
from django.core.paginator import Paginator
import requests


from kroon.users.models import User
from transactions.models import Transactions
from kroon_token.models import PurchaseTokenFees , WithDrawTokenFees
from kroon_withdrawal.models import Kroon_Withdrawal_Record
from django.conf import settings

# Create your views here.
from locations.models import Country


CURRENCY_CONVERT_API_KEY = settings.CURRENCY_CONVERT_API_KEY

def home_page( request ):
    all_countries = Country.objects.all()

    context = {
        'all_countries':all_countries,
    }
    return render(request, 'financial/index.html', context )



# getting each country financial analytics
def financial_analytics (request , country, *args, **kwargs):
    # topup
    total_topup = 0
    flutterwave_total_fees = 0
    application_fees = 0
    # withdraws
    total_withdraws = 0
    total_cashout_fee = 0
    total_cashout_vat_fee = 0

    # Getting all users according to te country selected
    # getting all topups 
    all_users = Transactions.objects.filter( user__country_of_residence  = country , action = 'KROON WALLET TOPUP' , status = 'successful')

    # getting all withdraws 
    all_withdraws = Transactions.objects.filter( user__country_of_residence  = country , action = 'LOCAL BANK WITHDRAWAL' , status = 'successful')
   
    all_transactions = Transactions.objects.filter( Q(action = 'KROON WALLET TOPUP') | Q(action = 'LOCAL BANK WITHDRAWAL') | Q(action = 'MOBILE MONEY WITHDRAWAL') , user__country_of_residence  = country , )

    # pagination
    paginator = Paginator(all_transactions, 15) # Show 25 contacts per page.
    page_number = request.GET.get('page')
    all_transactions = paginator.get_page(page_number)

    all_countries = Country.objects.all()
    country_id = Country.objects.get( id = country )
    
    for i in all_users:
        # calcualting for flutterwave app charges 
        i.amount_in_localcurrency -= i.amount_settled
        flutterwave_total_fees += i.amount_in_localcurrency
        total_topup += i.amount


    app_fees = PurchaseTokenFees.objects.get( country = country )

    # calculating to get the app fees which is 10% by defualt
    flutterwave_fees = flutterwave_total_fees
    topup_app_fee_percentage = app_fees.application_fee
    percentage = (topup_app_fee_percentage * total_topup) / 100
    application_fees = format(percentage, '.2f')
    
    # calculating the vat cost for this country
    vat_fees_percentage = app_fees.vat_fee
    vat_fees = (vat_fees_percentage * percentage) / 100
    total_vat_fee = format(vat_fees, '.2f')

    # all transaction count
    all_transactions_count = all_users.count()


    """
    working on the all withdraw transactions which consist of
    both the vat and application fee from both platform 
    kroon and kiosk
    """
    # getting the all fees on withdrawal
    withdraw_fees = WithDrawTokenFees.objects.get( country = country , operator = "bank withdrawal" )
    try:
        mobile_money_withdrawal = WithDrawTokenFees.objects.get( country = country , operator = "mobile money cashout" )
    except WithDrawTokenFees.DoesNotExist:
        pass
    
    # all withdraw transactions count
    all_withdraws_count = all_withdraws.count()
    # total cash fees 
    total_cashout_fee = all_withdraws_count * withdraw_fees.withdrawal_limit
    for w in all_withdraws:
        total_withdraws += w.amount_in_localcurrency

    # getting the cashout vat amount 
    cashout_vat = ( total_withdraws * withdraw_fees.vat_fee ) / 100
    total_cashout_vat_fee = format(cashout_vat, '.2f')

    currency = country_id.currency
    # converting local currency to USD
    reqUrl = f"https://api.getgeoapi.com/v2/currency/convert?api_key={CURRENCY_CONVERT_API_KEY}&format=json&from={currency}&to=USD&amount={total_topup}"

    headersList = {
        "Accept": "*/*",
        "User-Agent": "Thunder Client (https://www.thunderclient.com)" 
    }

    payload = ""

    response = requests.request("GET", reqUrl, data=payload,  headers=headersList)

    response_data = response.json()
    
    # converted balance to USD decimal
    usd_balance = Decimal( response_data['rates']['USD']['rate_for_amount'] )
    print(response_data['rates']['USD']['rate_for_amount'])
    converted_balance = format(usd_balance, '.2f')



    context = {

        'all_countries':all_countries,
        'flutterwave_fees':flutterwave_fees,
        'country_id':country_id,
        'total_topup':total_topup,
        'application_fees':application_fees,
        'app_fees':app_fees,
        'total_vat_fee':total_vat_fee,
        'all_transactions':all_transactions,
        'all_transactions_count':all_transactions_count,

        # withdrawal rate
        'total_cashout_fee':total_cashout_fee,
        'total_withdraws':total_withdraws,
        'total_cashout_vat_fee':total_cashout_vat_fee,
        'cashout_amount_fee': withdraw_fees.withdrawal_limit,
        'cashout_vat_fee': withdraw_fees.application_fee,

        # converted balance
        'converted_balance':converted_balance,

    }
    return render(request, 'financial/analytics.html', context )


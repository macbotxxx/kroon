import json
import random
import string

from django.contrib import messages
from datetime import timedelta, datetime
from django.utils import timezone
from django.contrib.auth.decorators import login_required
# email settings
from django.core import mail
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.shortcuts import redirect, render

from .models import Subscription_Plan
from .forms import Gov_Promo_codeForm
from kroon.users.models import BusinessProfile, User
from subscriptions.models import Subscription_Plan ,Merchant_Subcribers
from promotional_codes.models import Government_Promo_Code
from kiosk_cart.api.views import _company_account , _company_account_in_app
from helpers.common.paypal import get_access_token , deactivate_subscription_plan



def transaction_ref():
    return ''.join(random.choices(string.digits, k=9))




def transaction_ref_re():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))



def generate_code (request , *args, **kwargs ):
    code_range = 100
    
    plan = Subscription_Plan.objects.get( plan_name = "Kiosk Plus" )
    for i in range( code_range ):
        codes = transaction_ref()
        codes_re = transaction_ref_re()

        try:
            Government_Promo_Code.objects.get( promo_code = codes )
            Government_Promo_Code.objects.create( code_plan = plan , promo_code = codes_re )
        except Government_Promo_Code.DoesNotExist:
            Government_Promo_Code.objects.create( code_plan = plan , promo_code = codes )
        
    return render(request, 'kiosk_merchant_dash/all_plans.html')
    

@login_required()
def all_plans (request):
    plans = Subscription_Plan.objects.all().order_by('created_date')
    user_plan = None
    try:
        user_plan = Merchant_Subcribers.objects.get( user = request.user , active = True )
    except Merchant_Subcribers.DoesNotExist :
        user_plan = None
    user_profile = BusinessProfile.objects.get ( user = request.user , active = True)
    

    context = {
        'plans': plans,
        'user_plan':user_plan,
        'user_profile':user_profile,
    }
    return render(request, 'kiosk_merchant_dash/all_plans.html', context)


@login_required()
def plans_details (request, plan_id , period ):
    
    try:
        # Get the Subscription_Plan with the given ID.
        plan = Subscription_Plan.objects.get( id = plan_id )
        user_profile = BusinessProfile.objects.get ( user = request.user , active = True)
    except Subscription_Plan.DoesNotExist :
        return redirect('all_plans')

    if period == "month":
        plan_period = 'monthly'
        plan_id = plan.monthly_plan_id
    elif period == "yearly":
        plan_period = 'yearly'
        plan_id = plan.yearly_plan_id
    else:
        return redirect('all_plans')

    # Context for creating a plan.
    context = {
        'plan': plan,
        'user_profile':user_profile,
        'plan_period':plan_period,
        'plan_id':plan_id,

    }
    return render(request, 'kiosk_merchant_dash/plan_details.html', context)  




@login_required()
def government_code (request, plan_id):
    form = Gov_Promo_codeForm()
    plan = Subscription_Plan.objects.get( id = plan_id )
    user_profile = BusinessProfile.objects.get ( user = request.user , active = True)

    if request.method == 'POST':
        form = Gov_Promo_codeForm(request.POST)
        company_profile = _company_account(request)

        if form.is_valid():
            promo_code = form.cleaned_data['promotional_code']
            try:
                code = Government_Promo_Code.objects.get ( promo_code = promo_code , used_code = False  )
                plan = code.code_plan
                code_yearly = code.yearly_code

                if code_yearly:
                    days = code.code_plan.yearly_plan_duration
                else:
                    days = code.code_plan.plan_duration

                end_date = timezone.now()+timedelta( days = days )

                 # get the privious plan and deactivates it 
                try:
                    # deactivating the old plan
                    old_plan = Merchant_Subcribers.objects.get( user = request.user , active = True )
                    old_plan.active = False
                    old_plan.end_date = timezone.now()
                    old_plan.save()

                    # activating the new plans
                    if code_yearly:
                        Merchant_Subcribers.objects.create( user = request.user , active = True , plan = plan , end_date = end_date , yearly_plan = True)
                    else:
                        Merchant_Subcribers.objects.create( user = request.user , active = True , plan = plan , end_date = end_date )
                
                except Merchant_Subcribers.DoesNotExist :
                    # activating the new plans
                    Merchant_Subcribers.objects.create( user = request.user , active = True , plan = plan , end_date = end_date )

                # expiring the promo code 
                code.used_code = True
                code.user = request.user
                code.save()
                messages.info(request, f"Subscription plan is been activated for this account successfully.")

                subscriptions = Merchant_Subcribers.objects.get( user = request.user , active = True )

                #  sending email to the customer alerting him of the succesful order 
                subject = f'Successful Payment - {company_profile.merchant_business_name}'
                html_message = render_to_string(
                    'kiosk_emails/payment.html',
                    {
                    # 'user': company_profile,
                    'subscriptions':subscriptions,
                    } 
                )
                plain_message = strip_tags(html_message)
                from_email = 'support@mykroonapp.com'
                to = company_profile
                mail.send_mail(subject, plain_message, from_email, [to], html_message = html_message)
                return redirect('my_subscriptions')


            except Government_Promo_Code.DoesNotExist:
                messages.info(request, f"Promotional code is ether inactive or incorrect , kindly check the code and try again. ")

    context = {
        'plan': plan,
        'form':form,
        'user_profile':user_profile,
    }
    return render(request, 'kiosk_merchant_dash/gov_promo_code.html', context)  




@login_required()
def my_subscriptions (request):
    # Returns a list of all subscriptions for the current user.
    subscriptions = Merchant_Subcribers.objects.filter( user=request.user )[:5]
    user_profile = BusinessProfile.objects.get ( user = request.user , active = True)
    active_sub = None
    try:
        active_sub = Merchant_Subcribers.objects.get( user=request.user , active = True)
    except:
        pass

    # Context for adding a subscriptions user_profile and active_sub.
    context = {
        'subscriptions':subscriptions,
        'user_profile':user_profile,
        'active_sub':active_sub,
    }
    return render(request, 'kiosk_merchant_dash/my_subcriptions.html', context)  




@login_required()
def card_subscription(self, request, *args, **kwargs):
    plan_id = kwargs.get('plan_id')
    
    try:
        plans = Subscription_Plan.objects.get ( id = plan_id )
        days = plans.plan_duration
        end_date = timezone.now()+timedelta( days = days )

            # get the privious plan and deactivates it 
        try:
            # deactivating the old plan
            old_plan = Merchant_Subcribers.objects.get( user = request.user , active = True )
            old_plan.active = False
            old_plan.end_date = timezone.now()
            old_plan.save()

            # activating the new plans
            Merchant_Subcribers.objects.create( user = request.user , active = True , plan = plans , end_date = end_date )
        
        except Merchant_Subcribers.DoesNotExist :
            # activating the new plans
            Merchant_Subcribers.objects.create( user = request.user , active = True , plan = plans , end_date = end_date )

        # expiring the promo code 
        plans.used_code = True
        plans.user = request.user
        plans.save()
        messages.info(request, f"Subscription plan is been activated for this account successfully.")
        return redirect('my_subscriptions')

    except Subscription_Plan.DoesNotExist :
        messages.info(request, f"Promotional code is ether inactive or incorrect , kindly check the code and try again. ")




@login_required()
def PayPal_Payment (request):
    body = json.loads(request.body)
    plan_id = body['plan_id']
    payment_method = body['payment_method']
    period = body['period']
    subscription_id = body['subscription_id']
    company_profile = _company_account(request)
    print(body)
    

    try:
        plans = Subscription_Plan.objects.get ( id = plan_id )

        if period == "monthly":
            days = plans.plan_duration
            sub_plan_id = plans.monthly_plan_id
        elif period == "yearly":
            days = plans.yearly_plan_duration
            sub_plan_id = plans.yearly_plan_id

        else:
            msg = {'status':'error','message':'Promotional code is ether inactive or incorrect , kindly check the code and try again. ' }
            return JsonResponse(status=404,data=msg, safe=False)

        end_date = timezone.now()+timedelta( days = days )
   
            # get the privious plan and deactivates it 
        try:
            # deactivating the old plan
            old_plan = Merchant_Subcribers.objects.get( user = request.user , active = True )
            old_plan.active = False
            old_plan.end_date = timezone.now()
            old_plan.save()

            # deactivating the subscription plan for the current user
            if old_plan.recurring_payment:
                access_token = get_access_token()
                subscription_ids = old_plan.subscription_id
                deactivate_subscription = deactivate_subscription_plan( access_token , subscription_ids )
                print( deactivate_subscription )
            #  deactivate the subscription end here 

            if period == "monthly":
                Merchant_Subcribers.objects.create( user = request.user , active = True , plan = plans , subscription_id = subscription_id , sub_plan_id = sub_plan_id , end_date = end_date )
            elif period == "yearly":
                Merchant_Subcribers.objects.create( user = request.user , active = True , yearly_plan = True , plan = plans , subscription_id = subscription_id , sub_plan_id = sub_plan_id , end_date = end_date )
               
            else:
              
                msg = {'status':'error','message':'Promotional code is ether inactive or incorrect , kindly check the code and try again. ' }
                return JsonResponse(status=404,data=msg, safe=False)
            # activating the new plans
        
        except Merchant_Subcribers.DoesNotExist :
            # activating the new plans
            if period == "monthly":
                Merchant_Subcribers.objects.create( user = request.user , active = True , plan = plans , subscription_id = subscription_id , sub_plan_id = sub_plan_id , end_date = end_date )

            elif period == "yearly":
                Merchant_Subcribers.objects.create( user = request.user , active = True , yearly_plan = True , subscription_id = subscription_id , sub_plan_id = sub_plan_id , plan = plans , end_date = end_date )
        
        messages.info(request, f"Subscription plan is been activated for this account successfully.")
        subscriptions = Merchant_Subcribers.objects.get( user=request.user , active = True )

        #  sending email to the customer alerting him of the succesful order 
        subject = f'Successful Payment - {company_profile.merchant_business_name}'
        html_message = render_to_string(
            'kiosk_emails/payment.html',
            {
            'user': company_profile,
            'subscriptions':subscriptions,
            } 
        )
        plain_message = strip_tags(html_message)
        from_email = 'support@mykroonapp.com'
        to = company_profile
        mail.send_mail(subject, plain_message, from_email, [to], html_message = html_message) 

    except Subscription_Plan.DoesNotExist :
        messages.info(request, f"Promotional code is ether inactive or incorrect , kindly check the code and try again. ")
    



# this is to cancel the active subscription
def cancel_subscription(request):
    active_sub = Merchant_Subcribers.objects.get( user=request.user , active = True)

    # deactivating the subscription plan for the current user
    access_token = get_access_token()
    subscription_ids = active_sub.subscription_id
    deactivate_subscription = deactivate_subscription_plan( access_token , subscription_ids )
    
    #  deactivate the subscription end here 
    if deactivate_subscription == 204:
        # cancelling merchant subscription record
        active_sub.recurring_payment = False
        active_sub.save()
        messages.info(request, f"Subscription plan auto renewal is been deactivated for this active plan successfully.")
    else:
        # updating merchant subscription record
        active_sub.recurring_payment = True
        active_sub.save()
        messages.error(request, f"Sorry ! the is an issue cancelling your subscription at the moment kindly try again")

    return redirect('my_subscriptions')




# list of all in-app subscriptions
def all_app_sub (request , email ):
    
    # checking if the email is valid customer
    try:
        user_email = User.objects.get(email=email)
    except user_email.DoesNotExist:
        return JsonResponse("You are not authorized to make this request", safe=False)

    # saving the email address to a session
    request.session['email'] = email

    plans = Subscription_Plan.objects.all().order_by('created_date')
    # access_token = get_access_token() 
    # print(access_token)   

    context = {
        'plans': plans
    }

    return render(request , 'app_subscription/plans.html', context)




def app_plan_details (request ,  plan_id , period ):
    # in-app subscription plan details page
    if request.session.has_key('email'):
        user_email = request.session['email']
    else:
        return JsonResponse("unauthorized request" , safe = False )

    # Attempt to access a subscription plan
    try:
        plan = Subscription_Plan.objects.get( id = plan_id )
        # Returns true if the request was successful.
        user_profile = BusinessProfile.objects.get ( user__email = user_email , active = True)
    except Subscription_Plan.DoesNotExist :
        # Returns a JsonResponse for unauthorized requests
        return JsonResponse("unauthorized request" , safe = False )


    if period == "month":
        plan_period = 'monthly'
        plan_id = plan.monthly_plan_id
    elif period == "yearly":
        plan_period = 'yearly'
        plan_id = plan.yearly_plan_id
    else:
        return redirect('all_plans')

    # Context for creating a plan.
    context = {
        'plan': plan,
        'user_profile':user_profile,
        'plan_period':plan_period,
        'plan_id':plan_id,

    }

    return render(request , 'app_subscription/plan_details.html', context)




def in_app_government_code ( request, plan_id ):
    """
    this function requires a plan id and to use only on the in app subscription
    """

    # unauthorized request.
    if request.session.has_key('email'):
        user_email = request.session['email']
        account_user = User.objects.get(email=user_email )
    else:
        return JsonResponse("unauthorized request" , safe = False )



    # Creates a form to create a new Promo code for a subscription plan.
    form = Gov_Promo_codeForm()
    plan = Subscription_Plan.objects.get( id = plan_id )
    user_profile = BusinessProfile.objects.get ( user = account_user , active = True)

    # Create a Promo code for a company account in the app.
    if request.method == 'POST':
        form = Gov_Promo_codeForm(request.POST)
        company_profile = _company_account_in_app(request)

        if form.is_valid():
            promo_code = form.cleaned_data['promotional_code']
            try:
                # Returns a Government_Promo_Code for a given promo code
                code = Government_Promo_Code.objects.get ( promo_code = promo_code , used_code = False  )
                plan = code.code_plan
                code_yearly = code.yearly_code

                # Calculate the duration of the plan.
                if code_yearly:
                    days = code.code_plan.yearly_plan_duration
                else:
                    days = code.code_plan.plan_duration

                end_date = timezone.now() + timedelta( days = days )

                 # get the privious plan and deactivates it 
                try:
                    # deactivating the old plan
                    old_plan = Merchant_Subcribers.objects.get( user = account_user , active = True )
                    old_plan.active = False
                    old_plan.end_date = timezone.now()
                    old_plan.save()

                    # activating the new plans
                    if code_yearly:
                        Merchant_Subcribers.objects.create( user = account_user , active = True , plan = plan , end_date = end_date , yearly_plan = True)
                    else:
                        Merchant_Subcribers.objects.create( user = account_user , active = True , plan = plan , end_date = end_date )
                
                except Merchant_Subcribers.DoesNotExist :
                    # activating the new plans
                    Merchant_Subcribers.objects.create( user = account_user , active = True , plan = plan , end_date = end_date )

                # expiring the promo code 
                code.used_code = True
                code.user = account_user
                code.save()
                messages.info(request, f"Subscription plan is been activated for this account successfully.")

                subscriptions = Merchant_Subcribers.objects.get( user = account_user , active = True )

                #  sending email to the customer alerting him of the succesful order 
                subject = f'Successful Payment - {company_profile.merchant_business_name}'
                html_message = render_to_string(
                    'kiosk_emails/payment.html',
                    {
                    'user': company_profile,
                    'subscriptions':subscriptions,
                    } 
                )
                plain_message = strip_tags(html_message)
                from_email = 'support@mykroonapp.com'
                to = company_profile
                mail.send_mail(subject, plain_message, from_email, [to], html_message = html_message)
                del request.session['email']
                return JsonResponse("subscriptions is activated" , safe = False )
                # response = HttpResponse("<script>setTimeout(function() {window.close();}, 5000);</script>")
                # return response


            except Government_Promo_Code.DoesNotExist:
                messages.info(request, f"Promotional code is ether inactive or incorrect , kindly check the code and try again. ")

    context = {
        'plan': plan,
        'form':form,
        'user_profile':user_profile,
    }
    return render(request, 'app_subscription/gov_promo_code.html', context)  



@login_required()
def inapp_sub_page (request):
    form = Gov_Promo_codeForm()
    user_profile = BusinessProfile.objects.get ( user = request.user , active = True )

    if request.method == 'POST':
        form = Gov_Promo_codeForm(request.POST)
        company_profile = _company_account(request)

        if form.is_valid():
            promo_code = form.cleaned_data['promotional_code']
            try:
                code = Government_Promo_Code.objects.get ( promo_code = promo_code , used_code = False  )
                plan = code.code_plan
                code_yearly = code.yearly_code

                if code_yearly:
                    days = code.code_plan.yearly_plan_duration
                else:
                    days = code.code_plan.plan_duration

                end_date = timezone.now()+timedelta( days = days )

                 # get the privious plan and deactivates it 
                try:
                    # deactivating the old plan
                    old_plan = Merchant_Subcribers.objects.get( user = request.user , active = True )
                    old_plan.active = False
                    old_plan.end_date = timezone.now()
                    old_plan.save()

                    # activating the new plans
                    if code_yearly:
                        Merchant_Subcribers.objects.create( user = request.user , active = True , plan = plan , end_date = end_date , yearly_plan = True)
                    else:
                        Merchant_Subcribers.objects.create( user = request.user , active = True , plan = plan , end_date = end_date )
                
                except Merchant_Subcribers.DoesNotExist :
                    # activating the new plans
                    Merchant_Subcribers.objects.create( user = request.user , active = True , plan = plan , end_date = end_date )

                # expiring the promo code 
                code.used_code = True
                code.user = request.user
                code.save()
                messages.info(request, f"Subscription plan is been activated for this account successfully.")

                subscriptions = Merchant_Subcribers.objects.get( user=request.user , active = True )

                #  sending email to the customer alerting him of the succesful order 
                subject = f'Successful Payment - {company_profile.merchant_business_name}'
                html_message = render_to_string(
                    'kiosk_emails/payment.html',
                    {
                    'user': company_profile,
                    'subscriptions':subscriptions,
                    } 
                )
                plain_message = strip_tags(html_message)
                from_email = 'support@mykroonapp.com'
                to = company_profile
                mail.send_mail(subject, plain_message, from_email, [to], html_message = html_message)
                return redirect('inapp_sub_page')

            except Government_Promo_Code.DoesNotExist:
                messages.info(request, f"Promotional code is ether inactive or incorrect , kindly check the code and try again. ")

    context = {
        'form':form,
        'user_profile':user_profile,
    }
    return render(request, 'app_subscription/inapp_sub.html', context)  



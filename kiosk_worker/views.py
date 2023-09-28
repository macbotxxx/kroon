
import random
import string
import threading
import datetime
import pytz

from django.contrib import messages
from django.shortcuts import redirect, render
from django.db.models import Count
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
# django email settings
from django.core import mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

utc=pytz.UTC

from datetime import datetime, timezone

from subscriptions.models import Subscription_Plan ,Merchant_Subcribers
from kroon_otp.models import OPTs
from kiosk_cart.models import  Order
from kroon.users.models import User, BusinessProfile
from .forms import VerifyEmail, WorkerSignupForm, WorkerVerifyOtp



def opt_code():
    return ''.join(random.choices(string.digits, k=6))


# Create your views here.
@login_required()
def workers (request):
    try:
        worker = BusinessProfile.objects.filter( user = request.user, active = True )
    except BusinessProfile.DoesNotExist:
        worker = None
    user_profile = BusinessProfile.objects.get ( user = request.user , active = True )
    

    context = {
        'worker':worker,
        'user_profile':user_profile,
    }
    return render(request, 'kiosk_merchant_dash/workers.html', context)


@login_required()
def worker_details (request, worker_id):
    user_profile_set = User.objects.get (id=worker_id)
    user_profile = BusinessProfile.objects.get ( user = request.user, active = True )


    worker_sales = list(Order.objects.select_related("user", "payment").filter(  worker = user_profile_set.name , is_ordered = True  ).extra({'day': "to_char(created_date, 'DD MONTH')"}).values('day').annotate(sales_total=Count('id')).order_by('day')[0:28])

    context = {
        'user_profile_set':user_profile_set,
        'worker_sales':worker_sales,
        'user_profile':user_profile,
    }
    return render(request, 'kiosk_merchant_dash/worker_details.html', context)


@login_required()
def verify_email (request):
    user_profile = BusinessProfile.objects.get ( user = request.user , active = True)

    title = f'Worker Email Verification'
    description = f'This section requires your worker email address for verification, if the email address is registered with any of our platforms , their details will automatically be verified .'
    form_title = f'Email Verification'
    submit_button = f'Click To Verify Email'

    total_workers = 0

    try:
        worker = BusinessProfile.objects.get( user = request.user, active = True )
        total_workers = worker.workers.count()
    except BusinessProfile.DoesNotExist:
        pass
    
    # verifying the account ability to add workers
    try:
        user_plan = Merchant_Subcribers.objects.get( user = request.user , active = True )
    except Merchant_Subcribers.DoesNotExist :
        user_plan = None

    worker_limitation = False

    if user_plan is not None :
        if user_plan.plan.plan_name == "Basic":
            worker_limitation = False

        elif user_plan.plan.plan_name == "Kiosk Plus":
            if total_workers > 0:
                worker_limitation = False
            else:
                worker_limitation = True

        elif user_plan.plan.plan_name == "Kiosk Pro":
            worker_limitation = True

        else:
            print('no plan')
    
    else:
        return redirect('all_plans')

    # end worker restriction
    
    
    form = VerifyEmail()
    if request.method == 'POST':
        form = VerifyEmail(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            opt_pin = opt_code()

            # try:
            #     worker_id = User.objects.get( email = email )
            #     BusinessProfile.objects.get( workers_id = worker_id.id  )
            #     messages.info(request, f"{email} is already registered as a worker on kroon kiosk platform.")
            #     return HttpResponseRedirect(request.path_info)

            # except User.DoesNotExist:
            #     pass


            try:
                user_info = User.objects.get( email = email )
                request.session['email'] = user_info.email
                business_name = user_profile.business_name.upper()

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
                    'content': f"A company with the following names { business_name } has provided your email as a wroker , to proceed with the worker registeration process , kindly provide the following PIN to confirm your action which will be performed by your employer , note! some personal information will be displayed to the employer for clearifications, you can ignore this message if you havent applied for any position — this OTP code will expire in 5 minutes:",

                    } 
                )
                plain_message = strip_tags(html_message)
                from_email = f"{settings.EMAIL_HOST_USER}" 
            
                to = email
                mail.send_mail(subject, plain_message, from_email, [to], html_message = html_message)
                # store otp 

                return redirect('worker_otp_verification')

            except User.DoesNotExist:
                request.session['email'] = email
                return redirect(register_worker)

    context = {
        'form': form,

        # contents
        'title':title,
        'description':description,
        'form_title':form_title,
        'submit_button':submit_button,
        'total_workers':total_workers,
        'user_plan':user_plan,
        'worker_limitation':worker_limitation,
        'user_profile':user_profile,

        }
    return render(request, 'kiosk_merchant_dash/verify_worker.html', context)


@login_required()
def register_worker (request):
    user_profile = BusinessProfile.objects.get ( user = request.user , active = True)
    total_workers = 0

    # verifying the account ability to add workers
    try:
        user_plan = Merchant_Subcribers.objects.get( user = request.user , active = True )
    except Merchant_Subcribers.DoesNotExist :
        user_plan = None

    if user_plan is not None :
        if user_plan.plan.plan_name == "Basic":
            worker_limitation = False

        elif user_plan.plan.plan_name == "Kiosk Plus":
            if total_workers > 0:
                worker_limitation = False
            else:
                worker_limitation = True

        elif user_plan.plan.plan_name == "Kiosk Pro":
            worker_limitation = True

        else:
            print('no plan')
    
    else:
        return redirect('all_plans')

    title = f'Create Workers Account'
    description = f'This section creates your workers account which will automatically create an account for our platforms such as Kroon and Kroon Kiosk, if kroon app is been allowed in your region , your workers can easily make use of kroon app.'
    form_title = f'Account Creation'
    submit_button = f'Click To Register'

    if request.session['email'] == None:
        return redirect(verify_email)

    form = WorkerSignupForm()
    if request.method == 'POST':
        form = WorkerSignupForm(request.POST)
        if form.is_valid():
            user = form.save(request)
             # adding the new worker the companys account as a worker 
            merchant_business = BusinessProfile.objects.get( user = request.user, active = True )
            merchant_business.workers.add(user)

            request.session['email'] = None
            return redirect(workers)

    context = {
        'form': form,
        # contents
        'title':title,
        'description':description,
        'form_title':form_title,
        'submit_button':submit_button,
        'user_profile':user_profile,
        'worker_limitation':worker_limitation,
        'user_plan':user_plan,

        }

    return render(request, 'kiosk_merchant_dash/verify_worker.html', context)


@login_required()
def worker_otp_verification(request):
    title = f'Worker Code Verification'
    description = f'This section requires your worker code for verification, if the code  is valid , their information will be displayed to you for verification.'
    form_title = f'Worker Code Verification'
    submit_button = f'Click To Verify Worker Code'

    total_workers = 0

    try:
        worker = BusinessProfile.objects.get( user = request.user, active = True )
        total_workers = worker.workers.count()
    except BusinessProfile.DoesNotExist:
        pass
    
    # verifying the account ability to add workers
    try:
        user_plan = Merchant_Subcribers.objects.get( user = request.user , active = True )
    except Merchant_Subcribers.DoesNotExist :
        user_plan = None

    worker_limitation = False

    if user_plan is not None :
        if user_plan.plan.plan_name == "Basic":
            worker_limitation = False

        elif user_plan.plan.plan_name == "Kiosk Plus":
            if total_workers > 0:
                worker_limitation = False
            else:
                worker_limitation = True

        elif user_plan.plan.plan_name == "Kiosk Pro":
            worker_limitation = True

        else:
            print('no plan')
    
    else:
        return redirect('all_plans')

    form = WorkerVerifyOtp()
    if request.method == 'POST':
        form = WorkerVerifyOtp(request.POST)
        if form.is_valid():
            otp_pin = form.cleaned_data.get('code')

            if request.session['email'] == None:
                return redirect(verify_email)
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
                    return redirect('add_worker')

            else:
                check_otp = OPTs.objects.filter(otp_code = otp_pin)
                if check_otp:
                    #checking and verifying if the pin is invalid or expired  
                    current_time = datetime.now()
                    # check_otp_duration = utc.localize(check_otp.duration)
                    current_time = utc.localize(current_time)
                    for i in check_otp:
                        if i.duration < current_time:
                            messages.info(request, f"OTP pin has expired")
                            return HttpResponseRedirect(request.path_info)
                        else:
                            check_otp.delete()
                            messages.info(request, f"Opt pin valid")
                            return redirect('add_worker')
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

        'total_workers':total_workers,
        'user_plan':user_plan,
        'worker_limitation':worker_limitation,
    }
    
    return render(request, 'kiosk_merchant_dash/worker_code.html', context )


@login_required()
def add_worker (request):
    user_profile = BusinessProfile.objects.get ( user = request.user , active = True)
    
    if request.session['email'] == None:
        return redirect(verify_email)

    email = request.session.get('email')
    user_profile_set = User.objects.get ( email = email )

    if request.method == 'POST':
        # adding the new worker the companys account as a worker
        try:
            BusinessProfile.objects.get( workers = user_profile_set )
            messages.info(request, f"Kindly contact your worker to resign from his or her former employee, so to be able to continue.")
            return redirect(add_worker)

        except BusinessProfile.DoesNotExist:
            pass

        merchant_business = BusinessProfile.objects.get( user = request.user, active = True )
        merchant_business.workers.add(user_profile_set)
        request.session['email'] = None
        messages.info(request, f"{user_profile_set} has been added to your business profile successfully ")
        return redirect(workers)

    # working on the subscriptions restrictions
    try:
        user_plan = Merchant_Subcribers.objects.get( user = request.user , active = True )
    except Merchant_Subcribers.DoesNotExist :
        user_plan = None

    context = {
        'user_profile_set':user_profile_set,
        'user_plan':user_plan,
        'user_profile':user_profile,
    }

    return render(request, 'kiosk_merchant_dash/add_worker.html', context)
    

@login_required()
def remove_worker (request, *args, **kwargs):
    user_profile = BusinessProfile.objects.get ( user = request.user , active = True)

    worker_id = kwargs.get('worker_id')
    user_profile_set = User.objects.get ( id  = worker_id )
    try:
        BusinessProfile.objects.get( workers = user_profile_set )
        pass
        
    except BusinessProfile.DoesNotExist:
        messages.info(request, f"Worker profile does not exist on the business platform")
        return redirect(workers)

    merchant_business = BusinessProfile.objects.get( user = request.user, active = True )
    merchant_business.workers.remove(user_profile_set)
    messages.info(request, f"{user_profile_set} has been removed from your business profile successfully ")
    return redirect(workers)






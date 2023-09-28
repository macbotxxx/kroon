from django.http import HttpResponse
from django.shortcuts import redirect

from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from secrets import compare_digest
from django.conf import settings
from kroon.users.models import BusinessProfile
from subscriptions.models import Merchant_Subcribers
# from kiosk_cart.api.views import 

def _company_account (request):
    try:
        business_profiles = BusinessProfile.objects.get ( user = request.user , active = True )
        business_profile = business_profiles.user
    except BusinessProfile.DoesNotExist:
        checking_business_profile = BusinessProfile.objects.select_related("user").filter( workers = request.user )
        if checking_business_profile:
            for b in checking_business_profile:
                # print(checking_business_profile)
                business_profile = b.user
        else:
            business_profile = None
    return business_profile

# def unauthenticated_user(view_func):
# 	def wrapper_func(request, *args, **kwargs):
# 		if request.user.is_authenticated:
# 			return redirect('home')
# 		else:
# 			return view_func(request, *args, **kwargs)

# 	return wrapper_func

def allowed_user(allowed_roles=[]):
	def decorator(view_func):
		def wrapper_func(request, *args, **kwargs):

			group = None
			if request.user.groups.exists():
				group = request.user.groups.all()[0].name

			if group in allowed_roles:
				return view_func(request, *args, **kwargs)
			else:
				return HttpResponse('You are not authorized to view this page')
		return wrapper_func
	return decorator


def allowed_accounts(allowed_account_type = ['merchant']):
	def merchant_only(view_func):
		def merchant_function(request, *args, **kwargs):
			account_type = None
			if request.user:
				account_type = request.user.account_type

			if account_type in allowed_account_type:
				return view_func(request, *args, **kwargs)
			else:
				# return redirect('warning')
				return HttpResponse('You are not authorized to view this page')
		return merchant_function
	return merchant_only


def admin_only(view_func):
	def wrapper_function(request, *args, **kwargs):
		group = None
		if request.user.groups.exists():
			group = request.user.groups.all()[0].name
		
		# marketing urls and permissions
		if group == 'Marketers':
			return redirect('marketers:marketer_index')
	
		if group == 'Financial':
			return redirect('core:investorshome')

		if group == 'Gov_Worker':
			return redirect('gov_panel_home')
		
		if group == 'Gov_Super_Admin':
			return redirect('gov_panel_home')

		if group == 'admin':
			return view_func(request, *args, **kwargs)
		else:
			return HttpResponse('You are not authorized to view this page as an admin')

	return wrapper_function


# nontification decorator for Kiosk Pro 
def kiosk_pro_merchants ( request ):
	company_profile = _company_account(request)
	# user permissions
	try:
		user_plan = Merchant_Subcribers.objects.get( user = company_profile , active = True )
	except Merchant_Subcribers.DoesNotExist :
		user_plan = None
	 
	notifications_pass = False
	if user_plan is not None :
		if user_plan.plan.plan_name == "Kiosk Pro":
			notifications_pass = True
		else:
			notifications_pass = False
	else:
		notifications_pass = False

	return notifications_pass
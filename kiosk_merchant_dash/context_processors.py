
from kroon.users.models import BusinessProfile

# working on context

def merchant_business_accounts(request):
    if request.user.is_authenticated:
        my_business_profile = BusinessProfile.objects.filter(  user = request.user ).order_by('created_date')
    
    else:
        my_business_profile = None

    return dict(my_business_profile=my_business_profile)

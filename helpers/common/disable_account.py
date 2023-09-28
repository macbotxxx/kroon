# import all kiosk models
from kiosk_business_plan.models import Business_Plan
from kiosk_cart.models import Payment, CartItem , Order ,  OrderProduct 
from kiosk_stores.models import Merchant_Product
from subscriptions.models import Merchant_Subcribers
from kroon.users.models import User, BusinessProfile



class Delete_Accounts:
    """
    Functions that hodl both the delete account and disable account for both kroon and kiosk.
    """

    def kiosk_delete_account (self, user, user_id):
        user_profile = user
        users_id = user_id


        """
        this holds kiosk delete account function which is been taken action by the user ,
        this will delete all the user record on kiosk and return the user account to personal account , 
        which automatically denies the user the ability to access their kiosk account again.
        """
        # deleting all users records business plans
        user_business_plan = Business_Plan.objects.select_related('user').filter( user = user_profile )
        user_business_plan.delete()
        # ends here 

        # deleting all merchant payments , CartItem , Orders, Order Products
        user_payment = Payment.objects.select_related('user').filter( user = user_profile )
        user_cart_item = CartItem.objects.select_related('user', 'product', 'cart').filter( user = user_profile )
        user_orders = Order.objects.select_related('user','payment').filter( user = user_profile )
        user_completed_orders = OrderProduct.objects.select_related('user', 'order', 'payment', 'product').filter( user = user_profile )

        # deleting records ..
        user_payment.delete()
        user_cart_item.delete()
        user_orders.delete()
        user_completed_orders.delete()
        # ends here 

        # delete user product
        user_products = Merchant_Product.objects.select_related('user', 'category').filter( user = user_profile )
        user_products.delete()

        user_subscriptions = Merchant_Subcribers.objects.select_related('user', 'plan').filter( user = user_profile )
        user_subscriptions.delete()

        user_business_profile = BusinessProfile.objects.select_for_update('user').filter( user = user_profile )
        user_business_profile.delete()
        # ends here 

        # switching user account to personal account_type
        user_account = User.objects.get( id = users_id ) 
        user_account.account_type = 'personal'
        user_account.merchant_business_name = ''
        user_account.save()
        # ends here 

        response = True

        return response


    def kroon_disable_account():
        response = "done and working"

        return response

from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import BasePermission
from rest_framework.exceptions import APIException


from secrets import compare_digest
from django.conf import settings

from kroon.users.models import BusinessProfile


class SignatureMissMatch(APIException):
    """Raised when the signatures are not matched."""
    status_code = 401
    default_detail = "Signature header is invalid."
    default_code = "signature_invalid"


class SignatureHeaderMissing(APIException):
    """Raised when the request does not have the signature."""
    status_code = 401
    default_detail = "Signature header is missing. Make sure KOK-Authentication-Token is present in header."
    default_code = "signature_header_missing"


class APIAccessDenied(APIException):
    status_code = 401
    default_detail = "API Access Denied. Signature is not valid."
    default_code = "api_access_denied"


class MerchantAccessDenied(APIException):
    status_code = 404
    default_detail = "Your account is not permitted to take any of this actions, kindly provides the necessary documentation of your business , you can also contact your administrator . Still facing an issues email customer_care@kiosk.com"
    default_code = "merchant_access_denied"

class MerchantPermitDenied(APIException):
    status_code = 404
    default_detail = "This action is permitted only for kroon kiosk merchants , you can also contact your administrator . Still facing an issues email customer_care@kiosk.com"
    default_code = "merchant_access_denied"


class KOKPermission(BasePermission):

    def has_permission(self, request, *args, **kwargs):
        # Checking if the KOK auth is been authorized
        # is been authorized by switching it to true
       
        given_token = request.headers.get("KOK-Authentication-Token", None)
        if settings.KOK_AUTH:
            if not given_token:
                raise SignatureHeaderMissing()
            return given_token == settings.KOK_AUTH_KEYS
        
        else:
            given_token = None
            return given_token == None



class KOKMerchantPermission (BasePermission):

    def has_permission(self, request, *args, **kwargs):
        # this hold the permission for user account
        # to verify if the user is a merchant user or not
        
        try:
            user = BusinessProfile.objects.get ( user = request.user , active = True)
        except BusinessProfile.DoesNotExist:
            worker = BusinessProfile.objects.select_related("user").filter( workers = request.user )
            if worker:
                user = request.user
            else:
                raise MerchantAccessDenied()
        return user
    

class KOKMerchantOnly (BasePermission):

    def has_permission(self, request, *args, **kwargs):
        # this hold the permission for user account
        # to verify if the user is a merchant user or not
        
        merchant_role = request.user.account_type
        if merchant_role != 'merchant':
            raise MerchantPermitDenied()
        return merchant_role
            

       



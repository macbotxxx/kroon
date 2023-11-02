from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import BasePermission
from rest_framework.exceptions import APIException
from django.db.models import Q
from secrets import compare_digest
from django.conf import settings




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


class AdminReportsDenied(APIException):
    """Raised when the request is a allowed admin to get the records"""
    status_code = 401
    default_detail = "Access denied , admin reports is not allowed for the following account"
    default_code = "reports_access_denied"





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
        

class EtransacAdmin(BasePermission):

    def has_permission(self,request, *args, **kwargs):
        group = None
        if request.user.groups.exists():
            group = request.user.groups.get_or_create(name = 'etransac')
            if group :
                return True
            raise AdminReportsDenied()
        
    
class BlekieAdmin(BasePermission):
    
    def has_permission(self,request, *args, **kwargs):
        group = None
        if request.user.groups.exists():
            group = request.user.groups.get_or_create(name = 'blekie_tech')
            if group :
                return True
            raise AdminReportsDenied()
        

class IsBlekieAndEtransac(BasePermission):
    
    def has_permission(self,request, *args, **kwargs):
        group = None
        if request.user.groups.exists():
            group = request.user.groups.filter(Q(name = 'etransac') | Q( name = 'blekie_tech') )
            if group:
                return True
            raise AdminReportsDenied()

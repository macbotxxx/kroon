import string
import random
import requests

from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.generics import GenericAPIView
from rest_framework import status
from helpers.common.security import KOKPermission
from rest_framework.views import APIView


from generate_pin.models import Generate_Pin

def generated_pin():
    return ''.join(random.choices(string.digits, k=4))


class Generate_pin_view (APIView):
    permissions_classes = [ IsAuthenticated,KOKPermission ]

    def get (self, request, *args, **kwargs):
        # generating a random pin
        pin = generated_pin()

        # delete the previously geenrated pin 
        Generate_Pin.objects.filter( user = request.user ).delete()

        # generate a new pin
        Generate_Pin.objects.create( user = request.user, pin = pin )

        return Response({'status': 'success', 'message': 'one time pin is been generated successfully', 'data':pin},status = status.HTTP_201_CREATED )



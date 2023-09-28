# Signals that fires when a user logs in and logs out

from kroon.users.models import UserActivity
from django.contrib.auth import user_logged_in, user_logged_out
from django.dispatch import receiver
from accounts.models import LoggedInUser

## importing socket module
import socket
## getting the hostname by socket.gethostname() method
hostname = socket.gethostname()
## getting the IP address using socket.gethostbyname() method
ip_address = socket.gethostbyname(hostname)
## printing the hostname and ip_address
# print(f"Hostname: {hostname}")
# print(f"IP Address: {ip_address}")



@receiver(user_logged_in)
def on_user_logged_in(sender, request, **kwargs):
    LoggedInUser.objects.get_or_create(user=kwargs.get('user')) 
    UserActivity.objects.create(user=kwargs.get('user'), hostname = hostname, ip_address = ip_address) 


@receiver(user_logged_out)
def on_user_logged_out(sender, **kwargs):
    LoggedInUser.objects.filter(user=kwargs.get('user')).delete()
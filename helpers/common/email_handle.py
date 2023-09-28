import threading

from django.conf import settings
# django email settings
from django.core import mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from datetime import timedelta, datetime


"""
this script hold the email action
"""

class Login_Security_Email:
    """
    a security email is be sent to the merchant when even they login 
    this helps in the security process.
    this function is consists of two kroon and kroon kiosk security email
    """

    def security_kiosk_email( self, user , full_name):
        """
        this email template will be sent to the merchant user when even they
        they login to their account for security purposes
        KIOSK SECURITY EMAIL FUNCTION- 
        """
        # timing record of the login time
        time = datetime.now()
        # sending email to the customer alerting him of the succesful transfer 
        user_email = user
        user_name = full_name
       
        subject = "Kiosk Security Notification"
        html_message = render_to_string(
            'emails/security.html',
            {
            'header':"Kiosk Security Notification",
            'time': time,
            'user_name': user_name,
            } 
        )
        plain_message = strip_tags(html_message)
        from_email = f"{settings.EMAIL_HOST_USER}" 
        to = user_email
        mail.send_mail(subject, plain_message, from_email, [to], html_message = html_message)

        response = "sent"
        return response


    def security_kroon_email():
        response = "sent"
        return response

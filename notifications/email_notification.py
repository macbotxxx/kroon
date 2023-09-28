from django.contrib.auth import get_user_model
# import Django Packages
from django.core.mail import send_mail
from django.core import mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings

# import celery
from config import celery_app
from celery import shared_task
from celery.schedules import crontab

# user model
# User = get_user_model()


@celery_app.task()
def send_otp_email_func( email , otp_pin , platform , **kwargs):
        """
        this function handles the sending of OTP using email address
        its defines the users platforms which is used in identifing which 
        email templete will be sent to the email address. options are 
        kroon and kiosk .
        """
        notification_content = "Thank you for choosing Kroon Kiosk, the leading enterprise solution for small businesses. We are excited to have you on board! To proceed with your account activation, please use the following One-Time PIN (OTP) within the next 5 minutes:"
        
        if kwargs.get('forget_password_content') is None:
                content = notification_content
        else:
                content = kwargs.get('forget_password_content')
        
        subject = 'Kiosk OTP Verification'
        if platform == 'kroon':
                html_message = render_to_string(
                        'emails/otp.html',
                        {
                        'user': "Hello",
                        'opt': otp_pin,
                        'content':"f{content}",
                        } 
                )
        else:
                html_message = render_to_string(
                        'kiosk_emails/otp.html',
                        {
                        'user': "Hello",
                        'opt': otp_pin,
                        'content':"f{content}",

                        } 
                )

        plain_message = strip_tags(html_message)
        from_email = f"{settings.EMAIL_HOST_USER}" 

        to = email
        mail.send_mail(subject, plain_message, from_email, [to], html_message = html_message)
        return "Done"


@celery_app.task()
def kiosk_promo_code_email( *args , **kwargs ):
        #  sending email to the customer alerting him of the succesful order 
        subject = kwargs.get('subject')
        html_message = render_to_string(
        'kiosk_emails/payment.html',
        {
         'invoice_id': kwargs.get('invoice_id'),
         'amount_paid': kwargs.get('amount_paid'),
         'plan_duration': kwargs.get('plan_duration'),
         'sub_type': kwargs.get('sub_type'),
         'sub_start_date': kwargs.get('sub_start_date'),
         'sub_end_date': kwargs.get('sub_end_date'),
        }
        )
        plain_message = strip_tags(html_message)
        from_email = f"{settings.EMAIL_HOST_USER}" 
        to = kwargs.get('email')
        mail.send_mail(subject, plain_message, from_email, [to], html_message = html_message)



@celery_app.task()
def send_merchants_datail_email( *args, **kwargs ):
        # email notification for topup_payment
        subject = 'Login Details - Kroon Kiosk'
        html_message = render_to_string(
            'emails/onboarding_mail.html',
            {
            'name': kwargs.get("name"),
            'email':kwargs.get("email"),
            'default_password':"M080341i",
            } 
        )
        plain_message = strip_tags(html_message)
        from_email = f"{settings.EMAIL_HOST_USER}" 
        to = kwargs.get("email")
        mail.send_mail(subject, plain_message, from_email, [to], html_message = html_message)



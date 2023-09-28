from django.db.models.signals import pre_save
from allauth.account.signals import user_signed_up
from django.dispatch import receiver
from .models import User
from django.contrib.auth import user_logged_in
from django.dispatch.dispatcher import receiver
from django.contrib.sessions.models import Session
from .models import UserSession
from django.core import mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings




@receiver(user_logged_in)
def remove_other_sessions(sender, user, request, **kwargs):
    Session.objects.filter(usersession__user=user).delete() # removing user other session

    request.session.save() # here is the saving users current session

    # create a link from the user to the current session (for later removal)
    UserSession.objects.get_or_create(
        user=user,
        session=Session.objects.get(pk=request.session.session_key)
    )



#  SENDING WELCOME EMAIL MESSAGE TO NEW USERS 
@receiver(user_signed_up)
def user_sign_up_email_signal(request, user, **kwargs):
    print(user.account_type)
    # user signed up now send email
    # send email part - do your self
    # sending email to the user about to be giftted kroon token 
    subject = f'Kroon Welcomes You To Community'
    html_message = render_to_string(
        'emails/welcome.html',
        {
        'user': user.first_name,
        } 
    )
    plain_message = strip_tags(html_message)
    from_email = f"{settings.EMAIL_HOST_USER}" 
    to = user.email
    mail.send_mail(subject, plain_message, from_email, [to], html_message = html_message)



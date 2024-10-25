from django.core.mail import EmailMultiAlternatives
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.urls import reverse

from django_rest_passwordreset.signals import reset_password_token_created
from django_gunpermit.settings import WEBAPP_URL 
from django_gunpermit.settings import EMAIL_HOST 

@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    """
    Handles password reset tokens
    When a token is created, an e-mail needs to be sent to the user
    :param sender: View Class that sent the signal
    :param instance: View Instance that sent the signal
    :param reset_password_token: Token Model Object
    :param args:
    :param kwargs:
    :return:
    """
    # send an e-mail to the user
    user = reset_password_token.user
    print("first", user.first_name)
    print("last", user.last_name)
    context = {
        'first_name': user.first_name,
        'last_name': user.last_name,
        'reset_password_url': "{}?token={}".format(
            WEBAPP_URL,
            reset_password_token.key)
    }

    # render email text
    email_html_message = render_to_string(
        'email/password_reset_email.html', context)
    email_plaintext_message = render_to_string(
        'email/password_reset_email.txt', context)

    msg = EmailMultiAlternatives(
        # title:
        "Password Reset for {title}".format(title="Gun Permit"),
        # message:
        email_plaintext_message,
        # from:
        EMAIL_HOST,
        # to:
        [reset_password_token.user.email]
    )
    msg.attach_alternative(email_html_message, "text/html")
    msg.send()

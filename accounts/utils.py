from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.conf import settings

from foodonline_main import settings

def detectuser(user):
  if user.role == 1:
    return 'vendordashboard'
  elif user.role == 2:
    return 'custdashboard'
  elif user.role == None and user.is_superadmin:
    return '/admin'

def send_verification_email(request,user,mail_subject,mail_template):
    from_email = settings.DEFAULT_FROM_EMAIL
    current_site = get_current_site(request)
    message = render_to_string(mail_template,{
      'user':user,
      'domain':current_site,
      'uid': urlsafe_base64_encode(force_bytes(user.pk)),
      'token' : default_token_generator.make_token(user)
    })
    to_email=user.email
    email=EmailMessage(mail_subject,message,from_email,to = [to_email])
    email.send()


from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.urls import reverse_lazy
from .forms import UserForm
from .models import User,UserProfile
from django.contrib import messages,auth
from vendor.forms import VendorForm
from . utils import detectuser, send_verification_email
from django.contrib.auth.decorators import login_required,user_passes_test
from django.core.exceptions import PermissionDenied
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator

#restrict customer from accessing vendor page

def check_login_customer(user):
  if user.role == 2:
    return True
  else:
    raise PermissionDenied

def check_login_vendor(user):
  if user.role == 1:
    return True
  else:
    raise PermissionDenied
# Create your views here.

def registeruser(request):
  if request.user.is_authenticated:
    messages.warning(request,"you are already logged in")
    return redirect('myaccount')
  elif request.method == 'POST':
    form=UserForm(request.POST)
    if form.is_valid():
      #hashing the password using the set_password method
      password=form.cleaned_data['password']
      user = form.save(commit=False)
      user.set_password(password)
      user.role=User.CUSTOMER
      user.save()
      #send verification email
      mail_subject = "Please activate your account"
      mail_template = "accounts/emails/account_verification_email.html"
      send_verification_email(request,user,mail_subject,mail_template)
      messages.success(request, 'Your account has been created sucessfully')
      return redirect('registeruser')

      #hasing the password using the create user method and ORM query
      # first_name=form.cleaned_data['first_name']
      # last_name=form.cleaned_data['last_name']
      # username=form.cleaned_data['username']
      # email=form.cleaned_data['email']
      # password=form.cleaned_data['password']
      # user = User.objects.create_user(first_name=first_name,last_name=last_name,username=username,email=email,password=password)
      # user.role=User.CUSTOMER
      # user.save()
      # return redirect('registeruser')
    else:
      print('invalid')
      print(form.errors)
  else:
    form = UserForm()
  context={'form':form}
  return render(request,'accounts/registerUser.html',context)

def registervendor(request):
  if request.user.is_authenticated:
    messages.warning(request,"you are already logged in")
    return redirect('myaccount')
  elif request.method == 'POST':
    form = UserForm(request.POST)
    v_form = VendorForm(request.POST, request.FILES)
    if form.is_valid() and v_form.is_valid():
      first_name=form.cleaned_data['first_name']
      last_name=form.cleaned_data['last_name']
      username=form.cleaned_data['username']
      email=form.cleaned_data['email']
      password=form.cleaned_data['password']
      user = User.objects.create_user(first_name=first_name,last_name=last_name,username=username,email=email,password=password)
      user.role=User.RESTAURENT
      user.save()
      vendor = v_form.save(commit=False)
      vendor.user = user
      user_profile = UserProfile.objects.get(user=user)
      vendor.user_profile = user_profile
      vendor.save()
      #send verification email
      mail_subject = "Please activate your account"
      mail_template = "accounts/emails/account_verification_email.html"
      send_verification_email(request,user,mail_subject,mail_template)
      messages.success(request, 'Your account has been created sucessfully')
      return redirect('registervendor')
  else:
    form = UserForm()
    v_form = VendorForm()
  context = {'form':form, 'v_form':v_form}
  return render(request, 'accounts/registervendor.html', context)

def activate(request,uidb64,token):
  #Request for activating the account my marking the is_activate variable True
  try:
    uid= urlsafe_base64_decode(uidb64).decode()
    user = User._default_manager.get(pk=uid)
  except (TypeError, ValueError, user.DoesNotExist, OverflowError):
    user = None

  if user is not None and default_token_generator.check_token(user,token):
    user.is_active = True
    user.save()
    messages.success(request, 'Congratulations your account is now active')
    return redirect('myaccount')
  else:
    messages.error(request, 'Activation link is invalid or expired')
    return redirect('myaccount')

def login(request):
  if request.user.is_authenticated:
    messages.warning(request,"ou are already logged in")
    return redirect('myaccount')
  elif request.method == 'POST':
    email=request.POST['email']
    password=request.POST['password']
    user=auth.authenticate(email=email, password=password)
    if user is not None:
      auth.login(request, user)
      messages.success(request,'You have loged in successfully')
      return redirect('myaccount')
    else:
      messages.error(request,'Invalid credentials')
      return redirect('login')

  return render(request,'accounts/login.html')

def logout(request):
  auth.logout(request)
  messages.info(request,'You have logged out successfully')
  return redirect('login')

@login_required(login_url= reverse_lazy('login'))  # decorator to check if user is logged in before accessing this view
def myaccount(request):
  user = request.user
  redirect_url = detectuser(user)
  return redirect(redirect_url)

@login_required(login_url= reverse_lazy('login'))
@user_passes_test(check_login_customer)
def custdashboard(request):
  return render(request,'accounts/custdashboard.html')

@login_required(login_url= reverse_lazy('login'))
@user_passes_test(check_login_vendor)
def vendordashboard(request):
  return render(request,'accounts/vendordashboard.html')

def forgot_password(request):
  if request.method == 'POST':
    email=request.POST['email']
    if User.objects.filter(email=email).exists():
      user=User.objects.get(email__exact=email)

      #send password reset email
      mail_subject = "Reset your password"
      mail_template = "accounts/emails/password_reset_email.html"
      send_verification_email(request, user, mail_subject, mail_template)
      messages.success(request, 'Password reset email has been sent to your registered email address')
      return redirect('login')
    else:
      messages.error(request, 'Email does not exist')
      return redirect('forgot_password')
  return render(request,'accounts/forgot_password.html')

def forgot_password_validate(request,uidb64,token):
  #Request for validating the user who have clicked the password reset button
  try:
    uid= urlsafe_base64_decode(uidb64).decode()
    user = User._default_manager.get(pk=uid)
  except (TypeError, ValueError, user.DoesNotExist, OverflowError):
    user = None

  if user is not None and default_token_generator.check_token(user,token):
    request.session['uid'] = uid
    messages.info(request,'Please reset your password')
    return redirect('forgot_password_reset')
  else:
    messages.error(request, 'Password reset link is invalid or expired')
    return redirect('myaccount')

def forgot_password_reset(request):
  if request.method == 'POST':
    password = request.POST.get('password')
    confirm_password = request.POST['confirm_password']
    if password == confirm_password:
      uid = request.session.get('uid')
      user = User.objects.get(pk=uid)
      user.set_password(password)
      user.is_active = True
      user.save()
      messages.success(request, 'Password reset successfully')
      return redirect('login')
    else:
      messages.error(request, 'Passwords do not match')
      return redirect('forgot_password_reset')
  return render(request,'accounts/password_reset_form.html')
from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.urls import reverse_lazy
from .forms import UserForm
from .models import User,UserProfile
from django.contrib import messages,auth
from vendor.forms import VendorForm
from . utils import detectuser
from django.contrib.auth.decorators import login_required,user_passes_test
from django.core.exceptions import PermissionDenied

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
      messages.success(request, 'Your account has been created sucessfully')
      return redirect('registervendor')
  else:
    form = UserForm()
    v_form = VendorForm()
  context = {'form':form, 'v_form':v_form}
  return render(request, 'accounts/registervendor.html', context)

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
from django.shortcuts import render,redirect
from django.http import HttpResponse
from .forms import UserForm
from .models import User,UserProfile
from django.contrib import messages
from vendor.forms import VendorForm

# Create your views here.

def registeruser(request):
  if request.method == 'POST':
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
  if request.method == 'POST':
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

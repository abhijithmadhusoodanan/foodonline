from django.shortcuts import render,get_object_or_404,redirect
from django.urls import reverse_lazy
from . forms import VendorForm
from accounts.forms import User_profile_form
from accounts.models import UserProfile
from . models import Vendor
from django.contrib import messages
from django.contrib.auth.decorators import login_required,user_passes_test
from accounts.views import check_login_vendor
# Create your views here.

@login_required(login_url= reverse_lazy('login'))
@user_passes_test(check_login_vendor)
def vprofile(request):
 profile_obj = get_object_or_404(UserProfile, user = request.user)
 vendor_obj = get_object_or_404(Vendor, user = request.user)
 if request.method == 'POST':
  v_form = VendorForm(request.POST, request.FILES, instance=vendor_obj)
  u_profile_form = User_profile_form(request.POST, request.FILES, instance=profile_obj)
  if v_form.is_valid() and u_profile_form.is_valid():
   v_form.save()
   u_profile_form.save()
   messages.success(request, 'Your profile has been updated sucessfully')
   return redirect('vprofile')
  else:
   messages.error(request, 'Error updating your profile')
   print(v_form.errors)
   print(u_profile_form.errors)
 else:
  v_form = VendorForm(instance=vendor_obj)
  u_profile_form = User_profile_form(instance=profile_obj)

 context = {'v_form': v_form,
            'u_profile_form': u_profile_form,
            'profile_obj': profile_obj,
            'vendor_obj': vendor_obj}

 return render(request, "vendor/vprofile.html", context)
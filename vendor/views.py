from django.shortcuts import render,get_object_or_404,redirect
from django.urls import reverse_lazy
from . forms import VendorForm
from accounts.forms import User_profile_form
from accounts.models import UserProfile
from . models import Vendor
from django.contrib import messages
from django.contrib.auth.decorators import login_required,user_passes_test
from accounts.views import check_login_vendor
from menu.models import  Category,Food_item
from menu.forms import Add_categoryForm
from django.template.defaultfilters import slugify
from django.db import IntegrityError
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

@login_required(login_url= reverse_lazy('login'))
@user_passes_test(check_login_vendor)
def menubuild(request):
 vendor = Vendor.objects.get(user=request.user)
 categories = Category.objects.filter(vendor_name=vendor).order_by('created_at')
 context = {'categories': categories}
 return render(request, "vendor/menubuild.html",context)

@login_required(login_url= reverse_lazy('login'))
@user_passes_test(check_login_vendor)
def menu_fooditems(request,pk=None):
 vendor = Vendor.objects.get(user=request.user)
 category = get_object_or_404(Category.objects.filter(vendor_name=vendor),pk=pk)
 food_items = Food_item.objects.filter(category_name=category)
 print(food_items)
 context = {'food_items':food_items,
            'category':category}
 return render(request, "vendor/menu_fooditems.html", context)

def add_category(request):
  if request.method == 'POST':
    form = Add_categoryForm(request.POST)
    if form.is_valid():
      category_name = form.cleaned_data['category_name']
      category = form.save(commit=False)
      category.vendor_name = Vendor.objects.get(user=request.user)
      base_slug = slugify(category_name)
      unique_slug = base_slug
      num = 1
      while Category.objects.filter(slug=unique_slug).exists():
          unique_slug = f"{base_slug}-{num}"
          num += 1
      category.slug = unique_slug  # Assign unique sl
      try:
          category.save()  # ✅ Save the category instance
          messages.success(request, "Category added successfully")
          return redirect('menubuilder')
      except IntegrityError:
          messages.error(request, "This category already exists!")
    else:
     print(form.errors)
  else:
    form = Add_categoryForm()
  context = {'form': form}
  return render(request, "vendor/add_category.html", context)

def edit_category(request, pk = None):
  category = get_object_or_404(Category, pk=pk)
  if request.method == 'POST':
    form = Add_categoryForm(request.POST, instance=category)
    if form.is_valid():
        category_name = form.cleaned_data['category_name']
        category = form.save(commit=False)
        category.vendor_name = Vendor.objects.get(user=request.user)
        category.slug = slugify(category_name)
        category.save()
        messages.success(request,"category updated successfully")
        return redirect('menubuilder')
    else:
      print(form.errors)
  else:
    form = Add_categoryForm(instance=category)
  context = {'form': form,
             'category': category}
  return render(request, "vendor/edit_category.html", context)

def delete_category(request, pk=None):
  category = get_object_or_404(Category, pk=pk)
  category.delete()
  messages.success(request, "Category deleted successfully")
  return redirect('menubuilder')

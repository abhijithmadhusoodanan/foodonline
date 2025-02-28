from django.urls import path,include
from . import views
from accounts import views as AccountViews

urlpatterns = [
  path('',AccountViews.myaccount, name="vendor"),
  path('profile/',views.vprofile,name="vprofile"),
  path('menubuilder/',views.menubuild,name="menubuilder"),
  path('menubuilder/category/fooditems/<int:pk>/',views.menu_fooditems,name="menu_fooditems"),

  #add_category crud operations
  path('menubuilder/category/add/',views.add_category,name="add_category"),
  path('menubuilder/category/edit/<int:pk>/',views.edit_category,name="edit_category"),
  path('menubuilder/category/delete/<int:pk>/',views.delete_category,name="delete_category"),
]

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
  #food_items crud operations
  path('menubuilder/food/add/',views.add_food,name="add_food"),
  path('menubuilder/food/edit/<int:pk>/',views.edit_food,name="edit_food"),
  path('menubuilder/food/delete/<int:pk>/',views.delete_food,name="delete_food"),
]

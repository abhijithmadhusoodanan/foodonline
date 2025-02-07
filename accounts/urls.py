from django.urls import path,include
from . import views

urlpatterns = [
  path('', views.myaccount),
  path('registeruser/',views.registeruser,name='registeruser'),
  path('registervendor/',views.registervendor,name='registervendor'),
  path('login/',views.login,name='login'),
  path('logout/',views.logout,name='logout'),
  path('myaccount/',views.myaccount,name='myaccount'),
  path('custdashboard/',views.custdashboard,name='custdashboard'),
  path('vendordashboard/',views.vendordashboard,name='vendordashboard'),
  path('activate/<uidb64>/<token>/',views.activate,name='activate'),
  path('forgot_password/',views.forgot_password,name='forgot_password'),
  path('forgot_password_validate/<uidb64>/<token>/',views.forgot_password_validate,name='forgot_password_validate'),
  path('forgot_password_reset/',views.forgot_password_reset,name='forgot_password_reset'),
  path('vendor/', include('vendor.urls'))
]


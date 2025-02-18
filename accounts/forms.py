from django import forms
from . models import User,UserProfile
from .validators import validate_image_extension

class UserForm(forms.ModelForm):
  password=forms.CharField(widget=forms.PasswordInput)
  confirm_password=forms.CharField(widget=forms.PasswordInput)
  class Meta:
    model = User
    fields = ['first_name','last_name','username','email','password']

  def clean(self):
    cleaned_data=super(UserForm, self).clean()
    password=cleaned_data.get('password')
    confirm_password = cleaned_data.get('confirm_password')

    if password != confirm_password:
      raise forms.ValidationError(
        "Password does not match"
      )

class User_profile_form(forms.ModelForm):
  profile_photo = forms.FileField(widget=forms.FileInput(attrs={'class': 'btn btn-info'}), validators = [validate_image_extension])
  cover_photo = forms.FileField(widget=forms.FileInput(attrs={'class': 'btn btn-info'}), validators = [validate_image_extension])
  latitude = forms.CharField(widget=forms.TextInput(attrs={}))
  longitude = forms.CharField(widget=forms.TextInput(attrs={}))
  address = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter your address', 'required' : 'required'}))
  class Meta:
    model = UserProfile
    fields = ['profile_photo','cover_photo','address','country','state','city','pin_code','latitude','longitude']


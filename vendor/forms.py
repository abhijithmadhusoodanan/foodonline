from django import forms
from . models import Vendor
from accounts.validators import validate_image_extension

class VendorForm(forms.ModelForm):
  class Meta:
    model = Vendor
    fields = ['vendor_name','vendor_liscense']
  vendor_liscense = forms.FileField(widget=forms.FileInput(attrs={'class': 'btn btn-info'}), validators = [validate_image_extension])
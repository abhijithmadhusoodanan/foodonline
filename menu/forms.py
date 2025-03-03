from django import forms

from accounts.validators import validate_image_extension
from . models import Category,Food_item

class Add_categoryForm(forms.ModelForm):
  class Meta:
    model = Category
    fields = ['category_name','description']

class AddFoodForm(forms.ModelForm):
  image = forms.FileField(widget=forms.FileInput(attrs={'class': 'btn btn-info w-100'}), validators = [validate_image_extension])
  class Meta:
    model = Food_item
    fields = ['category_name','food_name', 'description', 'price', 'image', 'is_available']
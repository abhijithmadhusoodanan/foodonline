from django.db import models
from vendor.models import Vendor

# Create your models here.

class Category(models.Model):
  vendor_name = models.ForeignKey(Vendor, on_delete=models.CASCADE)
  category_name = models.CharField(max_length=100,unique=True)
  slug = models.SlugField(max_length=150,unique=True)
  description = models.TextField(blank=True, max_length=250)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  def clean(self):
    self.category_name = self.category_name.capitalize()



  def __str__(self):
    return self.category_name
  class Meta:
    verbose_name = 'Category'
    verbose_name_plural = 'Categories'

class Food_item(models.Model):
  category_name = models.ForeignKey(Category, on_delete=models.CASCADE)
  food_name = models.CharField(max_length=100)
  slug = models.SlugField(max_length=150,unique=True)
  price = models.DecimalField(max_digits=10, decimal_places=2)
  description = models.TextField(blank=True, max_length=250)
  image = models.ImageField(upload_to='food_images')
  is_available = models.BooleanField(default=True)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  def __str__(self):
    return self.food_name
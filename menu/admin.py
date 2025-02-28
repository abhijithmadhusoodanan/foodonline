from django.contrib import admin
from .models import Food_item,Category

# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
  prepopulated_fields = {'slug' : ('category_name',)}
  list_display = ('vendor_name','category_name','updated_at')
  search_fields = ('category_name', 'vendor_name__vendor_name')

class FoodItemAdmin(admin.ModelAdmin):
  prepopulated_fields = {'slug' : ('food_name',)}
  search_fields = ('category_name',)
  list_display = ('category_name','price','updated_at')

admin.site.register(Food_item,FoodItemAdmin)

admin.site.register(Category,CategoryAdmin)
from django.contrib import admin

# Register your models here.
from .models import *

class ProductAdmin(admin.ModelAdmin):
    list_display=['id','name','description','currency','price','image']
    list_filter=['id','name','price','image']

admin.site.register(User)
admin.site.register(Product,ProductAdmin)
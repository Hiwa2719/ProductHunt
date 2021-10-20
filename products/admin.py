from django.contrib import admin
from .models import Product


@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
    filter_horizontal = ['vote']

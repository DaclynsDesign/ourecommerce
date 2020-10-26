from django.contrib import admin
from .models import ProductModel

# Register your models here.


class ProductAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'slug']

    class Meta:
        model = ProductModel


admin.site.register(ProductModel, ProductAdmin)

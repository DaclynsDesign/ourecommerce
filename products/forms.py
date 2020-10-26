from django import forms
from .models import ProductModel

class ProductCreateForm(forms.ModelForm):
    class Meta:
        model = ProductModel
        fields='__all__'
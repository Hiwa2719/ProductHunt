from django import forms

from products.models import Product


class ProductCreateForm(forms.ModelForm):
    class Meta:
        model = Product
        exclude = 'hunter', 'vote'

from django import forms

from .models import Order

class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['name','email','address_country', 'address_house', 'postal_code']
from django import forms
from main.models import OrderItem


class AddQuantity(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = ['quantity']

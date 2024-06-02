from django import forms
from .models import EquipmentOrder


class UserForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()


class OrderForm(forms.ModelForm):
    class Meta:
        model = EquipmentOrder
        fields = ['order_date', 'order_time']
        widgets = {
            'order_date': forms.DateInput(attrs={'type': 'date'}),
            'order_time': forms.TimeInput(attrs={'type': 'time'}),
        }

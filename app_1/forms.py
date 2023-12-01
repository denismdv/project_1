from django import forms
from .models import *


class UpdateItemForm(forms.Form):
    description = forms.CharField(widget=forms.Textarea(attrs={'cols': 30, 'rows': 4}), label="Описание")
    price = forms.IntegerField(label="Цена")
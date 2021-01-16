
from django.forms import ModelForm
from .models import Choices
from django import forms



class ChoiceForm(ModelForm):
    class Meta:
        model = Choices
        fields = ['choice']


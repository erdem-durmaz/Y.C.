from django.db.models import fields
from django.forms import forms
from django.forms.fields import ImageField, FileField 
from django import forms
from django.forms import ModelForm
from django.forms.widgets import Select
from .models import Question

class UploadFileForm(forms.Form):
    name = forms.CharField(max_length=50)
    template = forms.DecimalField()
    photo = forms.ImageField()
    email = forms.EmailField()
    message = forms.CharField(max_length=500)

class QuestionForm(ModelForm):
    class Meta:
        model = Question
        fields = ['question','photo']
        

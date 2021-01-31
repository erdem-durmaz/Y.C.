from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + ("email",)



class SignUpForm(UserCreationForm):
    isim = forms.CharField(max_length=30, required=False, help_text='Opsiyonel.')
    soyisim = forms.CharField(max_length=30, required=False, help_text='Opsiyonel.')
    email = forms.EmailField(max_length=254, help_text='Zorunlu. Lütfen Email Adresinizi Girin.')

    class Meta:
        model = User
        fields = ('username', 'isim', 'soyisim', 'email', 'password1', 'password2', )
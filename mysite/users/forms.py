from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django import forms
from django.contrib.auth.models import User



class SignUpForm(UserCreationForm):
    isim = forms.CharField(max_length=30, required=False, help_text='Opsiyonel')
    soyisim = forms.CharField(max_length=30, required=False, help_text='Opsiyonel')
    email = forms.EmailField(max_length=254, help_text='Zorunlu. Lütfen Email Adresinizi Girin.')

    class Meta:
        model = User
        fields = ('username', 'isim', 'soyisim', 'email', 'password1', 'password2', )

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'Kullanıcı Adı'
        self.fields['username'].label=''

        self.fields['isim'].widget.attrs['class'] = 'form-control'
        self.fields['isim'].widget.attrs['placeholder'] = 'İsim'
        self.fields['isim'].label=''

        self.fields['soyisim'].widget.attrs['class'] = 'form-control'
        self.fields['soyisim'].widget.attrs['placeholder'] = 'Soyisim'
        self.fields['soyisim'].label=''

        self.fields['email'].widget.attrs['class'] = 'form-control'
        self.fields['email'].widget.attrs['placeholder'] = 'Email Adresiniz'
        self.fields['email'].label=''

        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['placeholder'] = 'Parolanızı Girin'
        self.fields['password1'].label=''
        
        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['placeholder'] = 'Parolanızı Tekrarlayın'
        self.fields['password2'].label=''
        self.fields['password2'].help_text=''



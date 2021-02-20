from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django import forms
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe



class SignUpForm(UserCreationForm):
    isim = forms.CharField(max_length=30, required=False, help_text='Opsiyonel')
    soyisim = forms.CharField(max_length=30, required=False, help_text='Opsiyonel')
    email = forms.EmailField(max_length=254, help_text='Zorunlu. Lütfen Email Adresinizi Girin.')
    terms = forms.BooleanField(required=True)

    class Meta:
        model = User
        fields = ('username', 'isim', 'soyisim', 'email', 'password1', 'password2','terms' )

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'Kullanıcı Adı'
        self.fields['username'].label=''
        self.fields['username'].help_text='Zorunlu. Sadece harfler, rakamlar ve @/./+/-/_ karakterleri kullanılabilir.'

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

        self.fields['terms'].widget.attrs['class'] = ''
        self.fields['terms'].label=''
        self.fields['terms'].help_text=mark_safe('<a data-toggle="modal" data-target="#exampleModalüyelik" href="#">Üyelik sözleşmesini</a> ve <a data-toggle="modal" data-target="#exampleModalgizlilik" href="#">Gizlilik sözleşmesini</a> okudum, onaylıyorum.')
        


class LoginForm(AuthenticationForm):
    
    class Meta:
        model = User
        fields = ('username', 'password',)

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'Kullanıcı Adı'
        self.fields['username'].label=''
        self.fields['username'].help_text=''

        self.fields['password'].widget.attrs['class'] = 'form-control'
        self.fields['password'].widget.attrs['placeholder'] = 'Parolanız'
        self.fields['password'].label=''
        
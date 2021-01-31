from django.forms import ModelForm
from django.forms import widgets
from django.forms.widgets import Select
from .models import  Challenge, Comment, ImageNominate, Profile
from django import forms



class ImageNominateForm(ModelForm):
    class Meta:
        model = ImageNominate
        fields = ['caption','owner','photo']
        widgets = {
            'caption': forms.TextInput(
				attrs={
					'class': 'form-control'
					}
				),
            'owner': forms.TextInput(
            attrs={
                'class': 'form-control'
                }
            ),
			}

class CommentForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        self.fields['comment'].label = ""
    class Meta:
        model = Comment
        fields = ['comment']
        widgets = {
            'comment': forms.TextInput(
				attrs={
                    'placeholder': 'Yorumunuzu Girin',
					'class': 'form-control',
                    'id':'post-text',
					}
				),
			}

class ProfileForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        self.fields['description'].label = ""

    class Meta:
        model = Profile
        fields = ['description','profile_pic']
       

class ContactForm(forms.Form):
    İsminiz = forms.CharField(required=True)
    Email = forms.EmailField(required=True)
    Mesajınız = forms.CharField(
        required=True,
        widget=forms.Textarea
    )
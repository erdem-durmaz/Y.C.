from django.forms import ModelForm
from django.forms import widgets
from django.forms.widgets import Select
from .models import  Challenge, Comment, ImageNominate, Mood, Profile
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
        
    class Meta:
        model = Profile
        fields = ['description','profile_pic']

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        self.fields['description'].widget.attrs['class'] = 'form-control form-control-lg'
        self.fields['description'].widget.attrs['rows'] = 3
        self.fields['description'].widget.attrs['placeholder'] = 'Hakkınızda'
        self.fields['description'].label=''

        self.fields['profile_pic'].label=''

       

class ContactForm(forms.Form):
    İsminiz = forms.CharField(required=True)
    Email = forms.EmailField(required=True)
    Mesajınız = forms.CharField(
        required=True,
        widget=forms.Textarea
    )
    def __init__(self, *args, **kwargs):
        super(ContactForm, self).__init__(*args, **kwargs)
        self.fields['İsminiz'].widget.attrs['class'] = 'form-control form-control-lg'
        self.fields['İsminiz'].widget.attrs['rows'] = 3
        self.fields['İsminiz'].widget.attrs['placeholder'] = 'İsminiz'
        self.fields['İsminiz'].label=''

        self.fields['Email'].widget.attrs['class'] = 'form-control form-control-lg'
        self.fields['Email'].widget.attrs['placeholder'] = 'Email adresiniz'
        self.fields['Email'].label=''

        self.fields['Mesajınız'].widget.attrs['class'] = 'form-control form-control-lg'
        self.fields['Mesajınız'].widget.attrs['placeholder'] = 'Mesajınız'
        self.fields['Mesajınız'].label=''


class MoodForm(ModelForm):
        
    class Meta:
        model = Mood
        fields = ['mood']

    def __init__(self, *args, **kwargs):
        super(MoodForm, self).__init__(*args, **kwargs)
        self.fields['mood'].widget.attrs['class'] = 'form-control form-control-lg'
        self.fields['mood'].widget.attrs['placeholder'] = 'Hakkınızda'

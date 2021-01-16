from django import forms
from .models import Course

class ContactForm(forms.Form):
    subject = forms.CharField(max_length=100)
    message = forms.CharField(widget=forms.Textarea)
    sender = forms.EmailField()
    cc_myself = forms.BooleanField(required=False)


class CourseForm(forms.Form):
    course_name = forms.CharField(max_length=100)
    pub_date = forms.DateTimeField()


class AttendeeForm(forms.Form):
    course = forms.ModelChoiceField(queryset=Course.objects.all())
    name = forms.CharField(max_length=100)
    email = forms.CharField(max_length=200)
    votes = forms.IntegerField()


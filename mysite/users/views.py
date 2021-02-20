from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import redirect, render
from django.urls import reverse
from .forms import  LoginForm, SignUpForm
from django.contrib import messages

# Create your views here.

def dashboard(request):
    return render (request,'users/dashboard.html')

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect(reverse('gamification:profile', kwargs={'username': request.user.username}))
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})




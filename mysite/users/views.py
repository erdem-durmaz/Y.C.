from django.contrib.auth import login, authenticate
from django.shortcuts import redirect, render
from django.urls import reverse
from .forms import CustomUserCreationForm,SignUpForm
from django.contrib import messages

# Create your views here.

def dashboard(request):
    return render (request,'users/dashboard.html')

def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(reverse("login"))
        else:
            messages.add_message(request, messages.ERROR,
                                 '<i class="fas fa-error"></i> Lütfen Gerekli Kriterleri Dikkate Alarak Seçim Yaparak Tekrar Deneyiniz')
            return redirect(reverse("users:register"))

    else:
        return render(request, "registration/register.html",{"form": CustomUserCreationForm})

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('users:dashboard')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})
from django.urls import path
from . import views


app_name = 'users'
urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),


] 

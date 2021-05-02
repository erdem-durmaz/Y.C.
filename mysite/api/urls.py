from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    path('hello/', views.HelloView.as_view(), name='hello'),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
    path('getUserId/', views.getUserIdView.as_view(), name='get_userid'),
    path('milks/', views.MilkList.as_view()),
    path('milks/<int:pk>/', views.MilkDetail.as_view()),   
    path('users/', views.UserList.as_view()),
    path('users/<int:pk>/', views.UserDetail.as_view()),
    path('blog/', views.BlogList.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
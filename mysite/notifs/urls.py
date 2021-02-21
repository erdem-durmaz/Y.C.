from django.urls import path
from . import views

app_name = 'notifications'

urlpatterns = [
    path('', views.all, name='all'),
    path('unread', views.unread, name='unread'),
    path('mark-as-read/<int:notif_id>', views.mark_as_read, name='mark_as_read'),
    path('mark-all-as-read/', views.mark_all_as_read, name='mark_all_as_read'),
    path('unreadcountajax/', views.unreadcountajax,name='unreadcountajax')
    # path('unread/>', views.unread, name='unread'),

]


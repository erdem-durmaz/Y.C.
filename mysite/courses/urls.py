from django.urls import path

from . import views

app_name = 'courses'
urlpatterns = [
    path('index/', views.index, name='index'),
    path('<int:course_id>/', views.detail, name= 'detail'),
    path('<int:course_id>/results', views.results, name= 'results'),
    path('<int:course_id>/vote', views.vote, name= 'vote'),
    path('form/', views.get_name, name= 'form'),
    path('', views.home, name= 'home'),
    path('courses/', views.get_courses, name= 'courses'),
    path('show-course/<int:course_id>/', views.show_course, name= 'show_course'),
    path('create-attendee/<int:course_id>/', views.create_attendee, name= 'create_attendee'),
    path('areyousure/<int:course_id>/', views.areyousure, name= 'areyousure'),
    path('delete-course/<int:course_id>/', views.delete_course, name= 'delete_course'),
    path('delete-attendee/<int:attendee_id>/', views.delete_attendee, name= 'delete_attendee'),
    path('update-attendee/<int:attendee_id>/<int:course_id>', views.update_attendee, name= 'update_attendee'),
]

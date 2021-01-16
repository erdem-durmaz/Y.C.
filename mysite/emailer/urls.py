from django.urls import path


from . import views

app_name = 'emailer'
urlpatterns = [
    path('', views.show_emails, name='show_emails'),
    path('add-message/', views.add_message, name='add_message'),
    path('conduct-quiz/<int:quiz_id>', views.conduct_quiz, name='conduct_quiz'),
    path('scores/<int:quiz_id>', views.score, name='score'),
    path('start/', views.start, name='start'),
    path('create-quiz/', views.create_quiz, name='create_quiz'),
    path('delete-quiz/<int:quiz_id>', views.delete_quiz, name='delete_quiz'),
] 

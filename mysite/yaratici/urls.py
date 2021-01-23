from django.urls import path
from . import views

app_name = 'yaratici'
urlpatterns = [
    path('', views.landing_page, name='landing_page'),
    path('anasayfa/', views.home, name='home'),
    path('posts/', views.posts, name='posts'),
    path('question/', views.get_question, name='get_question'),
    path('results/<int:question_id>', views.question_results, name='question_results'),
    path('post/<slug:slug>', views.show_post, name='show_post'),
    path('cerez-politikasi', views.cerez, name='cerez'),
    path('ajax/', views.ajax, name='ajax'),
    path('ajax/vote/', views.vote, name='vote'),
    # path('add-message/', views.add_message, name='add_message'),
    # path('conduct-quiz/<int:quiz_id>', views.conduct_quiz, name='conduct_quiz'),
    # path('scores/<int:quiz_id>', views.score, name='score'),
    # path('start/', views.start, name='start'),
    # path('create-quiz/', views.create_quiz, name='create_quiz'),
    # path('delete-quiz/<int:quiz_id>', views.delete_quiz, name='delete_quiz'),
] 

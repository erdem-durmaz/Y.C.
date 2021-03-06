from django.urls import path
from . import views

app_name = 'gamification'
urlpatterns = [
    path('', views.main, name='main'),
    # challenges
    path('challenge/<slug:slug>', views.show_challenge, name='show_challenge'),
    path('challenge/<slug:slug>/details', views.get_challenge_details, name='get_challenge_details'),
    path('challenge/<slug:slug>/<int:image_id>', views.show_image, name='show_image'),
    path('delete-image/<int:image_id>', views.delete_image, name='delete_image'),
    path('send-challenge-photo/<int:challenge_id>', views.send_challenge_photo, name='send_challenge_photo'),

    # likes
    path('like/', views.like, name='like'),
    path('like-image/', views.like_image, name='like_image'),
    # comments
    path('save-comment/', views.save_comment, name='save_comment'),
    path('delete-comment/', views.delete_comment, name='delete_comment'),
    path('image-save-comment/', views.image_save_comment, name='image_save_comment'),
    # profile
    path('redirecttouserprofile/', views.redirecttouserprofile, name='redirecttouserprofile'),
    path('profile/<username>', views.profile, name='profile'),
    path('profile-settings/<username>', views.profile_settings, name='profile_settings'),
    # leaderboard
    path('leaderboard/', views.leaderboard, name='leaderboard'),
    path('leaderboard/<int:year>/', views.leaderboardbyyear, name='leaderboardbyyear'),
    # contact form
    path('contact-form', views.contact_form, name='contact_form'),
    # weeklyquestion
    path('question/', views.get_question, name='weeklyquestion'),
    # imaginequestion
    path('imaginequestion/', views.lastimaginequestion, name='lastimaginequestion'),
    path('imaginequestionmain/', views.imaginequestionmain, name='imaginequestionmain'),
    path('imaginequestion/<int:imagine_id>', views.imaginequestion, name='imaginequestion'),
    # dailysleep
    path('dailysleep/', views.dailysleep, name='dailysleep'),

    # dailymilk
    path('dailymilk/', views.dailymilk, name='dailymilk'),

    #monthlyentries

    path('monthlypoints/', views.monthlyUserPoints, name='monthlypoints'),
    
    path('profileapi/', views.ProfileView.as_view(), name='profileapi'),
]
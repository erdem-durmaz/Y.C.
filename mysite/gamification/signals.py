from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Challenge, Comment, ImageNominate, Mood, Profile, ScoreBoard, ScoringActivities
from django.core.mail import send_mail


# @receiver(post_save, sender=User) 
# def create_profile(sender, instance, created, **kwargs):
# 	if created:
# 		print('signal worked')



        
        

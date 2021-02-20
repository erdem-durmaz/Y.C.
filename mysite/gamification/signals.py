from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Challenge, Comment, ImageNominate, Mood, Profile, ScoreBoard, ScoringActivities
from django.core.mail import send_mail


# @receiver(post_save, sender=User) 
# def create_profile(sender, instance, created, **kwargs):
# 	if created:
# 		print('signal worked')

@receiver(post_save,sender=User) 
def create_profile(sender, instance, created, **kwargs):
    # if created:
    isim = instance.username
    email = instance.email
    subject = f"{isim} Kayıt Oldu!"
    messagetext = f"Email adresi: {email}"
    senderemail = "erdemdur.mailer@gmail.com"
    recipients = ['berdushwile@gmail.com', 'yaraticicocugum@gmail.com']
    try:
        send_mail(subject, messagetext, senderemail, recipients)            
    except:
        print("Hata oldu email gönderemedim")
    else:
        print('mail gönderildiiii')

        
        

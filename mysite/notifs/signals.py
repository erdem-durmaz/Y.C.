''' Django notifications signal file '''
# -*- coding: utf-8 -*-
from django.dispatch import Signal
from django.dispatch.dispatcher import receiver
from django.db.models.query import QuerySet
from .models import Notif
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_save
from yaratici.models import BlogPost,Question,ImagineQuestion
from gamification.models import Challenge,ImageNominate
from django.contrib.auth.models import User

notify = Signal(providing_args=[  # pylint: disable=invalid-name
    'recipient', 'actor', 'verb', 'description','target',
])

@receiver(notify)
def my_handler(sender, **kwargs):
    recipient=kwargs.pop('recipient')
    actor = kwargs.pop('actor')
    verb = kwargs.pop('verb')
    description = kwargs.pop('description',None)
    image = kwargs.pop('image',None)
    comment = kwargs.pop('comment',None)
    challenge=kwargs.pop('challenge',None)

    # notify.send(instance, verb='was saved')

    if isinstance(recipient, (QuerySet, list)):
        recipients = recipient
    else:
        recipients = [recipient]


    for recipient in recipients:
        newnotify = Notif(
            recipient=recipient,
            actor_id = actor,
            verb=str(verb),
            image= image,
            comment = comment,
            challenge = challenge,
        )
        newnotify.save()

    #     # Set optional objects
    #     for obj, opt in optional_objs:
    #         if obj is not None:
    #             setattr(newnotify, '%s_object_id' % opt, obj.pk)
    #             setattr(newnotify, '%s_content_type' % opt,
    #                     ContentType.objects.get_for_model(obj))

    #     if kwargs and EXTRA_DATA:
    #         newnotify.data = kwargs

    #     newnotify.save()
    #     new_notifications.append(newnotify)

    # return new_notifications

@receiver(post_save, sender=BlogPost)
def send_blog_notification(sender,instance, created,**kwargs):
    if created == True:
        sender=User.objects.get(pk=3)
        users=User.objects.all()
        notify.send(sender,recipient=users,actor=sender, verb='Yeni blog yazısı yayınlandı!')

@receiver(post_save, sender=Question)
def send_quiz_notification(sender,instance, created,**kwargs):
    if created == True:
        sender=User.objects.get(pk=3)
        users=User.objects.all()
        notify.send(sender,recipient=users,actor=sender, verb='Yeni anket sorusu yayınlandı!')

@receiver(post_save, sender=ImagineQuestion)
def send_imaginequestion_notification(sender,instance, created,**kwargs):
    if created == True:
        sender=User.objects.get(pk=3)
        users=User.objects.all()
        notify.send(sender,recipient=users,actor=sender, verb='Yeni hayal gücü sorusu yayınlandı!')
       
@receiver(post_save, sender=Challenge) 
def send_challenge_notification(sender, instance, created, **kwargs):
    if created == True:
        sender=User.objects.get(pk=3)
        users=User.objects.all()
        notify.send(sender,recipient=users,actor=sender, challenge= instance, verb='Yeni Challenge yayınlandı!')

@receiver(post_save, sender=ImageNominate) 
def send_challengephoto_notification(sender, instance, created, **kwargs):
    if created == True:
        users=User.objects.all()
        notify.send(sender,recipient=users,actor=instance.user, image= instance, verb='Fotoğraf yüklendi!')




from django.core.mail import send_mail, EmailMessage
from django.template.loader import render_to_string
from django.conf import settings



def send_html_email(to_list, subject, template_name, context, sender=settings.DEFAULT_FROM_EMAIL):
    msg_html = render_to_string(template_name, context)
    msg = EmailMessage(subject=subject, body=msg_html, from_email=sender, bcc=to_list)
    msg.content_subtype = "html"  # Main content is now text/html
    return msg.send()

@receiver(post_save,sender=User) 
def create_profile(sender, instance, created, **kwargs):
    if created:
        emails=['yaraticicocugum@gmail.com',instance.email]
        subject = f"{instance.username}, MiO Dijital Yaratıcılık Platformuna Hoş Geldiniz!!"
        context={
        'username':'username'
        }
        try:
            send_html_email(emails, subject, 'email.html', context)           
        except:
            print("Hata oldu email gönderemedim")
        else:
            print('mail gönderildiiii')
        
        # isim = instance.username
        # email = instance.email
        # subject = f"{isim} Kayıt Oldu!"
        # messagetext = f"Email adresi: {email}"
        # senderemail = "yaraticicocugum@gmail.com"
        # recipients = ['yaraticicocugum@gmail.com',]
        # try:
        #     send_mail(subject, messagetext, senderemail, recipients)            
        # except:
        #     print("Hata oldu email gönderemedim")
        # else:
        #     print('mail gönderildiiii')


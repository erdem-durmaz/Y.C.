''' Django notifications signal file '''
# -*- coding: utf-8 -*-
from django.dispatch import Signal
from django.dispatch.dispatcher import receiver
from django.db.models.query import QuerySet
from .models import Notif
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_save
from yaratici.models import BlogPost
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
def send_blog_notification(sender,**kwargs):
    sender=User.objects.get(pk=3)
    users=User.objects.all()
    notify.send(sender,recipient=users,actor=sender, verb='Yeni blog yazısı yayınlandı!')
       

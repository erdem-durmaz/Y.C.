from django.contrib import admin

from .models import Notif


class NotifAdmin(admin.ModelAdmin):
    list_display = ('recipient', 'actor_id','unread')
    list_filter = ('unread','timestamp',)



admin.site.register(Notif, NotifAdmin)
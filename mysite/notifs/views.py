from django.db.models import Avg, Sum, Max
from .models import Notif
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.urls import reverse
from django.shortcuts import get_object_or_404, redirect, render, HttpResponse
from django.contrib import messages
import json
from .models import Notif

from django.contrib.auth.decorators import login_required
from datetime import datetime,timedelta

@login_required
def all(request):
    notifications = Notif.objects.filter(recipient=request.user)
    unreadnotifcount = Notif.objects.filter(recipient=request.user,unread=True).count()
    
    context = {
        'notifs': notifications,
        'unreadnotifcount':unreadnotifcount
    }
    # for notif in notifications:
    #     notif.mark_as_read()
    return render(request, 'notification/all.html', context)

@login_required
def unread(request):
    notifications = Notif.objects.filter(recipient=request.user,unread=True)
    context = {
        'notifs': notifications,
    }
    return render(request, 'notification/all.html', context)

@login_required
def mark_as_read(request, notif_id):
    notification = get_object_or_404(
        Notif, pk=notif_id)
    notification.mark_as_read()

    return redirect('notifications:all')

@login_required
def mark_all_as_read(request):
    if request.method == "POST":
        print(request.POST)
        if request.POST.get("operation") == "read-all" and request.is_ajax():
            
            content_id = request.POST.get("content_id", None)
            user = get_object_or_404(User,pk=content_id)
            notifications = Notif.objects.filter(recipient=user,unread=True)
            for notif in notifications:
                notif.mark_as_read()

            ctx = {"user": str(request.user), "content_id": content_id,}
            return HttpResponse(json.dumps(ctx), content_type='application/json')


def unreadcountajax(request):
    if request.user.is_authenticated:
        if request.is_ajax():
            unreadnotifcount = Notif.objects.filter(recipient=request.user,unread=True).count()
            ctx = unreadnotifcount
            return HttpResponse(json.dumps(ctx), content_type='application/json')
    else:
        ctx = 0
        return HttpResponse('')

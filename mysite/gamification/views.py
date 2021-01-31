from django.conf import settings
from .forms import CommentForm, ContactForm, ImageNominateForm, ProfileForm
from .models import Challenge, Comment, ImageNominate, Profile, ScoreBoard
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.urls import reverse
from django.shortcuts import get_object_or_404, redirect, render, HttpResponse
from django.contrib import messages
import json
import os
from django.contrib.auth.decorators import login_required

# Create your views here.
def profile_settings(request, username):
    user = User.objects.get(username=username)


    if request.user != user:
        messages.add_message(request, messages.ERROR,
                                 '<i class="fas fa-error"></i> Yetkiniz Yok!, Anasayfaya Yönlendirildi')
        return redirect('gamification:main')

    if request.method == 'POST':
        current_profile_pic = os.path.join(settings.MEDIA_ROOT, user.profile.profile_pic.path)

        if user.profile.profile_pic.path:
            pass
            # os.remove(rf"{user.profile.profile_pic.path}")
        print(request.POST)
        if user.profile:
            form = ProfileForm(request.POST, instance=user.profile, files=request.FILES)
            if form.is_valid():
                form.save()
                return redirect(reverse('gamification:profile', kwargs={'username': user.username}))
        else:
            form = ProfileForm(request.POST, request.FILES)
            new_profile = Profile(
                description=form.cleaned_data['description'],
                user =request.user,
                profile_pic=form.cleaned_data['profile_pic'],
            )
            new_profile.save()
            
            return redirect(reverse('gamification:profile', kwargs={'username': user.username}))
    else:
        form = ProfileForm(instance=user.profile)
        # form = ProfileForm()

    context = {
        'user': user,
        'form': form
    }
    return render(request, 'gamification/profile-settings.html', context)


def profile(request, username):
    user = User.objects.get(username=username)
    # print(user.profile.profile_pic.url)
    if not user:
        return redirect('main')
    # challenge = Challenge.objects.get(pk=1).image_likes.all()
    challenge = Challenge.objects.filter(user__id=3).all()
    likes = 0
    for i in challenge:
        if user in i.image_likes.all():
            likes +=1

    if not Profile.objects.filter(user=user).exists() :
        new_profile = Profile(
            user=user,
        )
        new_profile.save()
    profile = Profile.objects.get(user=user)
    context = {
        'username': username,
        'user': user,
        'profile': profile,
        'image_likes': likes
    }
    return render(request, 'gamification/profile.html', context)

def get_challenge_details(request, slug):
    form = CommentForm
    challenge = get_object_or_404(Challenge,slug=slug)
    return render(request,'gamification/get-challenge-details.html',{'challenge':challenge,'form':form})


def show_image(request, slug, image_id):
    form = CommentForm
    # challenges = Challenge.objects.filter(is_Published__exact=True).order_by('-create_date')
    image = get_object_or_404(ImageNominate,pk=image_id)
    challenge = get_object_or_404(Challenge,slug=slug)
    comments = Comment.objects.order_by('-date')
    return render(request,'gamification/show-image.html', {'image':image,'challenge': challenge,'form':form})

@login_required
def main(request):
    form = CommentForm
    challenges = Challenge.objects.filter(is_Published__exact=True).order_by('-create_date')
    comments = Comment.objects.order_by('-date')
    return render(request, 'gamification/main.html', {'challenges': challenges,'comments':comments,'form':form})


def delete_comment(request):
    if request.method =="POST":
        print(request.POST)
        if request.POST.get("operation") == "delete_comment" and request.is_ajax():
            content_id = int(request.POST.get("content_id"))
            comment = get_object_or_404(Comment,pk=content_id)
            ctx={"comment_id":comment.id,"message":"Başarıyla Silindi"}
            comment.delete()
            return HttpResponse(json.dumps(ctx), content_type='application/json')

# Like for Challenges
def save_comment(request):
    if request.method =="POST":
        print(request.POST)
        if request.POST.get("operation") == "send_comment" and request.is_ajax():
            form = CommentForm(request.POST)
            content_id=request.POST.get("content_id",None)
            challenge=get_object_or_404(Challenge,pk=content_id)
            if form.is_valid():
                new_comment = Comment(
                    comment = form.cleaned_data['comment'],
                    user = request.user,
                    challenge = challenge
                    )
                new_comment.save()
                ctx={"user":str(request.user),"likes_count":challenge.image_likes.count(),"content_id":content_id,"text":form.cleaned_data['comment']}
                return HttpResponse(json.dumps(ctx), content_type='application/json')

# Like for Images
def image_save_comment(request):
    if request.method =="POST":
        print(request.POST)
        if request.POST.get("operation") == "send_comment" and request.is_ajax():
            form = CommentForm(request.POST)
            content_id=request.POST.get("content_id",None)
            image=get_object_or_404(ImageNominate,pk=content_id)
            if form.is_valid():
                new_comment = Comment(
                    comment = form.cleaned_data['comment'],
                    user = request.user,
                    image = image
                    )
                new_comment.save()
                ctx={"user":str(request.user),"content_id":content_id,"text":form.cleaned_data['comment']}
                return HttpResponse(json.dumps(ctx), content_type='application/json')



# Like for Challenges
def like(request):
       if request.method =="POST":
        #    print(request.POST['content_id'])
           if request.POST.get("operation") == "like_submit" and request.is_ajax():
                content_id=request.POST.get("content_id",None)
                challenge=get_object_or_404(Challenge,pk=content_id)
                score = ScoreBoard.objects.filter(user=request.user).filter(challenge=challenge)
                    # score = get_object_or_404(ScoreBoard,user=request.user,challenge=challenge)
                print(score)
                if challenge.image_likes.filter(id=request.user.id): #already liked the content
                    challenge.image_likes.remove(request.user) #remove user from likes 
                    score.delete()
                    liked=False
                    
                else:
                    challenge.image_likes.add(request.user) 
                    liked=True
                    score = ScoreBoard(
                        user=request.user,
                        challenge=challenge,
                        score = 20 
                    )
                    score.save()
                    messages.add_message(request, messages.SUCCESS,
                                 '<i class="fas fa-trophy"></i> Tebrikler! 20 Puan Kazandın')
                ctx={"likes_count":challenge.image_likes.count(),"liked":liked,"content_id":content_id}
                return HttpResponse(json.dumps(ctx), content_type='application/json')


def show_challenge(request,slug):
    form = CommentForm
    challenge = get_object_or_404(Challenge, slug=slug)
    nominees = ImageNominate.objects.filter(challenge=challenge)
    comments = Comment.objects.order_by('-date')
    return render(request, 'gamification/show_challenge.html', {'form':form,'challenge': challenge,'nominees':nominees,'comments':comments})


# like for challenge photos
def like_image(request):
    if request.method =="POST":
        print(request.POST)
        if request.POST.get("operation") == "like_submit" and request.is_ajax():
            nominee_id=request.POST.get("content_id",None)
            nominee= get_object_or_404(ImageNominate,pk=nominee_id)
            challenge_id=request.POST.get("challenge_id",None)
            challenge=get_object_or_404(Challenge,pk=challenge_id)
            # score = ScoreBoard.objects.filter(user=request.user).filter(challenge=challenge)
            #     # score = get_object_or_404(ScoreBoard,user=request.user,challenge=challenge)
            # print(score)
            if nominee.image_likes.filter(id=request.user.id): #already liked the content
                nominee.image_likes.remove(request.user) #remove user from likes 
                # score.delete()
                liked=False
                
            else:
                nominee.image_likes.add(request.user) 
                liked=True
                # score = ScoreBoard(
                #     user=request.user,
                #     challenge=challenge,
                #     score = 20 
                # )
                # score.save()
                # messages.add_message(request, messages.SUCCESS,
                #              '<i class="fas fa-trophy"></i> Tebrikler! 20 Puan Kazandın')
            ctx={"likes_count":nominee.image_likes.count(),"liked":liked,"content_id":nominee_id}
            return HttpResponse(json.dumps(ctx), content_type='application/json')


def send_challenge_photo(request, challenge_id):
    print(request.POST)
    challenge = get_object_or_404(Challenge,pk=challenge_id)
    print(challenge)
    if request.method == 'POST':
        challenge = get_object_or_404(Challenge,pk=challenge_id)
        print(challenge)
        form = ImageNominateForm(request.POST, request.FILES)
        if form.is_valid():
            new_photo = ImageNominate(
                caption=form.cleaned_data['caption'],
                user =request.user,
                challenge = challenge,
                photo=form.cleaned_data['photo'],
            )
            new_photo.save()

            print('saved')
            messages.add_message(request, messages.SUCCESS,
                             '<i class="fas fa-trophy"></i> Tebrikler! Fotoğrafınız Yüklendi')
            return HttpResponseRedirect(reverse('gamification:show_challenge', args=(challenge.slug,)))
    else:
        form = ImageNominateForm()
    
    return render(request, 'gamification/send-challenge-photo.html', {'form': form, 'challenge':challenge})


def contact_form(request):
    
    form = ContactForm()
    return render(request, 'gamification/contact-form.html', {'form': form})

from django.db.models import Avg, Sum, Max
from yaratici.models import Question, BlogPost, ImagineQuestion
from django.conf import settings
from .forms import CommentForm, ContactForm, ImageNominateForm, ProfileForm
from .models import Challenge, Comment, ImageNominate, Profile, ScoreBoard, ScoringActivities
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.urls import reverse
from django.shortcuts import get_object_or_404, redirect, render, HttpResponse
from django.contrib import messages
import json
import os
from django.contrib.auth.decorators import login_required
from datetime import datetime

NOW = datetime.now()

POINTS = [
    {'id': 2, 'score': 1, 'title': 'Challenge - Fotoğraf Yükle'},
    {'id': 3, 'score': 1, 'title': 'Challenge - Yaptığın Like'},
    {'id': 4, 'score': 1, 'title': 'Challenge - Fotoğrafına gelen like'},
    {'id': 5, 'score': 1, 'title': 'Challenge - Fotoğraflara yaptığın yorum'},
    {'id': 6, 'score': 1, 'title': 'Challenge - Fotoğrafına gelen yorum'},
    {'id': 7, 'score': 1, 'title': 'Challenge - Ana Aktivite Like'},
    {'id': 8, 'score': 1, 'title': 'Haftalık Soru'},
    {'id': 9, 'score': 1, 'title': 'Blog Yazı Okuma'},
    {'id': 10, 'score': 1, 'title': 'Yaratıcı Soru'}
]
# Create your views here.


def contact_form(request):
    form = ContactForm()
    points = ScoringActivities.objects.values('id', 'score', 'title')
    print(points)

    context = {
        'form': form,
    }
    return render(request, 'gamification/contact-form.html', context)


def leaderboard(request):
    winnerlst = list()
    place = 1
    top213 = []
    restlst = list()
    leaderboard = ScoreBoard.objects.values('user').annotate(
        sum=Sum('totalscore')).order_by('-sum')

    if len(leaderboard) >= 3:

        for player in leaderboard[:3]:
            currentuser = get_object_or_404(User, pk=player['user'])
            print(currentuser)
            board = dict()
            board['place'] = place
            board['username'] = currentuser.username
            board['imgpath'] = currentuser.profile.profile_pic.url
            board['points'] = player['sum']
            winnerlst.append(board)
            place += 1
        top213.append(winnerlst[1])
        top213.append(winnerlst[0])
        top213.append(winnerlst[2])

        rest = ScoreBoard.objects.values('user').annotate(
            sum=Sum('totalscore')).order_by('-sum')
        for player in rest[3:]:
            currentuser = get_object_or_404(User, pk=player['user'])
            board = dict()
            board['place'] = place
            board['username'] = currentuser.username
            board['imgpath'] = currentuser.profile.profile_pic.url
            board['points'] = player['sum']
            restlst.append(board)
            place += 1

    context = {
        'leaders': top213,
        'rest': restlst,
        'month': NOW
    }

    return render(request, 'gamification/leaderboard.html', context)


@login_required
def profile_settings(request, username):
    user = User.objects.get(username=username)

    if request.user != user:
        messages.add_message(request, messages.ERROR,
                             '<i class="fas fa-error"></i> Yetkiniz bulunmuyor, anasayfaya yönlendirildi')
        return redirect('gamification:main')

    if request.method == 'POST':
        # current_profile_pic = os.path.join(settings.MEDIA_ROOT, user.profile.profile_pic.path)

        # if user.profile.profile_pic.path:
        #     pass
        #     # os.remove(rf"{user.profile.profile_pic.path}")
        # print(request.POST)
        if user.profile:
            form = ProfileForm(
                request.POST, instance=user.profile, files=request.FILES)
            if form.is_valid():
                form.save()
                return redirect(reverse('gamification:profile', kwargs={'username': user.username}))
        else:
            form = ProfileForm(request.POST, request.FILES)
            new_profile = Profile(
                description=form.cleaned_data['description'],
                user=request.user,
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


def calculate_score(user):
    # Calculate Challenge Like Sum
    scoresheet = ScoreBoard.objects.filter(user=user).filter(date__month=NOW.month).values(
        'id', 'activity', 'date', 'deleted', 'weeklyquestion', 'imaginequestion')

    points = ScoringActivities.objects.values('id', 'score', 'title')

    total_point = 0
    challenges = 0
    likes = 0
    comments = 0
    images = 0
    weeklyquestion = 0
    imaginequestion = 0
    results = dict()
    for scoreobj in scoresheet:
        if scoreobj['activity'] == 3 or scoreobj['activity'] == 4 or scoreobj['activity'] == 7:  # likes
            if scoreobj['deleted'] == False:
                activitynum = scoreobj['activity']
                for pointobj in points:
                    if activitynum == pointobj['id']:
                        total_point += pointobj['score']
                        challenges += pointobj['score']
                        likes += pointobj['score']
            else:
                activitynum = scoreobj['activity']
                for pointobj in points:
                    if activitynum == pointobj['id']:
                        total_point -= pointobj['score']
                        challenges -= pointobj['score']
                        likes -= pointobj['score']

        elif scoreobj['activity'] == 5 or scoreobj['activity'] == 6:  # comments
            if scoreobj['deleted'] == False:
                activitynum = scoreobj['activity']
                for pointobj in points:
                    if activitynum == pointobj['id']:
                        total_point += pointobj['score']
                        challenges += pointobj['score']
                        comments += pointobj['score']
            else:
                activitynum = scoreobj['activity']
                for pointobj in points:
                    if activitynum == pointobj['id']:
                        total_point -= pointobj['score']
                        challenges -= pointobj['score']
                        comments -= pointobj['score']

        elif scoreobj['activity'] == 2:  # img upload
            if scoreobj['deleted'] == False:
                activitynum = scoreobj['activity']
                for pointobj in points:
                    if activitynum == pointobj['id']:
                        total_point += pointobj['score']
                        challenges += pointobj['score']
                        images += pointobj['score']

            else:
                activitynum = scoreobj['activity']
                for pointobj in points:
                    if activitynum == pointobj['id']:
                        total_point -= pointobj['score']
                        challenges -= pointobj['score']
                        images -= pointobj['score']

        elif scoreobj['activity'] == 8:  # weeklyquestion
            if scoreobj['deleted'] == False:
                activitynum = scoreobj['activity']
                for pointobj in points:
                    if activitynum == pointobj['id']:
                        total_point += pointobj['score']
                        weeklyquestion += pointobj['score']
                        results['weeklyquestionid'] = scoreobj['weeklyquestion']

        elif scoreobj['activity'] == 10:  # imaginequestion
            if scoreobj['deleted'] == False:
                activitynum = scoreobj['activity']
                for pointobj in points:
                    if activitynum == pointobj['id']:
                        total_point += pointobj['score']
                        imaginequestion += pointobj['score']
                        results['imaginequestionid'] = scoreobj['imaginequestion']
            else:
                activitynum = scoreobj['activity']
                for pointobj in points:
                    if activitynum == pointobj['id']:
                        total_point -= pointobj['score']
                        imaginequestion -= pointobj['score']

    postcount = BlogPost.objects.exclude(
        id=1).filter(is_Published__exact=True).count()
    readpost = ScoreBoard.objects.filter(
        user=user).filter(activity__exact=9).count()



    # calculate blog points seperately (outside monthly calc)
    blogpoint = ScoringActivities.objects.get(pk=9).score
    blog_points = readpost * blogpoint
    total_point += blog_points

    results['blog_points'] = blog_points
    results['blog_read'] = readpost
    results['blog_postcount'] = postcount
    results['total_point'] = total_point
    results['challenges'] = challenges
    results['likes'] = likes
    results['comments'] = comments
    results['images'] = images
    results['weeklyquestion'] = weeklyquestion
    results['imaginequestion'] = imaginequestion
    
    print(results)
    return results


def positioninleaderboard(user):
    leaderboard = list(ScoreBoard.objects.values(
        'user').annotate(sum=Sum('totalscore')).order_by('-sum'))

    if not ScoreBoard.objects.filter(user=user).values('user').annotate(sum=Sum('totalscore')).order_by('-sum').exists():
        position = dict()
        position['current'] = len(leaderboard)+1
        position['total'] = len(leaderboard)+1
        return position
    else:
        userpoint = list(ScoreBoard.objects.filter(user=user).values(
            'user').annotate(sum=Sum('totalscore')).order_by('-sum'))
        index = leaderboard.index(userpoint[0])
        position = dict()
        position['current'] = index + 1
        position['total'] = len(leaderboard)
        return position


def profile(request, username):
    user = User.objects.get(username=username)

    question = get_object_or_404(Question, is_Published=True)
    imaginequestion = get_object_or_404(ImagineQuestion, is_Published=True)
    scoringactivities = ScoringActivities.objects.all()
    if not user:
        return redirect('main')
    # Create Profile if doesnt exist
    if not Profile.objects.filter(user=user).exists():
        new_profile = Profile(
            user=user,
        )
        new_profile.save()

    profile = Profile.objects.get(user=user)

    results = calculate_score(user)
    position = positioninleaderboard(user)

    context = {
        'username': username,
        'username': user,
        'profile': profile,
        'results': results,
        'question': question,
        'imaginequestion': imaginequestion,
        'position': position,
        'month': NOW,
        'scores': scoringactivities
    }
    return render(request, 'gamification/profile.html', context)


def get_challenge_details(request, slug):
    form = CommentForm
    challenge = get_object_or_404(Challenge, slug=slug)
    return render(request, 'gamification/get-challenge-details.html', {'challenge': challenge, 'form': form})


def show_image(request, slug, image_id):
    form = CommentForm
    # challenges = Challenge.objects.filter(is_Published__exact=True).order_by('-create_date')
    image = get_object_or_404(ImageNominate, pk=image_id)
    challenge = get_object_or_404(Challenge, slug=slug)
    comments = Comment.objects.order_by('-date')
    return render(request, 'gamification/show-image.html', {'image': image, 'challenge': challenge, 'form': form})


def main(request):
    form = CommentForm
    challenges = Challenge.objects.filter(
        is_Published__exact=True).order_by('-create_date')
    comments = Comment.objects.order_by('-date')
    return render(request, 'gamification/main.html', {'challenges': challenges, 'comments': comments, 'form': form})


@login_required
def delete_comment(request):
    if request.method == "POST":
        if request.POST.get("operation") == "delete_comment" and request.is_ajax():
            content_id = int(request.POST.get("content_id"))
            comment = get_object_or_404(Comment, pk=content_id)
            activity = get_object_or_404(ScoringActivities, pk=5)
            score = ScoreBoard(
                user=request.user,
                activity=activity,
                comment=comment,
                deleted=True
            )
            score.save()
            messages.add_message(request, messages.ERROR,
                                 f'<i class="fas fa-error"></i> Yorum silindiği için {activity.score} Puanınız Silindi')

            if comment.image.user != request.user:
                activity = get_object_or_404(
                    ScoringActivities, pk=6)  # Comment by Others
                score = ScoreBoard(
                    user=comment.image.user,
                    activity=activity,
                    deleted=True
                )
                score.save()
            ctx = {"comment_id": comment.id, "message": "Başarıyla Silindi"}
            comment.delete()
            return HttpResponse(json.dumps(ctx), content_type='application/json')


# Like for Challenges
def save_comment(request):
    if request.method == "POST":
        print(request.POST)
        if request.POST.get("operation") == "send_comment" and request.is_ajax():
            form = CommentForm(request.POST)
            content_id = request.POST.get("content_id", None)
            challenge = get_object_or_404(Challenge, pk=content_id)

            if form.is_valid():
                new_comment = Comment(
                    comment=form.cleaned_data['comment'],
                    user=request.user,
                    challenge=challenge
                )
                new_comment.save()

                ctx = {"user": str(request.user), "imgpath": str(request.user.profile.profile_pic.url), "likes_count": challenge.image_likes.count(
                ), "content_id": content_id, "text": form.cleaned_data['comment']}
                return HttpResponse(json.dumps(ctx), content_type='application/json')

# Like for Images


def image_save_comment(request):
    if request.method == "POST":
        if request.POST.get("operation") == "send_comment" and request.is_ajax():
            form = CommentForm(request.POST)
            content_id = request.POST.get("content_id", None)
            image = get_object_or_404(ImageNominate, pk=content_id)
            activity = get_object_or_404(ScoringActivities, pk=5)
            if form.is_valid():
                new_comment = Comment(
                    comment=form.cleaned_data['comment'],
                    user=request.user,
                    image=image
                )
                new_comment.save()
                score = ScoreBoard(
                    user=request.user,
                    activity=activity,
                    comment=new_comment
                )
                score.save()
                if image.user != request.user:
                    activity = get_object_or_404(
                        ScoringActivities, pk=6)  # Comment by Others
                    score = ScoreBoard(
                        user=image.user,
                        activity=activity,
                        comment=new_comment
                    )
                    score.save()
                messages.add_message(request, messages.SUCCESS,
                                     f'<i class="fas fa-trophy"></i> Tebrikler! Yorum yaparak {activity.score} puan kazandın')
                ctx = {"user": str(request.user), "imgpath": str(
                    request.user.profile.profile_pic.url), "content_id": content_id, "text": form.cleaned_data['comment']}
                return HttpResponse(json.dumps(ctx), content_type='application/json')


# Like for Challenges
@login_required
def like(request):
    if request.method == "POST":
        #    print(request.POST['content_id'])
        if request.POST.get("operation") == "like_submit" and request.is_ajax():
            content_id = request.POST.get("content_id", None)
            challenge = get_object_or_404(Challenge, pk=content_id)
            activity = get_object_or_404(ScoringActivities, pk=7)

            # already liked the content
            if challenge.image_likes.filter(id=request.user.id):
                challenge.image_likes.remove(
                    request.user)  # remove user from likes
                # Add Delete Score
                score = ScoreBoard(
                    user=request.user,
                    activity=activity,
                    challenge=challenge,
                    deleted=True
                )
                score.save()
                liked = False

            else:
                challenge.image_likes.add(request.user)
                liked = True
                # Add Score
                score = ScoreBoard(
                    user=request.user,
                    activity=activity,
                    challenge=challenge
                )
                score.save()
                messages.add_message(request, messages.SUCCESS,
                                     f'<i class="fas fa-trophy"></i> Tebrikler! Like ile {activity.score} puan kazandın')
            ctx = {"likes_count": challenge.image_likes.count(
            ), "liked": liked, "content_id": content_id}
            return HttpResponse(json.dumps(ctx), content_type='application/json')


def show_challenge(request, slug):
    form = CommentForm
    challenge = get_object_or_404(Challenge, slug=slug)
    nominees = ImageNominate.objects.filter(challenge=challenge)
    comments = Comment.objects.order_by('-date')
    return render(request, 'gamification/show_challenge.html', {'form': form, 'challenge': challenge, 'nominees': nominees, 'comments': comments})


# like for challenge photos
@login_required
def like_image(request):
    if request.method == "POST":
        if request.POST.get("operation") == "like_submit" and request.is_ajax():
            nominee_id = request.POST.get("content_id", None)
            nominee = get_object_or_404(ImageNominate, pk=nominee_id)
            challenge_id = request.POST.get("challenge_id", None)
            challenge = get_object_or_404(Challenge, pk=challenge_id)
            activity = get_object_or_404(
                ScoringActivities, pk=3)  # Img Like Others
            # already liked the content
            if nominee.image_likes.filter(id=request.user.id):
                # remove user from likes
                nominee.image_likes.remove(request.user)
                liked = False
                # Add Score
                score = ScoreBoard(
                    user=request.user,
                    activity=activity,
                    imagenominate=nominee,
                    deleted=True
                )
                score.save()
                if nominee.user != request.user:
                    activity = get_object_or_404(
                        ScoringActivities, pk=4)  # Img Like Others
                    score = ScoreBoard(
                        user=nominee.user,
                        activity=activity,
                        imagenominate=nominee,
                        deleted=True
                    )
                    score.save()

            else:
                nominee.image_likes.add(request.user)
                liked = True
                # Add Score
                score = ScoreBoard(
                    user=request.user,
                    activity=activity,
                    imagenominate=nominee
                )
                score.save()
                messages.add_message(request, messages.SUCCESS,
                                     f'<i class="fas fa-trophy"></i> Tebrikler! Like ile {activity.score} puan kazandın')
                if nominee.user != request.user:
                    activity = get_object_or_404(
                        ScoringActivities, pk=4)  # Img Like Others
                    score = ScoreBoard(
                        user=nominee.user,
                        activity=activity,
                        imagenominate=nominee
                    )
                    score.save()

                # messages.add_message(request, messages.SUCCESS,
                #              '<i class="fas fa-trophy"></i> Tebrikler! 20 Puan Kazandın')
            ctx = {"likes_count": nominee.image_likes.count(
            ), "liked": liked, "content_id": nominee_id}
            return HttpResponse(json.dumps(ctx), content_type='application/json')


# Delete Image for Challenge
@login_required
def delete_image(request, image_id):
    image = get_object_or_404(ImageNominate, pk=image_id)
    if request.user == image.user:
        activity = get_object_or_404(ScoringActivities, pk=2)
        score = ScoreBoard(
            user=request.user,
            activity=activity,
            imagenominate=image,
            challenge=image.challenge,
            deleted=True
        )
        score.save()
        # score = get_object_or_404(ScoreBoard,user=request.user,imagenominate=image, activity=2)
        # if score.date.year == NOW.year and score.date.month == NOW.month:
        #     score.delete()
        image.delete()
        messages.add_message(request, messages.SUCCESS,
                             '<i class="fas fa-error"></i> Fotoğraf Silindi')
        messages.add_message(request, messages.ERROR,
                             f'<i class="fas fa-error"></i> {activity.score} puanınız silindi')
        return HttpResponseRedirect(reverse('gamification:main'))
    else:
        messages.add_message(request, messages.ERROR,
                             '<i class="fas fa-error"></i> Yetkiniz bulunmuyor, anasayfaya yönlendirildi')
        return HttpResponseRedirect(reverse('gamification:main'))


# Send photo for Challenge
@login_required
def send_challenge_photo(request, challenge_id):
    activity = get_object_or_404(ScoringActivities, pk=2)
    challenge = get_object_or_404(Challenge, pk=challenge_id)

    if request.method == 'POST':
        challenge = get_object_or_404(Challenge, pk=challenge_id)
        activity = get_object_or_404(ScoringActivities, pk=2)

        form = ImageNominateForm(request.POST, request.FILES)
        if form.is_valid():
            new_photo = ImageNominate(
                caption=form.cleaned_data['caption'],
                user=request.user,
                challenge=challenge,
                photo=form.cleaned_data['photo'],
                owner=form.cleaned_data['owner']
            )
            new_photo.save()
            # Add Score
            x = ScoreBoard.objects.filter(
                user=request.user, challenge=challenge, activity=activity, deleted=False)
            total = 0
            for i in x:
                if i.imagenominate != None:
                    total += 1
                    print(i.imagenominate)
            print(total)
            if total < 1:
                score = ScoreBoard(
                    user=request.user,
                    activity=activity,
                    imagenominate=new_photo,
                    challenge=challenge
                )
                print("total 0dan kucuk")
                score.save()
                print('saved')
                messages.add_message(request, messages.SUCCESS,
                                     f'<i class="fas fa-trophy"></i> Tebrikler! Fotoğrafınız yüklendi, {activity.score} puan kazandınız')
            else:
                messages.add_message(request, messages.INFO,
                                     f'<i class="fas fa-trophy"></i> Tebrikler! Fotoğrafınız yüklendi!  Her challenge için maksimum {activity.score} puan kazanabilirsiniz')
            return HttpResponseRedirect(reverse('gamification:show_challenge', args=(challenge.slug,)))
    else:
        form = ImageNominateForm()

    return render(request, 'gamification/send-challenge-photo.html', {'form': form, 'challenge': challenge})

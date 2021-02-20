from django.db.models import Avg, Sum, Max
from yaratici.models import Question, BlogPost, ImagineQuestion, Category, Choices
from yaratici.forms import ChoiceForm
from django.conf import settings
from .forms import CommentForm, ContactForm, ImageNominateForm, ProfileForm
from .models import Challenge, Comment, ImageNominate, Mood, Profile, ScoreBoard, ScoringActivities
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.urls import reverse
from django.shortcuts import get_object_or_404, redirect, render, HttpResponse
from django.contrib import messages
import json
import os
from django.contrib.auth.decorators import login_required
from datetime import datetime,timedelta
from django.core.mail import send_mail, BadHeaderError


NOW = datetime.now()

# Create your views here.
def dailysleep(request):
    NOW = datetime.now()
    if request.method == "POST":
        if not Mood.objects.filter(user=request.user,date__year=NOW.year,date__month=NOW.month,date__day=NOW.day).exists():
            new_mood = Mood(user = request.user,mood = request.POST['rating'])
            new_mood.save()
            activity = get_object_or_404(ScoringActivities,pk=11)
            new_score = ScoreBoard(user=request.user,activity=activity,totalscore=activity.score)
            new_score.save()
            messages.add_message(request, messages.SUCCESS,f'<i class="fas fa-trophy"></i> Bravo! Çocuğunuzun uyku durumunu giriş yaparak günlük olarak takip edebilirsiniz.')
            return redirect(reverse('gamification:profile', kwargs={'username': request.user.username}))
        else:
            currentmood = Mood.objects.filter(user=request.user,date__year=NOW.year,date__month=NOW.month,date__day=NOW.day)[0]
            currentmood.mood = request.POST['rating']
            currentmood.save()
            messages.add_message(request, messages.SUCCESS,
                                     f'<i class="fas fa-trophy"></i> Günlük uyku girişiniz güncellendi.')
           
            return redirect(reverse('gamification:profile', kwargs={'username': request.user.username}))

    else:
        dailymoodentry = Mood.objects.filter(user=request.user,date__year=NOW.year,date__month=NOW.month,date__day=NOW.day)
        #chart data
        labels=[]
        data = []
        queryset = Mood.objects.filter(user=request.user).values_list('date__day','mood').order_by('date')
        for query in queryset:
            labels.append(query[0])
            data.append(query[1])

        context = {
                'todaysmood': dailymoodentry,
                'labels': labels,
                'data':data,
                'random_message':'yes'
            }

        return render(request, 'gamification/dailysleep.html', context)


def leaderboard(request):
    NOW = datetime.now()
    # update_scoreboard_points() #use only when points change
    winnerlst = list()
    place = 1
    top213 = []
    restlst = list()
    leaderboard = ScoreBoard.objects.exclude(user_id__exact=3).filter(date__month=NOW.month).values('user').annotate(
        sum=Sum('totalscore')).order_by('-sum')
    print(leaderboard)

    if len(leaderboard) >= 3:

        for player in leaderboard[:3]:
            currentuser = get_object_or_404(User, pk=player['user'])
            
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

        rest = ScoreBoard.objects.exclude(user_id__exact=3).filter(date__month=NOW.month).values('user').annotate(
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

# only use when point list is changed
def update_scoreboard_points():
    NOW = datetime.now()
    points = ScoringActivities.objects.values('id', 'score')
    scoreboard = ScoreBoard.objects.filter(date__month=NOW.month)
    for scoreobj in scoreboard:
        if scoreobj.deleted == False:
            activitynum = scoreobj.activity.id
            print(activitynum)
            for pointobj in points:
                    if activitynum == pointobj['id']:
                        scoreobj.totalscore = pointobj['score']
                        scoreobj.save()
        else:
            activitynum = scoreobj.activity.id
            for pointobj in points:
                    if activitynum == pointobj['id']:
                        scoreobj.totalscore = pointobj['score'] * -1
                        scoreobj.save()


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
                        
        elif scoreobj['activity'] == 11:  # dailysleep
            if scoreobj['deleted'] == False:
                activitynum = scoreobj['activity']
                for pointobj in points:
                    if activitynum == pointobj['id']:
                        total_point += pointobj['score']
             

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
    
    return results


def positioninleaderboard(user):
    NOW = datetime.now()
    leaderboard = list(ScoreBoard.objects.exclude(user_id__exact=3).filter(date__month=NOW.month).values(
        'user').annotate(sum=Sum('totalscore')).order_by('-sum'))

    if not ScoreBoard.objects.filter(user=user).values('user').annotate(sum=Sum('totalscore')).order_by('-sum').exists():
        position = dict()
        position['current'] = len(leaderboard)+1
        position['total'] = len(leaderboard)+1
        return position
    else:
        if user == User.objects.get(pk=3):
            
            position = dict()
            position['current'] = '-'
            position['total'] = len(leaderboard)
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
    NOW = datetime.now()
    user = User.objects.get(username=username)
    question = get_object_or_404(Question, is_Published=True)
    imaginequestion = get_object_or_404(ImagineQuestion, is_Published=True)
    scoringactivities = ScoringActivities.objects.all()
    def check_daily_mood():
        if request.user.is_authenticated:
            if Mood.objects.filter(user=request.user,date__year=NOW.year,date__month=NOW.month,date__day=NOW.day).exists():
                dailymoodentry = Mood.objects.filter(user=request.user,date__year=NOW.year,date__month=NOW.month,date__day=NOW.day)[0]
                print(dailymoodentry)
                return dailymoodentry
            
        
    # profil yoksa profil yaratır
    if not user:
        return redirect('main')
    # Create Profile if doesnt exist
    if not Profile.objects.filter(user=user).exists():
        new_profile = Profile(user=user,)
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
        'scores': scoringactivities,
        'dailymood': check_daily_mood()
    }
    return render(request, 'gamification/profile.html', context)

@login_required
def redirecttouserprofile(request):
    return HttpResponseRedirect(reverse('gamification:profile', args=(request.user.username,)))

#######👆👆PROFILE👆👆################################

#ID5-6######## YORUM SİLME HEM CHALLENGE HEM DE FOTOĞRAF######### puanlama ok
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
                deleted=True,
                totalscore = activity.score * -1
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
                    deleted=True,
                    totalscore = activity.score * -1
                )
                score.save()
            ctx = {"comment_id": comment.id, "message": "Başarıyla Silindi"}
            comment.delete()
            return HttpResponse(json.dumps(ctx), content_type='application/json')
            
            # delete for challenge details comment screen
        if request.POST.get("operation") == "delete_challenge_comment" and request.is_ajax():
            content_id = int(request.POST.get("content_id"))
            comment = get_object_or_404(Comment, pk=content_id)
            ctx = {"comment_id": comment.id, "message": "Başarıyla Silindi"}
            comment.delete()
            return HttpResponse(json.dumps(ctx), content_type='application/json')


#ID5-6######## CHALLENGE FOTOĞRAF YORUM KAYDET ######### puanlama ok
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
                    comment=new_comment,
                    totalscore = activity.score
                )
                score.save()
                if image.user != request.user:
                    activity = get_object_or_404(
                        ScoringActivities, pk=6)  # Comment by Others
                    score = ScoreBoard(
                        user=image.user,
                        activity=activity,
                        comment=new_comment,
                        totalscore = activity.score
                    )
                    score.save()
                messages.add_message(request, messages.SUCCESS,
                                     f'<i class="fas fa-trophy"></i> Tebrikler! Yorum yaparak {activity.score} puan kazandın')
                ctx = {"user": str(request.user), "imgpath": str(
                    request.user.profile.profile_pic.url), "content_id": content_id, "text": form.cleaned_data['comment']}
                return HttpResponse(json.dumps(ctx), content_type='application/json')


#ID3-4######## CHALLENGE FOTOĞRAF LİKE ######### PUANLAMA OK
@login_required
def like_image(request):
    if request.method == "POST":
        if request.POST.get("operation") == "like_submit" and request.is_ajax():
            nominee_id = request.POST.get("content_id", None)
            nominee = get_object_or_404(ImageNominate, pk=nominee_id)
            challenge_id = request.POST.get("challenge_id", None)
            challenge = get_object_or_404(Challenge, pk=challenge_id)
            activity = get_object_or_404(
                ScoringActivities, pk=3) 
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
                    deleted=True,
                    totalscore = activity.score * -1
                )
                score.save()
                if nominee.user != request.user:
                    activity = get_object_or_404(
                        ScoringActivities, pk=4)  # Img Like Others
                    score = ScoreBoard(
                        user=nominee.user,
                        activity=activity,
                        imagenominate=nominee,
                        deleted=True,
                        totalscore = activity.score * -1
                    )
                    score.save()

            else:
                nominee.image_likes.add(request.user)
                liked = True
                # Add Score
                activity = get_object_or_404(
                ScoringActivities, pk=3)
                score = ScoreBoard(
                    user=request.user,
                    activity=activity,
                    imagenominate=nominee,
                    totalscore = activity.score
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
                        imagenominate=nominee,
                        totalscore = activity.score
                    )
                    score.save()

                # messages.add_message(request, messages.SUCCESS,
                #              '<i class="fas fa-trophy"></i> Tebrikler! 20 Puan Kazandın')
            ctx = {"likes_count": nominee.image_likes.count(
            ), "liked": liked, "content_id": nominee_id}
            return HttpResponse(json.dumps(ctx), content_type='application/json')


######### CHALLENGE FOTOĞRAF SİLME ######### PUANLAMA OK
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
            deleted=True,
            totalscore = activity.score * -1
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


#ID2######## CHALLENGE FOTOĞRAF GÖNDERİMİ ######### puanlama ok
@login_required
def send_challenge_photo(request, challenge_id):
    activity = get_object_or_404(ScoringActivities, pk=2)
    challenge = get_object_or_404(Challenge, pk=challenge_id)
    upload_count = ScoreBoard.objects.filter(user=request.user, challenge=challenge, activity=activity).count() % 2

    def check_uploaded_photo():
        uploaded_photo = ImageNominate.objects.filter(user=request.user, challenge=challenge)
        if uploaded_photo.exists:
            return uploaded_photo
        else:
            return "nophoto"
 

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
            
            score = ScoreBoard(
                user=request.user,
                activity=activity,
                imagenominate=new_photo,
                challenge=challenge,
                totalscore = activity.score
            )
            score.save()
            messages.add_message(request, messages.SUCCESS,
                                    f'<i class="fas fa-trophy"></i> Tebrikler! Fotoğrafınız yüklendi, {activity.score} puan kazandınız')
            return HttpResponseRedirect(reverse('gamification:show_challenge', args=(challenge.slug,)))
    else:
        form = ImageNominateForm()

    return render(request, 'gamification/send-challenge-photo.html', {'form': form, 'challenge': challenge,'upload_count':upload_count,'upphoto':check_uploaded_photo})


######### KATILAN FOTOĞRAF GÖSTERİM SAYFASI #########
def show_image(request, slug, image_id):
    form = CommentForm
    # challenges = Challenge.objects.filter(is_Published__exact=True).order_by('-create_date')
    image = get_object_or_404(ImageNominate, pk=image_id)
    challenge = get_object_or_404(Challenge, slug=slug)
    comments = Comment.objects.order_by('-date')
    return render(request, 'gamification/show-image.html', {'image': image, 'challenge': challenge, 'form': form})


######### CHALLENGE' KATILAN FOTOĞRAFLAR SAYFASI ######### 
def show_challenge(request, slug):
    form = CommentForm
    challenge = get_object_or_404(Challenge, slug=slug)
    nominees = ImageNominate.objects.filter(challenge=challenge)
    comments = Comment.objects.order_by('-date')
    return render(request, 'gamification/show_challenge.html', {'form': form, 'challenge': challenge, 'nominees': nominees, 'comments': comments})


######### CHALLENGE DETAY SAYFASI ######### puanlama yok
def get_challenge_details(request, slug):
    form = CommentForm
    challenge = get_object_or_404(Challenge, slug=slug)
    return render(request, 'gamification/get-challenge-details.html', {'challenge': challenge, 'form': form})


######### CHALLENGE ANA ETKİNLİK YORUM ######### puanlama yok
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


#ID7######## CHALLENGE ANA ETKİNLİK İÇİN LİKE ######### puanlama ok
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
                    deleted=True,
                    totalscore = activity.score * -1
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
                    challenge=challenge,
                    totalscore = activity.score
                )
                score.save()
                messages.add_message(request, messages.SUCCESS,
                                     f'<i class="fas fa-trophy"></i> Tebrikler! Like ile {activity.score} puan kazandın')
            ctx = {"likes_count": challenge.image_likes.count(
            ), "liked": liked, "content_id": content_id}
            return HttpResponse(json.dumps(ctx), content_type='application/json')


######### GAMIFICATION ANASAYFA #########
def main(request):
    form = CommentForm
    challenges = Challenge.objects.filter(
        is_Published__exact=True).order_by('-create_date')
    comments = Comment.objects.order_by('-date')
    return render(request, 'gamification/main.html', {'challenges': challenges, 'comments': comments, 'form': form})


#ID8######## HAFTALIK SORU ######### PUANLAMA OK
def get_question(request):
    form = ChoiceForm()
    question = get_object_or_404(Question, is_Published=True)
    posts = BlogPost.objects.exclude(id=1).filter(is_Published__exact=True).order_by('-create_date')
    sidebar_posts = BlogPost.objects.exclude(id=1).filter(is_Published__exact=True).order_by('-create_date')[:3]
    dates = BlogPost.objects.dates('create_date','month')
    years = [i.year for i in dates]
    categories = Category.objects.all()


    if request.method == 'POST':
        if request.COOKIES.get('answer_status') == 'yes' and request.COOKIES.get('question_id') == str(question.id) and request.COOKIES.get("question_username")==request.user.username :
            messages.add_message(request, messages.SUCCESS, 'Anketi daha önce yanıtladınız, güncel sonuçları aşağıda görebilirsiniz')
            print('already answered')
            return redirect('yaratici:question_results', question_id= question.id)
        # print(request.POST)
        if 'response' not in request.POST:
            messages.add_message(request, messages.WARNING, 'Sonuçları görmek için öncesinde lütfen seçim yapınız')
            print('no selection')
            return redirect('yaratici:get_question')
        else:
            print(f"selectedchoice: {request.POST['response']}")
            messages.add_message(request, messages.WARNING, 'Ankete katılımınız için teşekkürler, güncel sonuçları aşağıda görebilirsiniz')
            choice_object = get_object_or_404(Choices,choice=request.POST['response'])
            choice_object.counter +=1
            choice_object.save()

            #add Score
            activity = get_object_or_404(ScoringActivities,pk=8) # Comment by Others

            if request.user.is_authenticated:
                if not ScoreBoard.objects.filter(user=request.user).filter(weeklyquestion=question).exists():
                    print('yes')
                    score = ScoreBoard(
                        user=request.user,
                        activity=activity,
                        weeklyquestion = question,
                        totalscore = activity.score
                    )
                    score.save()      
                
            response= redirect('yaratici:question_results', question_id= question.id)
            response.set_cookie('answer_status','yes',max_age=604800)
            response.set_cookie('question_id',question.id,max_age=604800)
            response.set_cookie('question_username',request.user.username,max_age=604800)
            return response

    return render(request, 'gamification/showdailyquestion.html', {'question': question, 'form': form, 'posts': posts,'sidebarposts':sidebar_posts,'years':set(years),'categories':categories})

######### HAYALGÜCÜ SORUSU #########
def imaginequestion(request):

    form = CommentForm()
    imaginequestion = get_object_or_404(ImagineQuestion, is_Published=True)
    
    posts = BlogPost.objects.exclude(id=1).filter(is_Published__exact=True).order_by('-create_date')
    sidebar_posts = BlogPost.objects.exclude(id=1).filter(is_Published__exact=True).order_by('-create_date')[:3]
    dates = BlogPost.objects.dates('create_date','month')
    years = [i.year for i in dates]
    categories = Category.objects.all()

    return render(request, 'gamification/hayalgucu.html', {'form':form, 'question': imaginequestion, 'posts': posts,'sidebarposts':sidebar_posts,'years':set(years),'categories':categories})

######### CONTACT FORM #########
def contact_form(request):

    form = ContactForm()
    # update_scoreboard_points()
    if request.method == "POST":
        print(request.POST)
        form = ContactForm(request.POST)
        if form.is_valid():
            isim = form.cleaned_data["İsminiz"]
            email = form.cleaned_data["Email"]
            mesaj = form.cleaned_data["Mesajınız"]
            subject = f"{isim}'den mesaj var"
            messagetext = f"{isim} kişisinden gelen mesaj: {mesaj}\n Email Adresi: \n{email}"
            sender = "erdemdur.mailer@gmail.com"
            recipients = ['berdushwile@gmail.com', 'yaraticicocugum@gmail.com']
            try:
                send_mail(subject, messagetext, sender, recipients)            
            except:
                print("errorrr"),
                messages.add_message(request, messages.ERROR,
                                     f'Bir hata oluştu, daha sonra tekrar deneyin')
                return redirect('gamification:main')
            else:
                messages.add_message(request, messages.SUCCESS,
                                     f'<i class="fas fa-trophy"></i> Mesajını aldık, en kısa sürede dönüş yapacağız')
                return redirect('gamification:main')

            


    else:
        form = ContactForm()
        context = {
            'form': form,
        }
        return render(request, 'gamification/contact-form.html', context)

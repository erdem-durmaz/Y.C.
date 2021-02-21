from gamification.models import Comment
from gamification.forms import CommentForm
from gamification.models import ScoreBoard, ScoringActivities
from .models import BlogPost, Category, Challange, ImagineQuestion, Question,Choices
from .forms import ChoiceForm
from django.shortcuts import get_object_or_404, redirect, render, HttpResponse
from django.contrib import messages
from django.urls import reverse
import json
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.


def landing_page(request):
    return render(request, 'yaratici/landing.html')

def cerez(request):
    posts = BlogPost.objects.exclude(id=1).filter(is_Published__exact=True).order_by('-publish_date')
    sidebar_posts = BlogPost.objects.exclude(id=1).filter(is_Published__exact=True).order_by('-publish_date')[:3]
    dates = BlogPost.objects.dates('create_date','month')
    years = [i.year for i in dates]
    categories = Category.objects.all()

    return render(request, 'yaratici/cerez.html', {'posts': posts,'sidebarposts':sidebar_posts,'years':set(years),'categories':categories})


def home(request):
    posts = BlogPost.objects.exclude(id=1).filter(is_Published__exact=True).order_by('-publish_date')[:3]
    challanges = Challange.objects.filter(is_Published__exact=True).order_by('-create_date')[:3]
    kimim = BlogPost.objects.get(slug__iexact="ben-kimim")
    return render(request, 'yaratici/home.html', {'kimim': kimim, 'posts': posts,'challanges': challanges})


def get_read_posts(request):
    if request.user.is_authenticated:
            readpostids = ScoreBoard.objects.filter(user=request.user).filter(activity__exact=9)
            print(readpostids)
            return readpostids
    else:
        return None
    

def posts(request):
    posts = BlogPost.objects.exclude(id=1).filter(is_Published__exact=True).order_by('-publish_date')
    sidebar_posts = BlogPost.objects.exclude(id=1).filter(is_Published__exact=True).order_by('-publish_date')[:3]
    dates = BlogPost.objects.dates('create_date','month')
    years = [i.year for i in dates]
    categories = Category.objects.all()
    readposts= get_read_posts(request)

    page = request.GET.get('page', 1)

    paginator = Paginator(posts, 10)
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)
    
    
    
    return render(request, 'yaratici/posts.html', {'users':users,'posts': posts,'sidebarposts':sidebar_posts,'years':set(years),'categories':categories,'readposts':readposts})

def posts_byyear(request,year):
    posts = BlogPost.objects.exclude(id=1).filter(is_Published__exact=True).filter(create_date__year=str(year)).order_by('-publish_date')
    sidebar_posts = BlogPost.objects.exclude(id=1).filter(is_Published__exact=True).order_by('-publish_date')[:3]
    dates = BlogPost.objects.dates('create_date','month')
    years = [i.year for i in dates]
    categories = Category.objects.all()

    page = request.GET.get('page', 1)

    paginator = Paginator(posts, 10)
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)
    
    return render(request, 'yaratici/posts.html', {'users':users,'posts': posts,'sidebarposts':sidebar_posts,'years':set(years),'categories':categories,'year':year })

def posts_bytag(request,slug):
    print(slug)
    category = Category.objects.get(slug=slug)
    posts = BlogPost.objects.exclude(id=1).filter(is_Published__exact=True).filter(category__exact=category).order_by('-publish_date')
    sidebar_posts = BlogPost.objects.exclude(id=1).filter(is_Published__exact=True).order_by('-publish_date')[:3]
    dates = BlogPost.objects.dates('create_date','month')
    years = [i.year for i in dates]
    categories = Category.objects.all()

    page = request.GET.get('page', 1)

    paginator = Paginator(posts, 10)
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)
        
    return render(request, 'yaratici/posts.html', {'users':users,'posts': posts,'sidebarposts':sidebar_posts,'years':set(years),'categories':categories,'category':category})

# ID9 READ POST ## PUANLAMA OK
def show_post(request, slug):
    posts = BlogPost.objects.exclude(id=1).filter(is_Published__exact=True).order_by('-publish_date')[:10]
    sidebar_posts = BlogPost.objects.exclude(id=1).filter(is_Published__exact=True).order_by('-publish_date')[:3]
    post = get_object_or_404(BlogPost, slug=slug)
    dates = BlogPost.objects.dates('create_date','month')
    years = [i.year for i in dates]
    categories = Category.objects.all()

    #add Score
    activity = get_object_or_404(ScoringActivities,pk=9) # Blog Read
   
   
    if request.user.is_authenticated:
         if not ScoreBoard.objects.filter(user=request.user).filter(blogpost=post).exists():
            score = ScoreBoard(
            user=request.user,
            activity=activity,
            blogpost = post,
            totalscore = activity.score
        )
            score.save()      

    return render(request, 'yaratici/post.html', {'post': post, 'posts': posts,'sidebarposts':sidebar_posts,'years':set(years),'categories':categories})

def calc_percentage(x,y):
    return x/y*100

def question_results(request,question_id):
    question = get_object_or_404(Question,pk=question_id)
    totalvotes = 0
    dict = {}
    
    for choice in question.choices_set.all():
        totalvotes += choice.counter

    for choice in question.choices_set.all():
        perc = int(calc_percentage(choice.counter,totalvotes))
        dict[choice.choice] = perc
    print(dict)

    return render(request, 'yaratici/question-results.html', {'question': question, 'dict':dict})


def delete_comment(request):
    if request.method =="POST":
        if request.POST.get("operation") == "delete_comment" and request.is_ajax():
            content_id = int(request.POST.get("content_id"))
            comment = get_object_or_404(Comment,pk=content_id)
            activity = get_object_or_404(ScoringActivities,pk=10)
            score = ScoreBoard.objects.filter(user=request.user).filter(comment=comment)
            score.delete()
            messages.add_message(request, messages.ERROR,
                                 f'<i class="fas fa-error"></i> Yorum silindiği için {activity.score} Puanınız Silindi')
                 
            ctx={"comment_id":comment.id,"message":"Başarıyla Silindi"}
            comment.delete()
            return HttpResponse(json.dumps(ctx), content_type='application/json')

# ID 10 Comment Save for ImagineQuestion PUANLAMA OK
def imaginequestion_save_comment(request):
    if request.method =="POST":
        print(request.POST)
        if request.POST.get("operation") == "send_comment" and request.is_ajax():
            form = CommentForm(request.POST)
            content_id=request.POST.get("content_id",None)
            imaginequestion=get_object_or_404(ImagineQuestion,pk=content_id)
            
            
            if form.is_valid():
                new_comment = Comment(
                    comment = form.cleaned_data['comment'],
                    user = request.user,
                    imaginequestion = imaginequestion
                    )
                new_comment.save()

                #add Score
                activity = get_object_or_404(ScoringActivities,pk=10) # Comment by Others
                if request.user.is_authenticated:
                    if not ScoreBoard.objects.filter(user=request.user).filter(imaginequestion = imaginequestion).exists():
                        score = ScoreBoard(
                        user=request.user,
                        activity=activity,
                        comment = new_comment,
                        imaginequestion = imaginequestion,
                        totalscore = activity.score
                        )
                        score.save()
                        messages.add_message(request, messages.SUCCESS,
                                        f'<i class="fas fa-success"></i> Tebrikler Yorumunuz için {activity.score} Puan kazandınız!')
                

                ctx={"user":str(request.user),"imgpath":str(request.user.profile.profile_pic.url),"content_id":content_id,"text":form.cleaned_data['comment']}
                return HttpResponse(json.dumps(ctx), content_type='application/json')


def imaginequestion(request):

    form = CommentForm()
    imaginequestion = get_object_or_404(ImagineQuestion, is_Published=True)
    print(imaginequestion)
    posts = BlogPost.objects.exclude(id=1).filter(is_Published__exact=True).order_by('-publish_date')
    sidebar_posts = BlogPost.objects.exclude(id=1).filter(is_Published__exact=True).order_by('-publish_date')[:3]
    dates = BlogPost.objects.dates('create_date','month')
    years = [i.year for i in dates]
    categories = Category.objects.all()

    return render(request, 'yaratici/hayalgucu.html', {'form':form, 'question': imaginequestion, 'posts': posts,'sidebarposts':sidebar_posts,'years':set(years),'categories':categories})


def get_question(request):
    form = ChoiceForm()
    question = get_object_or_404(Question, is_Published=True)
    posts = BlogPost.objects.exclude(id=1).filter(is_Published__exact=True).order_by('-publish_date')
    sidebar_posts = BlogPost.objects.exclude(id=1).filter(is_Published__exact=True).order_by('-publish_date')[:3]
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
                        totalscore = ScoringActivities.objects.get(pk=8).score
                    )
                    score.save()      
                
            response= redirect('yaratici:question_results', question_id= question.id)
            response.set_cookie('answer_status','yes',max_age=604800)
            response.set_cookie('question_id',question.id,max_age=604800)
            response.set_cookie('question_username',request.user.username,max_age=604800)
            return response

    return render(request, 'yaratici/show-question.html', {'question': question, 'form': form, 'posts': posts,'sidebarposts':sidebar_posts,'years':set(years),'categories':categories})



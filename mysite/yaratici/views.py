from .models import BlogPost, Category, Challange, Question,Choices
from .forms import ChoiceForm
from django.shortcuts import get_object_or_404, redirect, render, HttpResponse
from django.contrib import messages
from django.urls import reverse

# Create your views here.


def landing_page(request):
    return render(request, 'yaratici/landing.html')

def cerez(request):
    posts = BlogPost.objects.exclude(id=1).filter(is_Published__exact=True).order_by('-create_date')
    return render(request, 'yaratici/cerez.html', {'posts': posts})

def home(request):
    posts = BlogPost.objects.exclude(id=1).filter(is_Published__exact=True).order_by('-create_date')[:3]
    challanges = Challange.objects.filter(is_Published__exact=True).order_by('-create_date')[:3]
    kimim = BlogPost.objects.get(slug__iexact="ben-kimim")
    return render(request, 'yaratici/home.html', {'kimim': kimim, 'posts': posts,'challanges': challanges})


def posts(request):
    posts = BlogPost.objects.exclude(id=1).filter(is_Published__exact=True).order_by('-create_date')
    sidebar_posts = BlogPost.objects.exclude(id=1).filter(is_Published__exact=True).order_by('-create_date')[:3]
    dates = BlogPost.objects.dates('create_date','month')
    years = [i.year for i in dates]
    categories = Category.objects.all()

    return render(request, 'yaratici/posts.html', {'posts': posts,'sidebarposts':sidebar_posts,'years':set(years),'categories':categories})

def posts_byyear(request,year):
    posts = BlogPost.objects.exclude(id=1).filter(is_Published__exact=True).filter(create_date__year=str(year)).order_by('-create_date')
    sidebar_posts = BlogPost.objects.exclude(id=1).filter(is_Published__exact=True).order_by('-create_date')[:3]
    dates = BlogPost.objects.dates('create_date','month')
    years = [i.year for i in dates]
    categories = Category.objects.all()
    return render(request, 'yaratici/posts.html', {'posts': posts,'sidebarposts':sidebar_posts,'years':set(years),'categories':categories})

def posts_bytag(request,slug):
    print(slug)
    category = Category.objects.get(slug=slug)
    posts = BlogPost.objects.exclude(id=1).filter(is_Published__exact=True).filter(category__exact=category).order_by('-create_date')
    sidebar_posts = BlogPost.objects.exclude(id=1).filter(is_Published__exact=True).order_by('-create_date')[:3]
    dates = BlogPost.objects.dates('create_date','month')
    years = [i.year for i in dates]
    categories = Category.objects.all()
    return render(request, 'yaratici/posts.html', {'posts': posts,'sidebarposts':sidebar_posts,'years':set(years),'categories':categories})


def show_post(request, slug):
    posts = BlogPost.objects.exclude(id=1).filter(is_Published__exact=True).order_by('-create_date')[:10]
    sidebar_posts = BlogPost.objects.exclude(id=1).filter(is_Published__exact=True).order_by('-create_date')[:3]
    post = get_object_or_404(BlogPost, slug=slug)
    return render(request, 'yaratici/post.html', {'post': post, 'posts': posts,'sidebarposts':sidebar_posts})

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



def get_question(request):
    form = ChoiceForm()
    question = get_object_or_404(Question, is_Published=True)
    posts = BlogPost.objects.exclude(id=1).filter(is_Published__exact=True).order_by('-create_date')[:10]

    if request.method == 'POST':
        if request.COOKIES.get('answer_status') == 'yes' and request.COOKIES.get('question_id') == str(question.id):
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
            print(choice_object.counter)
            choice_object.save()
            
            response= redirect('yaratici:question_results', question_id= question.id)
            response.set_cookie('answer_status','yes',max_age=604800)
            response.set_cookie('question_id',question.id,max_age=604800)
            return response

    return render(request, 'yaratici/show-question.html', {'question': question, 'form': form, 'posts': posts})



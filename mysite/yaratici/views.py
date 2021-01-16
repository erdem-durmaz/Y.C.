from .models import BlogPost, Question,Choices
from .forms import ChoiceForm
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.urls import reverse

# Create your views here.


def landing_page(request):
    return render(request, 'yaratici/landing.html')


def home(request):
    posts = BlogPost.objects.order_by('-create_date')[:3]
    print(posts)
    kimim = BlogPost.objects.get(slug__iexact="ben-kimim")
    return render(request, 'yaratici/home.html', {'kimim': kimim, 'posts': posts})


def posts(request):
    posts = BlogPost.objects.all().exclude(id=1).order_by('-create_date')
    return render(request, 'yaratici/posts.html', {'posts': posts})


def show_post(request, slug):
    posts = BlogPost.objects.all().exclude(id=1).order_by('-create_date')[:10]
    post = get_object_or_404(BlogPost, slug=slug)
    return render(request, 'yaratici/post.html', {'post': post, 'posts': posts})

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

    if request.method == 'POST':
        print(request.POST)
        if 'response' not in request.POST:
            messages.add_message(request, messages.WARNING, 'You Did Not Select Any Answer')
            print('no selection')
        else:
            print(f"selectedchoice: {request.POST['response']}")
            choice_object = get_object_or_404(Choices,choice=request.POST['response'])
            
            choice_object.counter +=1
            print(choice_object.counter)
            choice_object.save()
            
        return redirect('yaratici:question_results', question_id= question.id)

    return render(request, 'yaratici/show-question.html', {'question': question, 'form': form})



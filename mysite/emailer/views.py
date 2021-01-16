
from django.contrib import messages
from django.urls import reverse
from django.shortcuts import get_object_or_404, render, HttpResponseRedirect, get_list_or_404
from .forms import QuestionForm, UploadFileForm
from .models import Email, Quiz, Question, Answers, Choices
from django import forms
import requests
import random
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

# Create your views here.


def add_message(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        print(request.POST, request.FILES)
        if form.is_valid():
            new_email = Email(
                name=form.cleaned_data['name'],
                template=form.cleaned_data['template'],
                photo=form.cleaned_data['photo'],
                email=form.cleaned_data['email'],
                message=form.cleaned_data['message']
            )
            new_email.save()
            print('saved')
    else:
        form = UploadFileForm()
    return render(request, 'emailer/home.html', {'form': form})


def show_emails(request):
    emails = Email.objects.all()
    return render(request, 'emailer/show_emails.html', {'emails': emails})


def delete_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz,pk=quiz_id)
    quiz.delete()
    return HttpResponseRedirect(reverse('emailer:start'))


def create_quiz(request):
    random_nr = random.randint(3,10)
    data = requests.get(f"https://opentdb.com/api.php?amount={random_nr}&type=multiple").json()
    questions = data['results']
    new_quiz = Quiz(
        name=questions[0]['category'],
        about=questions[0]['difficulty'],
        instructions=questions[0]['type'],
        quizmaster=request.user
    )
    new_quiz.save()

    for question in questions:
        new_question = Question(
            quiz=new_quiz,
            question=question['question'],
            correct=question['correct_answer']
        )
        new_question.save()

        choices = question['incorrect_answers']
        choices.append(question['correct_answer'])
        for choice in choices:
            new_choice = Choices(
                quiz=new_quiz,
                question=new_question,
                answer=choice,
                comment = 'Comment Goes Here|' + question['correct_answer']
            )
            new_choice.save()

    return HttpResponseRedirect(reverse('emailer:start'))

@login_required()
def start(request):
    # for testing
    # if request.user.is_anonymous:
    #     print('yes')
    #     user = authenticate(request, username='berdushwile', password='948333')
    #     login(request, user)
    #     print('logged in')
    # end

    quiz_list = Quiz.objects.all()
    questions = Question.objects.all()
    return render(request, 'emailer/show-quiz.html', {'quiz_list': quiz_list, 'questions': questions})


def score(request, quiz_id):
    user = request.user
    quiz = get_object_or_404(Quiz, pk=quiz_id)
    answers = Answers.objects.filter(quiz=quiz, user=user)
    list_obj = []
    lenofquestions = len(list_obj)
    score = 0
    for answer in answers:
        dictionary = dict()
        print(answer.question)
        dictionary['question'] = answer.question
        dictionary['submission'] = answer.response
        dictionary['comment'] = answer.comment
        dictionary['correct'] = answer.correct_choice
        if answer.response == answer.correct_choice:
            score += 1
            dictionary['result'] = "Correct"
        else:
            dictionary['result'] = "False"
        list_obj.append(dictionary)
        

    return render(request, 'emailer/scores.html', {'quiz_object': quiz, 'answers': answers, 'list_obj': list_obj, 'score': score, 'len': lenofquestions})


def conduct_quiz(request, quiz_id):
    user = request.user
    quiz = get_object_or_404(Quiz, pk=quiz_id)
    # question = get_object_or_404(Question, pk=quiz_id)
    questions = Question.objects.filter(quiz=quiz)
    # choices =question.choices_set.filter()

    if request.method == 'POST':
        print(request.POST)
        if 'response' not in request.POST :
            messages.add_message(request, messages.WARNING,
                                 'You Did Not Select New Choice')
            print('no selection')
        else:
            question = get_object_or_404(
                Question, pk=int(request.POST['question_id']))
            choice = question.choices_set.filter(
                answer__contains=request.POST['response']).first()
            print(f'comment:{choice.comment}')
            try:
                answer_object = get_object_or_404(
                    Answers, user=user, quiz=quiz, question=question)
            except:
                new_answer = Answers(
                    user=user,
                    quiz=quiz,
                    question=question,
                    correct_choice=question.correct,
                    response=request.POST['response'],
                    comment=choice.comment
                )
                new_answer.save()
            else:
                answer_object.response = request.POST['response']
                answer_object.save()
                # print(answer_object)

    # 'question_object':question  'choices':choices,
    return render(request, 'emailer/take-quiz.html', {'quiz_object': quiz, 'questions': questions})

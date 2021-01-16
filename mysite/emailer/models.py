from django.db import models
from django.db.models.fields.related import OneToOneField
from django.contrib.auth.models import User
from datetime import timedelta 

# Create your models here.

class Email(models.Model):
    namee = models.CharField(max_length=255)
    template = models.DecimalField(max_digits=5, decimal_places=2)
    photo = models.ImageField(upload_to='email_img')
    create_date = models.DateField(auto_now_add=True)
    email = models.EmailField()
    message = models.TextField()

class Quiz(models.Model):
    name = models.CharField(max_length = 50)
    about = models.TextField(max_length= 2000)
    Test_Password = models.CharField(max_length=50,default='')
    quizmaster =   models.ForeignKey(User, on_delete= models.CASCADE)
    instructions = models.TextField(default=' ')
    positive = models.IntegerField(default=3)
    negative = models.IntegerField(default=1)
    duration = models.DurationField(default= timedelta())

    def __str__(self):
            return self.name


class Question(models.Model):
    quiz = models.ForeignKey('Quiz',on_delete=models.CASCADE)
    question = models.CharField(max_length=255)
    photo = models.ImageField(upload_to='email_img', blank=True)
    correct = models.CharField(max_length= 500,blank=True)
    
    
    def __str__(self):
        return self.question


class Choices(models.Model):
    quiz = models.ForeignKey('Quiz',on_delete=models.CASCADE)
    question = models.ForeignKey('Question',on_delete=models.CASCADE)
    answer = models.CharField(max_length = 250)
    is_correct = models.BooleanField(default=False)
    comment = models.CharField(max_length = 500,blank=True)
    def __str__(self):
        return self.answer


class Answers(models.Model):
    user = models.ForeignKey(User, on_delete= models.CASCADE ) 
    quiz = models.ForeignKey('Quiz', on_delete=models.CASCADE)
    question = models.ForeignKey('Question', on_delete=models.CASCADE)
    response = models.CharField(max_length=500, default='')
    correct_choice = models.CharField(max_length=500,blank=True)
    comment = models.CharField(max_length = 500,blank=True)
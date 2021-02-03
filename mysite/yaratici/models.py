from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from ckeditor.fields import RichTextField


# Create your models here.
class Category(models.Model):
    title = models.CharField(max_length=255)
    create_date = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField()

    def __str__(self):
            return self.title


class BlogPost(models.Model):
    user = models.ForeignKey(User, on_delete= models.CASCADE )
    title = models.CharField(max_length=255)
    meta_title = models.CharField(max_length=255)
    meta_tags = models.CharField(max_length=255,blank=True)
    photo = models.ImageField(upload_to='blog_img')
    create_date = models.DateTimeField(auto_now_add=True)
    edit_date = models.DateTimeField(auto_now=True)
    category = models.ForeignKey(Category, on_delete= models.CASCADE,blank=True,null=True )
    is_Published = models.BooleanField(default=False)
    message = RichTextField(blank=True,null=True)
    slug = models.SlugField()
    
    def __str__(self):
            return self.title

    def get_absolute_url(self):
        return reverse('yaratici:show_post', kwargs={'slug':self.slug})



from datetime import timedelta 


class Question(models.Model):
    question = models.CharField(max_length=255)
    blogpost = models.ForeignKey('BlogPost',on_delete=models.PROTECT, blank=True, null=True)
    create_date = models.DateTimeField(auto_now_add=True)
    is_Published = models.BooleanField(default=False)
    
    
    def __str__(self):
        return self.question


class Choices(models.Model):
    question = models.ForeignKey('Question',on_delete=models.CASCADE)
    choice = models.CharField(max_length = 250)
    counter = models.IntegerField(default=0)

    def __str__(self):
        return self.choice

class Challange(models.Model):
    name = models.CharField(max_length = 250)
    description = RichTextField(blank=True,null=True)
    create_date = models.DateTimeField(auto_now_add=True)
    is_Published = models.BooleanField(default=True)
    photo = models.URLField(max_length=250)
    youtube_link = models.CharField(max_length = 500)

    def __str__(self):
        return self.name






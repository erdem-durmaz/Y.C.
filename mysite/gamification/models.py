
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from ckeditor.fields import RichTextField

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,)
    profile_pic = models.ImageField(upload_to='ProfilePicture/',default="default_img.jpg")
    date = models.DateTimeField(auto_now_add=True, null= True)
    description = models.CharField(max_length=200, null=True, blank=True)  

    def __str__(self):
        return self.profile.user

class Challenge(models.Model):
    user = models.ForeignKey(User, on_delete= models.CASCADE )
    title = models.CharField(max_length=255)
    photo = models.ImageField(upload_to='challenge_img')
    create_date = models.DateTimeField(auto_now_add=True)
    edit_date = models.DateTimeField(auto_now=True)
    is_Published = models.BooleanField(default=False)
    message = RichTextField(blank=True,null=True)
    slug = models.SlugField()
    image_likes = models.ManyToManyField( User, blank=True, related_name='likes')


    def __str__(self):
            return self.title

    def get_absolute_url(self):
        return reverse('gamification:show_challenge', kwargs={'slug':self.slug})   

    def like_count(self):
        return self.challenge.image_likes_set.all()

class ImageNominate (models.Model):
    caption = models.CharField(max_length=150, blank=True, verbose_name="Fotoğrafınızın İsmi")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    photo = models.ImageField(upload_to='challenge_img')
    image_likes = models.ManyToManyField( User, blank=True, related_name='photo_likes')

    def __str__(self):
        return self.caption



class Comment (models.Model):
    comment = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE, blank=True, null=True)
    image = models.ForeignKey(ImageNominate, on_delete=models.CASCADE, blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.comment

class ScoreBoard (models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    score = models.IntegerField(default=0)




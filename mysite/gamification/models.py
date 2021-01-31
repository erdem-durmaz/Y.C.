
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from ckeditor.fields import RichTextField

import sys
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,)
    profile_pic = models.ImageField(upload_to='ProfilePicture/',default="default_img.jpg")
    date = models.DateTimeField(auto_now_add=True, null= True)
    description = models.CharField(max_length=200, null=True, blank=True)  

    def __str__(self):
        return self.profile.user
    
    def save(self):
        im = Image.open(self.profile_pic)
        output = BytesIO()
        im = im.resize( (500,500) )
        im.save(output, format='JPEG', quality=50)
        output.seek(0)
        self.profile_pic = InMemoryUploadedFile(output,'ImageField', "%s.jpg" %self.profile_pic.name.split('.')[0], 'image/jpeg', sys.getsizeof(output), None)
        super(Profile,self).save()
        


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

    def save(self):
        im = Image.open(self.photo)
		
        
        if im.width > 2000 and im.height> 2000:
            print('big picturee')
            output = BytesIO()
            half = 0.5
            im = im.resize( [int(half * s) for s in im.size] )
        # im = im.resize( (1000,1000) )
            im.save(output, format='JPEG', quality=50)
            output.seek(0)
            self.photo = InMemoryUploadedFile(output,'ImageField', "%s.jpg" %self.photo.name.split('.')[0], 'image/jpeg', sys.getsizeof(output), None)
            super(Challenge,self).save()
        else:
            output = BytesIO()
            im.save(output, format='JPEG', quality=30)
            output.seek(0)
            self.photo = InMemoryUploadedFile(output,'ImageField', "%s.jpg" %self.photo.name.split('.')[0], 'image/jpeg', sys.getsizeof(output), None)
            super(Challenge,self).save()

class ImageNominate (models.Model):
    caption = models.CharField(max_length=150, blank=True, verbose_name="Fotoğrafınızın İsmi")
    owner = models.CharField(max_length=150, blank=True, verbose_name="Eser Sahibi 😊")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    photo = models.ImageField(upload_to='challenge_img')
    image_likes = models.ManyToManyField( User, blank=True, related_name='photo_likes')

    def __str__(self):
        return self.caption

    def save(self):
        im = Image.open(self.photo)
		
        
        if im.width > 2000 and im.height> 2000:
            print('big picturee')
            output = BytesIO()
            half = 0.5
            im = im.resize( [int(half * s) for s in im.size] )
        # im = im.resize( (1000,1000) )
            im.save(output, format='JPEG', quality=50)
            output.seek(0)
            self.photo = InMemoryUploadedFile(output,'ImageField', "%s.jpg" %self.photo.name.split('.')[0], 'image/jpeg', sys.getsizeof(output), None)
            super(ImageNominate,self).save()
        else:
            output = BytesIO()
            im.save(output, format='JPEG', quality=30)
            output.seek(0)
            self.photo = InMemoryUploadedFile(output,'ImageField', "%s.jpg" %self.photo.name.split('.')[0], 'image/jpeg', sys.getsizeof(output), None)
            super(ImageNominate,self).save()



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



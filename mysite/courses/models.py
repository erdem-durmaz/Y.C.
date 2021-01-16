from django.db import models

# Create your models here.

from django.db import models
import datetime
from django.utils import timezone


class Course(models.Model):
    course_name = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    def __str__(self):
        return self.course_name

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)


class Attendee(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    def __str__(self):
        return self.name



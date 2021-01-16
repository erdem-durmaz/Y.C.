from django.contrib import admin

# Register your models here.

from .models import Quiz, Question, Answers, Choices

admin.site.register(Quiz)
admin.site.register(Question)
admin.site.register(Choices)
admin.site.register(Answers)

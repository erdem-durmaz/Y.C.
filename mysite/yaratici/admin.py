from django.contrib import admin

# Register your models here.

from .models import BlogPost, Question,Choices



class BlogPostAdmin(admin.ModelAdmin):
    list_display =('title','create_date','is_Published','user','edit_date')
    list_filter = ('create_date',)
    list_editable = ('is_Published',)
    search_fields = ('title','slug')
    prepopulated_fields = {"slug": ("title",)}
    list_per_page = 20

class QuestionAdmin(admin.ModelAdmin):
    list_display =('question','is_Published')
    list_editable = ('is_Published',)
    search_fields = ('question',)
    list_per_page = 20

class ChoiceAdmin(admin.ModelAdmin):
    list_display =('choice','question','counter')
    list_per_page = 20


admin.site.register(BlogPost,BlogPostAdmin)
admin.site.register(Question,QuestionAdmin)
admin.site.register(Choices, ChoiceAdmin)

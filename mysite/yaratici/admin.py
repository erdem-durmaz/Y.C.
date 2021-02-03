from django.contrib import admin

# Register your models here.

from .models import BlogPost, Question,Choices, Challange,Category



class BlogPostAdmin(admin.ModelAdmin):
    list_display =('title','create_date','is_Published','category','user','edit_date')
    list_filter = ('create_date','category')
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

class ChallangeAdmin(admin.ModelAdmin):
    list_display =('name','is_Published')
    list_editable = ('is_Published',)

class CategoryAdmin(admin.ModelAdmin):
    list_display =('title','create_date')
    prepopulated_fields = {"slug": ("title",)}
    



admin.site.register(BlogPost,BlogPostAdmin)
admin.site.register(Question,QuestionAdmin)
admin.site.register(Choices, ChoiceAdmin)
admin.site.register(Challange, ChallangeAdmin)
admin.site.register(Category, CategoryAdmin)


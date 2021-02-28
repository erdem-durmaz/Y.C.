from django.contrib import admin

# Register your models here.

from .models import Challenge,Comment, Milk, Mood, ScoreBoard,ImageNominate, ScoringActivities



class ChallengeAdmin(admin.ModelAdmin):
    list_display =('title','create_date','is_Published','user','edit_date')
    list_filter = ('create_date',)
    list_editable = ('is_Published',)
    search_fields = ('title','slug')
    prepopulated_fields = {"slug": ("title",)}
    list_per_page = 20

class CommentAdmin(admin.ModelAdmin):
    list_display =('comment','challenge','user','date')
    list_filter = ('user','challenge',)
    search_fields = ('comment',)
    list_per_page = 20

class ImageNominateAdmin(admin.ModelAdmin):
    list_display =('caption','challenge','user','date')
    list_filter = ('user','challenge',)
    list_per_page = 20

class ScoringActivitiesAdmin(admin.ModelAdmin):
    list_display =('title','id','score',)
    list_editable = ('score',)

class ScoreBoardAdmin(admin.ModelAdmin):
    list_display =('user','activity','totalscore','date')
    list_filter = ('date','user','activity')
    list_per_page = 20
    
class MoodAdmin(admin.ModelAdmin):
    list_display =('user','mood','date')
    list_filter = ('date','user','mood')
    list_per_page = 20

class MilkAdmin(admin.ModelAdmin):
    list_display =('user','drankmilk','date')
    list_filter = ('date','user','drankmilk')
    list_per_page = 20
    



admin.site.register(Challenge,ChallengeAdmin)
admin.site.register(ScoreBoard,ScoreBoardAdmin)
admin.site.register(Comment,CommentAdmin)
admin.site.register(ImageNominate,ImageNominateAdmin)
admin.site.register(ScoringActivities,ScoringActivitiesAdmin)
admin.site.register(Mood, MoodAdmin)
admin.site.register(Milk, MilkAdmin)
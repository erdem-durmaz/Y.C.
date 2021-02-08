from django.contrib import admin

# Register your models here.

from .models import Challenge,Comment, ScoreBoard,ImageNominate, ScoringActivities



class ChallengeAdmin(admin.ModelAdmin):
    list_display =('title','create_date','is_Published','user','edit_date')
    list_filter = ('create_date',)
    list_editable = ('is_Published',)
    search_fields = ('title','slug')
    prepopulated_fields = {"slug": ("title",)}
    list_per_page = 20

class ScoringActivitiesAdmin(admin.ModelAdmin):
    list_display =('title','id','score',)
    list_editable = ('score',)

class ScoreBoardAdmin(admin.ModelAdmin):
    list_display =('user','activity','challenge',)
    list_filter = ('date',)
    



admin.site.register(Challenge,ChallengeAdmin)
admin.site.register(ScoreBoard,ScoreBoardAdmin)
admin.site.register(Comment)
admin.site.register(ImageNominate)
admin.site.register(ScoringActivities,ScoringActivitiesAdmin)

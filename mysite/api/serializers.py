from yaratici.models import BlogPost
from rest_framework import serializers
from gamification.models import Challenge, Comment, ImageNominate, Milk, Mood, Profile, ScoreBoard, ScoringActivities
from django.contrib.auth.models import User


class MilkSerializer(serializers.ModelSerializer):
    # user = serializers.ReadOnlyField(source='user.username')
    class Meta:
        model = Milk
        fields = ['id', 'date', 'drankmilk','user']

class UserSerializer(serializers.ModelSerializer):
    # milks = serializers.PrimaryKeyRelatedField(many=True, queryset=Milk.objects.all())

    class Meta:
        model = User
        fields = ['id', 'username']

class BlogSerializer(serializers.ModelSerializer):
    # milks = serializers.PrimaryKeyRelatedField(many=True, queryset=Milk.objects.all())

    class Meta:
        model = BlogPost
        fields = ['id', 'title','photo','message']
from django.db import models
from django.contrib.auth.models import User
from gamification.models import Challenge,Comment,ImageNominate


class Notif(models.Model):
    recipient = models.ForeignKey(User, on_delete= models.CASCADE )
    unread = models.BooleanField(default=True, blank=False)
    actor_id = models.CharField(max_length=255)
    verb = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    deleted = models.BooleanField(default=False)
    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE, blank=True, null=True)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, blank=True, null=True)
    image = models.ForeignKey(ImageNominate, on_delete=models.CASCADE, blank=True, null=True)
    
    class Meta:
        ordering = ('-timestamp',)
        # speed up notifications count query
        index_together = ('recipient', 'unread')

    def mark_as_read(self):
        if self.unread:
            self.unread = False
            self.save()


    def __str__(self):
        return f"{self.recipient}, {self.actor_id}  {self.verb}"

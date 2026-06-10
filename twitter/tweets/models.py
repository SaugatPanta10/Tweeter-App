from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Tweet(models.Model):
    tweetor = models.ForeignKey(User,on_delete=models.CASCADE, related_name = 'tweets')
    content = models.TextField(max_length=500)
    image = models.FileField(upload_to = 'tweet_files/', blank = True, null = True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.content[:20]}"
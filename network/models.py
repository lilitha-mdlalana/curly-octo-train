from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

class User(AbstractUser):
    pass

class Post(models.Model):
    author = models.ForeignKey(User,on_delete=models.CASCADE)
    message = models.TextField(null=True,blank=False)
    created_at = models.DateTimeField(default=timezone.now)
    no_of_likes = models.IntegerField(default=0)
    
    def __str__(self) -> str:
        return self.message
    
        
    class Meta:
        ordering=['-created_at']
    
class PostLike(models.Model):
    user = models.CharField(max_length=100)
    post_id = models.CharField(max_length=500) 
    
    def __str__(self):
        return self.user
    

class FollowersCount(models.Model):
    follower = models.CharField(max_length=100)
    user = models.CharField(max_length=100)
    
    def __str__(self) -> str:
        return self.user
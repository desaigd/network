from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Post(models.Model):
    postedby =  models.ForeignKey(User, on_delete=models.CASCADE, related_name="postedby")
    content = models.CharField(max_length=200)
    datetime = models.DateTimeField(auto_now_add=True)
    likes = models.IntegerField(default=0)
    
    def __str__(self):
        return f"{self.id} {self.postedby} {self.content} {self.datetime} {self.likes} "


class Follower(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE, default=None, related_name="userfollower")
    follower = models.ForeignKey(User,on_delete=models.CASCADE,default=None, related_name="follower")
    

class Follow(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE, default=None, related_name="userfollow")
    follow = models.ForeignKey(User,on_delete=models.CASCADE, default=None, related_name="follow")


class Like(models.Model):
    likepostid = models.ForeignKey(Post,on_delete=models.CASCADE, related_name="likepostid")
    likedby = models.ForeignKey(User,on_delete=models.CASCADE, related_name="likedby")
    
    def __str__(self):
        return f"{self.likepostid} {self.likedby}"
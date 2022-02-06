from doctest import FAIL_FAST
from importlib.resources import contents
from pyexpat import model
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

    def get_following_users(self):
        """ Return a list of following user for user_"""
        followings_user = []
        for following in self.followings.all():
            followings_user.append(following.user_followed)
        return followings_user


class UserProfile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="profile")
    name = models.CharField(max_length=100, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    about = models.TextField(blank=True, null=True)
    image = models.ImageField(
        default="profile_pics/default.png", upload_to="profile_pics")

    def __str__(self):
        return f"{self.user.username}"


class Post(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="posts")
    content = models.TextField(max_length=400, blank=False)
    date = models.DateTimeField(auto_now_add=True)
    like = models.IntegerField(default=0)
    dislike = models.IntegerField(default=0)
    
    class Meta:
        ordering = ["-date"]

    def __str__(self):
        return f"Post {self.id} made by {self.user} on {self.date.strftime('%d %b %Y %H:%M:%S')}"

    def serialize(self):
        return {
            "id": self.id,
            "user": self.user.username,
            "date": self.date.strftime('%d %b %Y %H:%M:%S'),
            "like": self.like,
            "dislike": self.dislike,
            "content": self.content
        }


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="comments")
    content = models.TextField(max_length=400, blank=False)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-date"]


class Following(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="followings")
    user_followed = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="followers")

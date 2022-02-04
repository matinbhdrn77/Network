from doctest import FAIL_FAST
from importlib.resources import contents
from pyexpat import model
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Post(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="posts")
    content = models.TextField(max_length=400, blank=False)
    date = models.DateTimeField(auto_now_add=True)
    like = models.IntegerField(default=0)

    def __str__(self):
        return f"Post {self.id} made by {self.user} on {self.date.strftime('%d %b %Y %H:%M:%S')}"


class Comment(model.Model):
    user = models.ForeignKey(User)
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

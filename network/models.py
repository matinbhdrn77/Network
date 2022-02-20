from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

    def get_following_users(self):
        """ Return a list of following user for user"""
        followings_user = []
        for following in self.followings.all():
            followings_user.append(following.user_followed)
        return followings_user

    def is_like(self, post):
        return self.user_likes.filter(id=post.id).exists()

    def is_dislike(self, post):
        return self.user_dislikes.filter(id=post.id).exists()


class UserProfile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="profile")
    name = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}"


class Post(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="posts")
    content = models.TextField(max_length=400, blank=False)
    date = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, blank=True, related_name="user_likes")
    dislikes = models.ManyToManyField(
        User, blank=True, related_name="user_dislikes")

    class Meta:
        ordering = ["-date"]

    def __str__(self):
        return f"Post {self.id} made by {self.user} on {self.date.strftime('%d %b %Y %H:%M:%S')}"

    def serialize(self):
        return {
            "id": self.id,
            "user": self.user.username,
            "date": self.date.strftime('%d %b %Y %H:%M:%S'),
            "like": self.likes.all().count(),
            "dislike": self.dislikes.all().count(),
            "content": self.content
        }

    def num_likes(self):
        return self.likes.all().count()

    def num_dislikes(self):
        return self.dislikes.all().count()


class Following(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="followings")
    user_followed = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="followers")

from django import template
from django.shortcuts import get_object_or_404
from ..models import User, Post

register = template.Library()

@register.filter(is_safe=True)
def is_liked(post_id, user_id):
    post=get_object_or_404(Post, id=post_id)
    user=get_object_or_404(User, id=user_id)
    return user.is_like(post)

@register.filter(is_safe=True)
def is_disliked(post_id, user_id):
    post=get_object_or_404(Post, id=post_id)
    user=get_object_or_404(User, id=user_id)
    return user.is_dislike(post)


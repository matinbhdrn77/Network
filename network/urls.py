
from unicodedata import name
from django.urls import path

from . import views

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),

    path("new-post", views.ComposePostView.as_view(), name="new-post"),
    path("user-profile/<int:pk>", views.UserProfileView.as_view(), name="user-profile"),
    path("handle-following/<int:pk>", views.HandleFollowingView.as_view(), name="handle-following"),
    path("following-user-posts", views.FollowingUserPostsView.as_view(), name="following-user-posts"),
    path("edite-form/<int:pk>", views.EditeFormView.as_view(), name="edite-form")
]

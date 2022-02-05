from importlib.resources import contents
import json
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin

# Class Base Views
from django.views import View
from django.views.generic import TemplateView
from django.contrib.auth.views import LoginView

from .models import User, Post


class IndexView(TemplateView):
    template_name = "network/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        posts = Post.objects.all()[:10]
        context["posts"] = posts
        return context


class ComposePostView(LoginRequiredMixin, View):
    def post(self, request):
        data = json.loads(request.body)
        content = data.get("content")
        if content.strip() == "":
            return JsonResponse({"error": "Your post can't be empty!"}, status=400)
        post = Post.objects.create(user=request.user, content=content)
        post.save()
        return JsonResponse(post.serialize(), safe=False)

    # Composing a new post must be via POST
    def get(self, request):
        return JsonResponse({"error": "POST request required."}, status=400)


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

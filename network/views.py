from distutils.debug import DEBUG
import json
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator

# Class Base Views
from django.views import View
from django.views.generic import TemplateView
from django.contrib.auth.views import LoginView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView


from .models import User, Post, UserProfile, Following


class IndexView(TemplateView):
    template_name = "network/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        posts = Post.objects.all()

        # Create page controll
        paginator = Paginator(posts, 10)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context["page_obj"] = page_obj

        return context


class ComposePostView(LoginRequiredMixin, View):
    def post(self, request):
        content = request.POST.get("content")
        if content == '':
            return render(request, "network/index.html", {
                "error": "Your post can't be empty!"
            })
        new_post = Post.objects.create(user = request.user, content = content)
        return HttpResponseRedirect(reverse('index'))

    # Composing a new post must be via POST
    def get(self, request):
        return JsonResponse({"error": "POST request required."}, status=400)


class UserProfileView(DetailView):
    template_name = "network/user-profile.html"
    model = UserProfile
    context_object_name = "user_profile"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_ = get_object_or_404(User, id=self.kwargs.get('pk'))
        user_posts = Post.objects.filter(user=user_)

        # Create page controll
        paginator = Paginator(user_posts, 10)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        # Check if user is followed or not
        context["followed"] = False
        for following in user_.followers.all():
            if following.user == self.request.user:
                context["followed"] = True
                break

        context["followings"] = user_.followings.all().count()
        context["followers"] = user_.followers.all().count()
        context["page_obj"] = page_obj
        context["num_posts"] = user_posts.count()
        context["is_prof"] = True
        return context


class HandleFollowingView(LoginRequiredMixin, View):
    def get(self, request, pk):
        user_to_follow = get_object_or_404(User, id=pk)
        num_followers = user_to_follow.followers.all().count()

        # check user dont follow himself
        if request.user == user_to_follow:
            return JsonResponse({"error": "You can't follow yourself!"}, status=404)

        try:
            get_follow_obj = Following.objects.get(
                user=request.user.id, user_followed=user_to_follow)

        except Following.DoesNotExist:
            new_follow_obj = Following(
                user=request.user, user_followed=user_to_follow)
            new_follow_obj.save()
            return JsonResponse({
                "action": "followed",
                "followers": num_followers + 1
            }, status=200)

        else:
            get_follow_obj.delete()
            return JsonResponse({"action": "unfollowed", "followers": num_followers - 1}, status=200)


class FollowingUserPostsView(LoginRequiredMixin, ListView):
    template_name = "network/following-user-post.html"
    context_object_name = "posts"
    paginate_by = 10

    def get_queryset(self):
        qs = Post.objects.filter(
            user__in=self.request.user.get_following_users())
        return qs


class EditeFormView(View):
    def post(self, request, pk):
        post = get_object_or_404(Post, id=pk)
        print(post)
        # Check The post user editing post or not
        if post.user != self.request.user:
            print('first error')
            return JsonResponse({"error": "You can't edite someone else post!"}, status=400)

        data = json.loads(request.body)
        print(data)
        content = data.get("content")
        if content.strip() == "":
            print("second eror")
            return JsonResponse({"error": "Your post can't be empty!"}, status=400)
        post.content = content
        post.save()
        return JsonResponse({"content":post.content}, status=200)


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
            profile = UserProfile.objects.create(user=user)
            user.save()
            profile.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from .models import PostLike, User,Post


def index(request):
    all_posts = Post.objects.all()
    if request.method == "POST":
        message = request.POST.get("message")
        if message != "":
            post = Post()
            post.author = request.user
            post.message =  message
            post.save()
            return render(request, "network/index.html",)
        else:
            return render(request, "network/index.html", {
                "message": "Post cannot be empty"
            })
            
    return render(request, "network/index.html",{
        "posts":all_posts,
    })
  
def like_post(request):
    username = request.user.username
    post_id = request.GET.get('post_id')
    post = Post.objects.get(id=post_id)
    
    like_filter = PostLike.objects.filter(post_id=post_id,user=username).first()
    if like_filter == None:
        new_like = PostLike.objects.create(post_id=post_id,user=username)
        new_like.save()
        post.no_of_likes = post.no_of_likes+1
        post.save()
        return redirect('/')
    else:
        like_filter.delete()
        post.no_of_likes = post.no_of_likes -1
        post.save()
        return redirect("/")
    
    # post= get_object_or_404(Post,id=pk)
    # if post.likes.filter(id=request.user.id).exists():
    #     post.likes.remove(request.user)
    # else:
    #     post.likes.add(request.user)
    # return HttpResponseRedirect(reverse('index'))


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


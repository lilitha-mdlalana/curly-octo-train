from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import FollowersCount, PostLike, User, Post


def index(request):
    all_posts = Post.objects.all()
    if request.method == "POST":
        message = request.POST.get("message")
        if message != "":
            post = Post()
            post.author = request.user
            post.message = message
            post.save()
            return render(
                request,
                "network/index.html",
            )
        else:
            return render(
                request, "network/index.html", {"message": "Post cannot be empty"}
            )

    return render(
        request,
        "network/index.html",
        {
            "posts": all_posts,
        },
    )


def like_post(request):
    username = request.user.username
    post_id = request.GET.get("post_id")
    post = Post.objects.get(id=post_id)

    like_filter = PostLike.objects.filter(post_id=post_id, user=username).first()
    if like_filter == None:
        new_like = PostLike.objects.create(post_id=post_id, user=username)
        new_like.save()
        post.no_of_likes = post.no_of_likes + 1
        post.save()
        return redirect("/")
    else:
        like_filter.delete()
        post.no_of_likes = post.no_of_likes - 1
        post.save()
        return redirect("/")
    

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
            return render(
                request,
                "network/login.html",
                {"message": "Invalid username and/or password."},
            )
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
        if username == "" and email == "":
            return render(
                request, "network/register.html", {"message": "All fields should be filled in."}
            )
        if password != confirmation:
            return render(
                request, "network/register.html", {"message": "Passwords must match."}
            )

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(
                request, "network/register.html", {"message": "Username already taken."}
            )
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

@login_required(login_url="login")
def edit_post(request, pk):
    post = Post.objects.get(pk=pk)
    if request.method == "POST":
        post_message = request.POST.get("message").strip()
        if post_message != None:
            post.message = post_message
            post.save()
            return redirect(reverse('index'))
        else:
            message = "Message cannot be empty."
            return render(
                request, "network/edit-post.html", {"post": post, "message": message}
            )
    return render(request, "network/edit-post.html", {"post": post})

@login_required(login_url="login")
def delete_post(request, pk):
    post = get_object_or_404(Post,pk=pk)
    if post.author == request.user:
        post.delete()
        return redirect(reverse('index'))
    else:
        return redirect(reverse('index'))

def follow(request):
    if request.method =="POST":
        follower = request.POST.get('follower')
        user = request.POST.get('user')
        if FollowersCount.objects.filter(follower=follower,user=user).first():
            delete_follower = FollowersCount.objects.get(follower=follower,user=user)
            delete_follower.delete()
            return redirect(reverse('user-profiles',args=[user]))
        else:
            new_follower = FollowersCount.objects.create(follower=follower,user=user)
            new_follower.save()
            return redirect(reverse('user-profiles',args=[user]))
    else:
        return redirect(reverse('index'))
    

def profile(request):
    post_by_user = Post.objects.filter(author=request.user)
    user_followers = len(FollowersCount.objects.filter(user=request.user))
    user_following = len(FollowersCount.objects.filter(follower=request.user))
    user_posts_length = len(post_by_user)
    return render(request, "network/profile.html",{
        "posts":post_by_user,
        'user_followers':user_followers,
        'user_following':user_following,
        "posts_length":user_posts_length,
    })
    
def user_details(request,pk):
    user_object = User.objects.get(username=pk)
    user_posts = Post.objects.filter(author=user_object)
    user_posts_length = len(user_posts)
    follower = request.user.username
    user = pk
    
    if FollowersCount.objects.filter(follower=follower,user=user).first():
        button_text = "Unfollow"
    else:
        button_text = "Follow"
        
    user_followers = len(FollowersCount.objects.filter(user=pk))
    user_following = len(FollowersCount.objects.filter(follower=pk))
    return render(request, "network/user-profiles.html",{
        "user_object":user_object,
        "user_posts": user_posts,
        "posts_length":user_posts_length,
        'button_text':button_text,
        'user_followers':user_followers,
        'user_following':user_following
    })
    
def following(request):
    user_following = FollowersCount.objects.filter(follower=request.user)
    return render(request,"network/following.html",{
        "following":user_following
    })
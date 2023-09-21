
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("like-post",views.like_post,name="like-post"),
    path("edit/<int:pk>/",views.edit_post,name="edit-post"),
    path("delete/<int:pk>/", views.delete_post, name="delete-post"),
    path("follow",views.follow,name="follow"),
    path("following/",views.following,name="following"),
    path("profile/", views.profile, name="profile"),
    path('profile/user/<str:pk>/',views.user_details,name="user-profiles"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register")
]


from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("profile/<str:id>", views.profile, name="profile"),
    path("following", views.following, name="following"),
    path("edit/<str:num>", views.edit, name="edit"), 
    path("likepst/<str:num1>", views.likepst, name="likepst"), 
]

from django.contrib import admin
from django.urls import path
from main.views import show_main, login, register, review

app_name = "main"

urlpatterns = [
    path("", show_main, name="show_main"),
    path("login/", login, name="login"),
    path("register/", register, name="register"),
    path("review/", review, name="review")
]

from django.contrib import admin
from django.urls import path
from main.views import show_main, login_user, register, request_admin

app_name = "main"

urlpatterns = [
    path("", show_main, name="show_main"),
    path("login/", login_user, name="login_user"),
    path("register/", register, name="register"),
    path("request-admin/", request_admin, name="request_admin"),
]

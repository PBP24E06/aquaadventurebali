from django.contrib import admin
from django.urls import path
from main.views import show_main, login_user, register, checkout

app_name = "main"

urlpatterns = [
    path("", show_main, name="show_main"),
    path("login/", login_user, name="login_user"),
    path("register/", register, name="register"),
    path("checkout/<uuid:id>", checkout, name="checkout")
]

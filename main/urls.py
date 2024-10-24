from django.contrib import admin
from django.urls import path
from main.views import show_main, login_user, register, checkout_cart

app_name = "main"

urlpatterns = [
    path("", show_main, name="show_main"),
    path("login/", login_user, name="login_user"),
    path("register/", register, name="register"),
    path("checkout/", checkout_cart, name="checkout_cart")
]

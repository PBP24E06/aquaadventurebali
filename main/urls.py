from django.contrib import admin
from django.urls import path
from main.views import show_main, login_user, register, create_review, request_admin, show_json, checkout, logout_user, all_review


app_name = "main"

urlpatterns = [
    path("", show_main, name="show_main"),
    path("login/", login_user, name="login_user"),
    path("logout/", logout_user, name='logout_user'),
    path("register/", register, name="register"),
    path("create-review/<uuid:id>", create_review, name="create_review"),
    path("checkout/<uuid:id>", checkout, name="checkout"),
    path("request-admin/", request_admin, name="request_admin"),
    path('json/', show_json, name='show_json'),
    path("all-review/<uuid:id>", all_review, name="all_review"),
]

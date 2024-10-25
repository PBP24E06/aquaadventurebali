from django.contrib import admin
from django.urls import path
from main.views import show_main, login_user, register, add_discussion_or_reply, show_user_discussion

app_name = "main"

urlpatterns = [
    path("", show_main, name="show_main"),
    path("login/", login_user, name="login_user"),
    path("register/", register, name="register"),
    path('add_discussion_or_reply/<int:product_id>/', add_discussion_or_reply, name='add_discussion_or_reply'),
    path('my_discussion/<uuid:user_id>', show_user_discussion, name="show_user_discussion"),
]

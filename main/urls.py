from django.contrib import admin
from django.urls import path
from .views import show_main, login_user, logout_user, register, checkout, request_admin, show_json, create_product, delete_product, edit_product, all_review, request_admin, create_review, product_detail, profile_view, edit_profile, add_discussion_or_reply, show_user_discussion, show_forum_json, delete_discussion, show_user_profile_json

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
    path('create-product', create_product, name='create_product'),
    path('delete/<uuid:id>', delete_product, name='delete_product'),
    path('edit-product/<uuid:id>', edit_product, name='edit_product'),
    path('product-detail/<uuid:id>', product_detail, name='product_detail'),
    path('profile/', profile_view, name='profile'),
    path('edit_profile/', edit_profile, name='edit_profile'),
    path('user_discussion/<int:user_id>/', show_user_discussion, name="show_user_discussion"),
    path('add_discussion_or_reply/<uuid:product_id>/', add_discussion_or_reply, name='add_discussion_or_reply'),
    path('forum_json/<uuid:product_id>/', show_forum_json, name='show_forum_json'),
    path('delete_discussion/<int:discussion_id>/', delete_discussion, name='delete_discussion'),
    path('user_profile_json/<int:userId>/', show_user_profile_json, name="show_user_profile_json")
]

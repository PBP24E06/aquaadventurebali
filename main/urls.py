from django.contrib import admin
from django.urls import path
from main.views import show_main, login_user, logout_user, register, checkout, request_admin, show_json, create_product, delete_product, edit_product, all_review, request_admin, create_review, product_detail, profile_view, edit_profile, show_wishlist, add_wishlist, delete_wishlist, filter_wishlist


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
    path('wishlist/', show_wishlist, name='show_wishlist'),
    path('filter_wishlist/', filter_wishlist, name='filter_wishlist'),
    path('delete_wishlist/<uuid:id>', delete_wishlist, name='delete_wishlist'),
    path('add_wishlist/<uuid:id>', add_wishlist, name='add_wishlist'),
]

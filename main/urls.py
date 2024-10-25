from django.contrib import admin
from django.urls import path


from .views import show_main, login_user, logout_user, register, checkout, request_admin, show_json, create_product, delete_product, edit_product, add_discussion_or_reply, show_user_discussion, show_product, show_forum_json, delete_discussion

app_name = "main"

urlpatterns = [
    path("", show_main, name="show_main"),
    path("login/", login_user, name="login_user"),
    path("logout/", logout_user, name='logout_user'),
    path("register/", register, name="register"),
    path("checkout/<uuid:id>", checkout, name="checkout"),
    path("request-admin/", request_admin, name="request_admin"),
    path('json/', show_json, name='show_json'),
    path('create-product', create_product, name='create_product'),
    path('delete/<uuid:id>', delete_product, name='delete_product'),
    path('edit-product/<uuid:id>', edit_product, name='edit_product'),
    path('my_discussion/<int:user_id>', show_user_discussion, name="show_user_discussion"),
    path('product_detail/<uuid:product_id>', show_product, name="product_detail"),
    path('add_discussion_or_reply/<uuid:product_id>/', add_discussion_or_reply, name='add_discussion_or_reply'),
    path('forum_json/<uuid:product_id>/', show_forum_json, name='show_forum_json'),
    path('delete_discussion/<int:discussion_id>/', delete_discussion, name='delete_discussion'),
]

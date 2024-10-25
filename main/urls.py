from django.contrib import admin
from django.urls import path


from main.views import show_main, login_user, logout_user, register, checkout, request_admin, show_json, create_product, delete_product, edit_product, view_transaction_history



app_name = "main"

urlpatterns = [
    path("", show_main, name="show_main"),
    path("login/", login_user, name="login_user"),
    path("logout/", logout_user, name='logout_user'),
    path("register/", register, name="register"),
    path("checkout/<uuid:id>", checkout, name="checkout"),
    path("request-admin/", request_admin, name="request_admin"),
    path('json/', show_json, name='show_json'),
    path('transaction-history', view_transaction_history, name='view_transaction_history'),
    path('create-product', create_product, name='create_product'),
    path('delete/<uuid:id>', delete_product, name='delete_product'),
    path('edit-product/<uuid:id>', edit_product, name='edit_product')
]

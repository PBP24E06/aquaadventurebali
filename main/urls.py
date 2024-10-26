from django.contrib import admin
from django.urls import path

from main.views import show_main, login_user, logout_user, register, checkout, request_admin, show_json_product, show_json_transaction, add_product_ajax, delete_product, edit_product, all_review, request_admin, create_review, view_transaction_history, checkout_by_ajax, get_product_data_for_checkout

from main.views import show_main, login_user, logout_user, register, checkout, request_admin, delete_product, edit_product, all_review, request_admin, create_review, product_detail, profile_view, edit_profile, create_report


app_name = "main"

urlpatterns = [
    path("", show_main, name="show_main"),
    path("login/", login_user, name="login_user"),
    path("logout/", logout_user, name='logout_user'),
    path("register/", register, name="register"),
    path("create-review/<uuid:id>", create_review, name="create_review"),
    path("checkout/<uuid:id>", checkout, name="checkout"),
    path("request-admin/", request_admin, name="request_admin"),
    path('json-product/', show_json_product, name='show_json_product'),
    path('json-transaction/', show_json_transaction, name='show_json_transaction'),
    path('transaction-history', view_transaction_history, name='view_transaction_history'),
    path("all-review/<uuid:id>", all_review, name="all_review"),
    path('add-product-ajax/', add_product_ajax, name='add_product_ajax'),
    path('delete/<uuid:id>', delete_product, name='delete_product'),
    path('edit-product/<uuid:id>', edit_product, name='edit_product'),
    path('product/<uuid:product_id>/report/', create_report, name='create_report'),
    path('checkout-by-ajax/<uuid:id>/', checkout_by_ajax, name='checkout_by_ajax'),
    path('get_product_data_for_checkout/<uuid:id>/', get_product_data_for_checkout, name='get_product_data_for_checkout'),
    path('product-detail/<uuid:id>', product_detail, name='product_detail'),
    path('profile/', profile_view, name='profile'),
    path('edit_profile/', edit_profile, name='edit_profile'),
]

from django.contrib import admin
from django.urls import path

from main.views import show_main, login_user, logout_user, register, checkout, request_admin, show_json_product, show_json_transaction, delete_product, edit_product, all_review, request_admin, create_review, view_transaction_history, checkout_by_ajax, product_detail,edit_profile, profile_view, create_review_by_ajax, get_product_data_for_checkout, add_product_ajax, show_user_discussion, show_forum_json, delete_discussion, show_user_profile_json, show_user_discussion_json, add_discussion_or_reply, show_wishlist, add_wishlist, delete_wishlist, filter_wishlist




from main.views import show_main, login_user, logout_user, register, checkout, request_admin, show_json_product, show_json_transaction, delete_product, edit_product, all_review, request_admin, create_review, view_transaction_history, checkout_by_ajax, get_product_data_for_checkout, product_detail, profile_view, edit_profile



from .views import show_main, login_user, logout_user, register, checkout, request_admin, show_json_product, show_json_transaction, delete_product, edit_product, all_review, request_admin, create_review, view_transaction_history, checkout_by_ajax, product_detail,edit_profile, profile_view, create_review_by_ajax, get_product_data_for_checkout, add_product_ajax, add_discussion_or_reply, show_user_discussion, show_forum_json, delete_discussion, show_user_profile_json, show_user_discussion_json, create_report_by_ajax, show_json_complain

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
    path('json-complain/', show_json_complain, name='show_json_complain'),
    path('transaction-history', view_transaction_history, name='view_transaction_history'),
    path("all-review/<uuid:id>", all_review, name="all_review"),
    path('add-product-ajax/', add_product_ajax, name='add_product_ajax'),
    path('delete/<uuid:id>', delete_product, name='delete_product'),
    path('edit-product/<uuid:id>', edit_product, name='edit_product'),
    path('checkout-by-ajax/<uuid:id>/', checkout_by_ajax, name='checkout_by_ajax'),
    path('get_product_data_for_checkout/<uuid:id>/', get_product_data_for_checkout, name='get_product_data_for_checkout'),
    path('product-detail/<uuid:id>', product_detail, name='product_detail'),
    path('profile/', profile_view, name='profile'),
    path('edit_profile/', edit_profile, name='edit_profile'),
    path('create-report-by-ajax/<uuid:product_id>', create_report_by_ajax, name='create-report-by-ajax'),
    path('create-review-by-ajax/<uuid:id>', create_review_by_ajax, name="create-review-by-ajax"),
    path('create-review-by-ajax/<uuid:id>', create_review_by_ajax, name="create_review_by_ajax"),
    path('user_discussion/<int:user_id>/', show_user_discussion, name="show_user_discussion"),
    path('add_discussion_or_reply/<uuid:product_id>/', add_discussion_or_reply, name='add_discussion_or_reply'),
    path('forum_json/<uuid:product_id>/', show_forum_json, name='show_forum_json'),
    path('delete_discussion/<int:discussion_id>/', delete_discussion, name='delete_discussion'),
    path('user_profile_json/<int:userId>/', show_user_profile_json, name="show_user_profile_json"),
    path('show_user_discussion_json/<int:user_id>/', show_user_discussion_json, name='show_user_discussion_json'),
    path('wishlist/', show_wishlist, name='show_wishlist'),
    path('filter_wishlist/', filter_wishlist, name='filter_wishlist'),
    path('delete_wishlist/<uuid:id>', delete_wishlist, name='delete_wishlist'),
    path('add_wishlist/<uuid:id>', add_wishlist, name='add_wishlist'),
    
    
]

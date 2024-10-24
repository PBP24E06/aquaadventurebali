from django.forms import ModelForm
from main.models import Product, Review, Forum, Wishlist, Cart, Report
from django import forms

class ProductForm(ModelForm):
    class Meta:
        model = Product
        # fields = (isi sesuai field form yang dibutuhkan)


class ReviewForm(ModelForm):
    class Meta:
        model = Review
        # fields = ["rating", "review_text"]


class ForumForm(ModelForm):
    class Meta:
        model = Forum
        # fields = (isi sesuai field form yang dibutuhkan)


class WishlistForm(ModelForm):
    class Meta:
        model = Wishlist
        # fields = (isi sesuai field form yang dibutuhkan)


class CheckoutForm(ModelForm):
    name = forms.CharField(max_length=255)
    email = forms.CharField(max_length=255)
    phone_number = forms.CharField(max_length=30)

    class Meta:
        model = Cart
        fields = ["name", "email", "phone_number"]
        

class ReportForm(ModelForm):
    class Meta:
        model = Report
        # fields = (isi sesuai field form yang dibutuhkan)
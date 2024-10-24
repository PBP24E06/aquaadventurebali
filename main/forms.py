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
        fields = ["rating", "review_text"]


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
    email = forms.EmailField()
    phone = forms.CharField(max_length=15)

    class Meta:
        model = Cart
        fields = ["name", "email", "phone"]
        

class ReportForm(ModelForm):
    class Meta:
        model = Report
        # fields = (isi sesuai field form yang dibutuhkan)
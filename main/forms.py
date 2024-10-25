from django.forms import ModelForm
from main.models import Product, Review, Forum, Wishlist, Cart, Report
from django.utils.html import strip_tags
from django import forms

class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ["name", "kategori", "harga", "toko", "alamat", "kontak", "gambar"]


class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ["rating", "review_text"]


class ForumForm(ModelForm):
    class Meta:
        model = Forum
        fields = ["message"]

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        self.product = kwargs.pop('product', None)
        self.parent = kwargs.pop('parent', None)
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        comment = super().save(commit=False)
        comment.user = self.user
        comment.product = self.product
        comment.commenter_name = self.user.username
        if self.parent:
            comment.parent = self.parent
        if commit:
            comment.save()
        return comment

    def clean_message(self):
        message = self.cleaned_data.get('message')
        sanitized_message = strip_tags(message)
        return sanitized_message


class WishlistForm(ModelForm):
    class Meta:
        model = Wishlist
        fields = ["product", "user"]


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
        fields = ["message"]
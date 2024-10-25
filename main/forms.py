from django.forms import ModelForm
from django.utils.html import strip_tags
from main.models import Product, Review, Forum, Wishlist, Cart, Report

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
        fields = ["diskusi"]

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        self.product = kwargs.pop('product', None)
        self.parent = kwargs.pop('parent', None)
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        comment = super().save(commit=False)
        comment.user = self.user
        comment.product = self.product
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
        # fields = (isi sesuai field form yang dibutuhkan)


class CartForm(ModelForm):
    class Meta:
        model = Cart
        # fields = (isi sesuai field form yang dibutuhkan)
        

class ReportForm(ModelForm):
    class Meta:
        model = Report
        # fields = (isi sesuai field form yang dibutuhkan)
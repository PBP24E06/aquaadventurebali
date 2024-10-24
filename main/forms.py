from django.forms import ModelForm
from main.models import Product, Review, Forum, Wishlist, Cart, Report

class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'kategori', 'harga', 'toko', 'alamat', 'kontak', 'gambar']


class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ["rating", "review_text"]


class ForumForm(ModelForm):
    class Meta:
        model = Forum
        fields = "__all__"


class WishlistForm(ModelForm):
    class Meta:
        model = Wishlist
        fields = "__all__"


class CartForm(ModelForm):
    class Meta:
        model = Cart
        fields = "__all__"
        

class ReportForm(ModelForm):
    class Meta:
        model = Report
        fields = "__all__"
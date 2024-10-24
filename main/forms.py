from django.forms import ModelForm
from main.models import Product, Review, Forum, Wishlist, Transaction, Report


class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'kategori', 'harga', 'toko', 'alamat', 'kontak', 'gambar']  # Add the necessary fields


class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ["rating", "review_text"]  # Specify the fields here


class ForumForm(ModelForm):
    class Meta:
        model = Forum
        fields = ['product', 'user', 'message']  # Specify the fields here


class WishlistForm(ModelForm):
    class Meta:
        model = Wishlist
        fields = ['product', 'user']  # Specify the fields here


class TransactionForm(ModelForm):
    class Meta:
        model = Transaction
        fields = ["name", "email", "phone_number", "product"]  # Include 'product' as well


class ReportForm(ModelForm):
    class Meta:
        model = Report
        fields = ['product', 'user', 'message']  # Specify the fields here

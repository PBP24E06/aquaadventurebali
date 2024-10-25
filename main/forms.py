from django.forms import ModelForm
from main.models import Product, Review, Forum, Wishlist, Transaction, Report


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


class WishlistForm(ModelForm):
    class Meta:
        model = Wishlist
        fields = ["product", "user"]


class TransactionForm(ModelForm):
    class Meta:
        model = Transaction
        fields = ["name", "email", "phone_number"] 


class ReportForm(ModelForm):
    class Meta:
        model = Report
        fields = ["message"]

from django.forms import ModelForm
from main.models import Product, Review, Forum, Wishlist, Transaction, Report


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
        fields = ['name', 'email', 'phone_number']


class TransactionForm(ModelForm):
    class Meta:
        model = Transaction
        # fields = (isi sesuai field form yang dibutuhkan)
        

class ReportForm(ModelForm):
    class Meta:
        model = Report
        # fields = (isi sesuai field form yang dibutuhkan)
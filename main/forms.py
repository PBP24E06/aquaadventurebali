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

        def __init__(self, *args, **kwargs):
                super(TransactionForm, self).__init__(*args, **kwargs)
                self.fields['name'].widget.attrs.update({
                'class': 'px-4 py-2.5 bg-white text-gray-800 rounded-md w-full text-sm border-b focus:border-gray-800 outline-none',
                'placeholder': 'Full Name'
                })
                self.fields['email'].widget.attrs.update({
                'class': 'px-4 py-2.5 bg-white text-gray-800 rounded-md w-full text-sm border-b focus:border-gray-800 outline-none',
                'placeholder': 'Email'
                })
                self.fields['phone_number'].widget.attrs.update({
                'class': 'px-4 py-2.5 bg-white text-gray-800 rounded-md w-full text-sm border-b focus:border-gray-800 outline-none',
                'placeholder': 'Phone No.'
                })



class ReportForm(ModelForm):
    class Meta:
        model = Report
        fields = ["message"]

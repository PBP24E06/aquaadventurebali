from django.forms import ModelForm
from main.models import Product, Review, Forum, Wishlist, Transaction, Report
from django.utils.html import strip_tags


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

        def clean_name(self):
            name = self.cleaned_data["name"]
            return strip_tags(name)
            
        def clean_email(self):
            email = self.cleaned_data["email"]
            return strip_tags(email)
        
        def clean_phone_number(self):
            phone_number = self.cleaned_data["phone_number"]
            return strip_tags(phone_number)




class ReportForm(ModelForm):
    class Meta:
        model = Report
        fields = ["message"]

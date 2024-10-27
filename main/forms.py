from django.forms import ModelForm
from main.models import Product, Review, Forum, Wishlist, Transaction, Report
from django.utils.html import strip_tags


from main.models import Product, Review, Forum, Wishlist, Transaction, Report, UserProfile
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

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['profile_picture', 'alamat', 'birthdate', 'phone_number', 'bio']

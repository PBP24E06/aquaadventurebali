from django.forms import ModelForm
from main.models import Product, Review

class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ["name", "kategori", "harga", "toko", "alamat", "kontak", "gambar"]


class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ["rating", "review_text"]
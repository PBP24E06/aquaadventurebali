from django.db import models
import uuid
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name="profile", on_delete=models.CASCADE)
    roles = (
        ('CUSTOMER', 'Customer'),
        ('ADMIN', 'Admin'),
    )
    role = models.CharField(max_length=10, choices=roles, default='CUSTOMER')
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)  # Gambar profil opsional
    alamat = models.TextField(blank=True, null=True)  # Alamat opsional
    birthdate = models.DateField(null=True, blank=True)  # Tanggal lahir opsional
    phone_number = models.CharField(max_length=15, null=True, blank=True)  # Nomor telepon opsional
    bio = models.TextField(null=True, blank=True)  # Deskripsi diri opsional
    date_joined = models.DateTimeField(auto_now_add=True)  


    def promote_admin(self):
        if self.role == 'CUSTOMER':
            self.role = 'ADMIN'
            self.save()

    def demote_to_customer(self):
        if self.role == 'ADMIN':
            self.role = 'CUSTOMER'
            self.save()


class Product(models.Model):
    id = models.UUIDField(primary_key=True, default = uuid.uuid4, editable = False)
    name = models.CharField(max_length=255)
    kategori = models.CharField(max_length=255)
    harga = models.IntegerField()
    toko = models.CharField(max_length=255)
    alamat = models.TextField()
    kontak = models.CharField(max_length=255)
    gambar = models.ImageField()

    def average_rating(self):
        reviews = self.reviews.all() 
        if reviews.count() > 0:
            avg = sum(review.rating for review in reviews) / len(reviews)
            return f"{avg:.2f}"
        return 0


class Review(models.Model):
    product = models.ForeignKey(Product, related_name='reviews', on_delete=models.CASCADE)  # Relasi balik ke product
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # User yang membuat review
    rating = models.FloatField(validators=[MinValueValidator(1.0), MaxValueValidator(5.0)])
    review_text = models.TextField()

    class Meta:
        unique_together = ('product', 'user')


class Forum(models.Model):
    product = models.ForeignKey(Product, related_name='discussions', on_delete=models.CASCADE)  # Relasi balik ke product
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    commenter_name = models.CharField(max_length=255, default='Anonymous')
    message = models.TextField()
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies')
    created_at = models.DateTimeField(auto_now_add=True)

class Wishlist(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name="wishlist", on_delete=models.CASCADE)  # Relasi balik ke user
    

class Cart(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name="cart", on_delete=models.CASCADE)  # Relasi balik ke user
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=30)
    time = models.DateField(auto_now_add=True)


class Report(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name="report", on_delete=models.CASCADE)  # Relasi balik ke user
    message = models.TextField()


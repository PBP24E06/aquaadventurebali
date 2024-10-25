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
    gambar = models.URLField()

    def average_rating(self):
        reviews = self.reviews.all() 
        if len(reviews) > 0:
            return sum(review.rating for review in reviews) / len(reviews)
        return 0


class Review(models.Model):
    product = models.ForeignKey(Product, related_name='reviews', on_delete=models.CASCADE)  # Relasi balik ke product
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # User yang membuat review
    rating = models.FloatField(validators=[MinValueValidator(1.0), MaxValueValidator(5.0)])
    review_text = models.TextField()


class Forum(models.Model):
    product = models.ForeignKey(Product, related_name='discussions', on_delete=models.CASCADE)  # Relasi balik ke product
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class Wishlist(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name="wishlist", on_delete=models.CASCADE)  # Relasi balik ke user
    

class Transaction(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name="transaction", on_delete=models.CASCADE)  # Relasi balik ke user
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=255)
    checkout_time = models.DateTimeField(auto_now_add=True)


class Report(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name="report", on_delete=models.CASCADE)  # Relasi balik ke user
    message = models.TextField()


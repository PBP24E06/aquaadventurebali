from django.test import TestCase, Client
from .models import Transaction, Product, UserProfile

from django.contrib.auth.models import User


# Create your tests here.

class TestModels(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.product = None

    def test_model_product(self):
        product = Product.objects.create(
            name='Item1', kategori='Kategori1', harga=10000, 
            toko='Toko Bagus', alamat='Jalan jalan', kontak='12345678', 
            gambar='static/image/86a6be95-eaa0-458c-98f0-785d5abd3772-550x550.jpg'
        )

        self.product = product
        self.assertTrue(isinstance(product, Product))

    def test_model_transaction(self):
        transaction = Transaction(
            product=self.product, user=self.user, name='tester',
            email='tester@gmail.com', phone_number='12345678',
        )

        self.assertTrue(isinstance(transaction, Transaction))

    def test_model_user_profile(self):
        user_profile = UserProfile(
            user=self.user
        )

class TestViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.userProfile = UserProfile.objects.create(user=self.user)
        self.client.login(username='testuser', password='testpassword')

    def test_show_main(self):
        response = self.client.get('/')
        
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'main.html')


    def test_request_admin_with_login(self):
        response = self.client.get('/request-admin/')

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'request_admin.html')

    def test_request_admin_without_login(self):
        self.client.logout()
        response = self.client.get('/request-admin/')

        self.assertEquals(response.status_code, 302)
        self.assertTemplateNotUsed(response, 'request_admin.html')

    def test_view_transaction_history_with_login(self):
        response = self.client.get('/transaction-history')

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'transaction_history.html')

    def test_view_transaction_history_without_login(self):
        self.client.logout()
        response = self.client.get('/transaction-history')

        self.assertEquals(response.status_code, 302)
        self.assertTemplateNotUsed(response, 'request_admin.html')

    def test_create_product_without_login(self):
        self.client.logout()
        response = self.client.get('/create-product/')

        self.assertEquals(response.status_code, 302)
        self.assertTemplateNotUsed(response, 'request_admin.html')

    def test_create_product_with_login_not_admin(self):
        response = self.client.get('/create-product/')

        self.assertEquals(response.status_code, 403)
        self.assertTemplateNotUsed(response, 'request_admin.html')

    # def test_create_product_admin(self):
    #     self.userProfile.promote_admin()
    
    #     # Ensure the profile is saved with the new role
    #     self.userProfile.save()
        
    #     response = self.client.get('/create-product/')

    #     self.assertEquals(response.status_code, 201)
    #     self.assertTemplateNotUsed(response, 'request_admin.html')
        
    # def test_view_product_detail(self):
    #     response = self.client.get('/product-detail/fa841a2a-528d-47c6-a0f9-0155eed06d03')

    #     self.assertEquals(response.status_code, 200)
    #     self.assertTemplateUsed(response, 'product_detail.html')

        
        

    


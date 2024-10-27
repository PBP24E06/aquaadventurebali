from django.test import TestCase, Client
from .models import Transaction, Product, UserProfile, Review, Forum
from django.urls import reverse
from django.contrib.auth.models import User

from uuid import uuid4


from django.contrib.auth.models import User


# Create your tests here.   

class TestProduct(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.userProfile = UserProfile.objects.create(user=self.user)
        self.client.login(username='testuser', password='testpassword')
        self.product = Product.objects.create(
            name='Item1', kategori='Kategori1', harga=10000, 
            toko='Toko Bagus', alamat='Jalan jalan', kontak='12345678', 
            gambar='static/image/86a6be95-eaa0-458c-98f0-785d5abd3772-550x550.jpg'
        )

    def test_model_product(self):
        product = Product.objects.create(
            name='Item1', kategori='Kategori1', harga=10000, 
            toko='Toko Bagus', alamat='Jalan jalan', kontak='12345678', 
            gambar='static/image/86a6be95-eaa0-458c-98f0-785d5abd3772-550x550.jpg'
        )

        
        self.assertTrue(isinstance(product, Product))

    def test_show_main(self):
        response = self.client.get('/')
        
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'main.html')

    def test_model_user_profile(self):
        user_profile = UserProfile(
            user=self.user
        )

        self.assertTrue(isinstance(user_profile, UserProfile))

    def test_request_admin_with_login(self):
        response = self.client.get('/request-admin/')

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'request_admin.html')

    def test_request_admin_without_login(self):
        self.client.logout()
        response = self.client.get('/request-admin/')

        self.assertEquals(response.status_code, 302)
        self.assertTemplateNotUsed(response, 'request_admin.html')

    def test_add_product_ajax_without_login(self):
        self.client.logout()
        response = self.client.post('/add-product-ajax/')

        self.assertEquals(response.status_code, 302)

    def test_add_product_ajax_login_not_admin(self):
        response = self.client.post('/add-product-ajax/')

        self.assertEquals(response.status_code, 403)

    def test_edit_product(self):
        self.userProfile.promote_admin()
        response = self.client.get(f'/edit-product/{self.product.pk}')

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'edit_product.html')

     # def test_view_product_detail(self):
    #     response = self.client.get('/product-detail/fa841a2a-528d-47c6-a0f9-0155eed06d03')

    #     self.assertEquals(response.status_code, 200)
    #     self.assertTemplateUsed(response, 'product_detail.html')


class TestCheckout(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.userProfile = UserProfile.objects.create(user=self.user)
        self.client.login(username='testuser', password='testpassword')
        self.product = Product.objects.create(
            name='Item1', kategori='Kategori1', harga=10000, 
            toko='Toko Bagus', alamat='Jalan jalan', kontak='12345678', 
            gambar='static/image/86a6be95-eaa0-458c-98f0-785d5abd3772-550x550.jpg'
        )

    def test_model_transaction(self):
        transaction = Transaction(
            product=self.product, user=self.user, name='tester',
            email='tester@gmail.com', phone_number='12345678',
        )

        self.assertTrue(isinstance(transaction, Transaction))

    def test_view_transaction_history_with_login(self):
        response = self.client.get('/transaction-history')

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'transaction_history.html')

    def test_view_transaction_history_without_login(self):
        self.client.logout()
        response = self.client.get('/transaction-history')

        self.assertEquals(response.status_code, 302)
        self.assertTemplateNotUsed(response, 'transaction_history.html')

    def test_checkout_successfull(self):
        url = reverse('main:checkout_by_ajax', args=[self.product.id])
        
        
        data = {
            'name': 'tes',
            'email': 'tes@gmail.com',
            'phone_number': '123456789'
        }
        
        response = self.client.post(url, data)
        
        
        self.assertEqual(response.status_code, 201)

    def test_checkout_wrong_email(self):


        url = reverse('main:checkout_by_ajax', args=[self.product.id])
        
        data = {
            'name': 'tes',
            'email': 'tesgmail.com',
            'phone_number': '123456789'
        }
        
        response = self.client.post(url, data)
        
        
        self.assertEqual(response.status_code, 403)
        

    


class TestReview(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.userProfile = UserProfile.objects.create(user=self.user)
        self.client.login(username='testuser', password='testpassword')
        self.product = Product.objects.create(
            name='Item1', kategori='Kategori1', harga=10000, 
            toko='Toko Bagus', alamat='Jalan jalan', kontak='12345678', 
            gambar='static/image/86a6be95-eaa0-458c-98f0-785d5abd3772-550x550.jpg'
        )

    def test_model_review(self):
        review = Review(
            user=self.user, product=self.product,
            rating=4.5, review_text="keren amat"
        )

        self.assertTrue(isinstance(review, Review))

    def test_add_review_by_ajax(self):
        pass



class DiscussionTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password")
        self.other_user = User.objects.create_user(username="otheruser", password="password")
        
        self.user_profile = UserProfile.objects.create(
            user=self.user,
            role="CUSTOMER",
            alamat="Test Address",
            bio="Test bio"
        )
        
        self.product = Product.objects.create(
            id=uuid4(),
            name="Test Product",
            kategori="Test Category",
            harga=10000,
            toko="Test Store",
            alamat="Store Address",
            kontak="123456789",
        )

        self.discussion = Forum.objects.create(
            product=self.product,
            user=self.user,
            message="Initial discussion",
            commenter_name="testuser"
        )

    def test_add_discussion(self):
        self.client.login(username="testuser", password="password")
        response = self.client.post(reverse('main:add_discussion_or_reply', args=[self.product.id]), {
            "message": "Test discussion message"
        })
        self.assertEqual(response.status_code, 201)
        self.assertContains(response, "CREATED", status_code=201)

    def test_add_reply(self):
        self.client.login(username="testuser", password="password")
        response = self.client.post(reverse('main:add_discussion_or_reply', args=[self.product.id]), {
            "message": "Test reply message",
            "parent_id": self.discussion.id
        })
        self.assertEqual(response.status_code, 201)
        self.assertContains(response, "CREATED", status_code=201)

    def test_add_reply_with_invalid_parent(self):
        self.client.login(username="testuser", password="password")
        response = self.client.post(reverse('main:add_discussion_or_reply', args=[self.product.id]), {
            "message": "Test reply message",
            "parent_id": 9999 
        })
        self.assertEqual(response.status_code, 404)
        self.assertContains(response, "Parent comment does not exist", status_code=404)

    def test_delete_discussion_by_owner(self):
        self.client.login(username="testuser", password="password")
        response = self.client.delete(reverse('main:delete_discussion', args=[self.discussion.id]))
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {"message": "Discussion deleted successfully."})

    def test_delete_discussion_by_non_owner(self):
        self.client.login(username="otheruser", password="password")
        response = self.client.delete(reverse('main:delete_discussion', args=[self.discussion.id]))
        self.assertEqual(response.status_code, 403)
        self.assertContains(response, "You are not allowed to delete this discussion.", status_code=403)

    def test_show_forum_json(self):
        response = self.client.get(reverse('main:show_forum_json', args=[self.product.id]), {'page': 1})
        self.assertEqual(response.status_code, 200)
        self.assertIn("top_level_discussions", response.json())
        self.assertIn("discussions", response.json())

    def test_show_user_discussion(self):
        self.client.login(username="testuser", password="password")
        response = self.client.get(reverse('main:show_user_discussion', args=[self.user.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "user_discussion.html")

    def test_show_user_discussion_json(self):
        response = self.client.get(reverse('main:show_user_discussion_json', args=[self.user.id]), {'page': 1})
        self.assertEqual(response.status_code, 200)
        self.assertIn("discussions", response.json())

    def test_show_user_profile_json(self):
        response = self.client.get(reverse('main:show_user_profile_json', args=[self.user.id]))
        self.assertEqual(response.status_code, 200)
        data = response.json()
        
        if data:
            self.assertIn("fields", data[0])
        else:
            self.fail("Expected data in the response, but got an empty list.")

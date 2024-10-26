from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Product, Forum, UserProfile
from uuid import uuid4

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

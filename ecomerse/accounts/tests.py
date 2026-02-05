from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()

class RegisterViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.register_url = reverse("register")
        self.login_url = reverse("login")

    # -----------------------
    # GET REQUEST
    # -----------------------
    def test_register_get_request(self):
        response = self.client.get(self.register_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "Register.html")

    # -----------------------
    # SUCCESSFUL REGISTRATION
    # -----------------------
    def test_register_success(self):
        data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "Test@123",
            "confirm_password": "Test@123",
            "role": "buyer"
        }

        response = self.client.post(self.register_url, data)

        self.assertRedirects(response, self.login_url)
        self.assertTrue(User.objects.filter(email="test@example.com").exists())

    # -----------------------
    # PASSWORD MISMATCH
    # -----------------------
    def test_register_password_mismatch(self):
        data = {
            "username": "testuser",
            "email": "test2@example.com",
            "password": "Test@123",
            "confirm_password": "Wrong@123",
        }

        response = self.client.post(self.register_url, data)

        self.assertRedirects(response, self.register_url)
        self.assertFalse(User.objects.filter(email="test2@example.com").exists())

    # -----------------------
    # DUPLICATE EMAIL
    # -----------------------
    def test_register_existing_email(self):
        User.objects.create_user(
            username="existing",
            email="exists@example.com",
            password="Test@123",
            roles="buyer"  
        )

        data = {
            "username": "newuser",
            "email": "exists@example.com",
            "password": "Test@123",
            "confirm_password": "Test@123",
        }

        response = self.client.post(self.register_url, data)

        self.assertRedirects(response, self.register_url)
        self.assertEqual(User.objects.filter(email="exists@example.com").count(), 1)

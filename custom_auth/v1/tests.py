from django.test import TestCase
from django.urls import reverse
from custom_auth.v1.models import CustomUser

class AuthTests(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(email='test@example.com', password='password')

    def test_login(self):
        response = self.client.post(reverse('login'), {'username': 'test@example.com', 'password': 'password'})
        self.assertEqual(response.status_code, 302)

    def test_user_role_assignment(self):
        user = CustomUser.objects.get(email='test@example.com')
        self.assertEqual(user.role, 'RESTAURANTEMPLOYEE')

    def test_admin_creation(self):
        admin = CustomUser.objects.create_superuser(email='admin@example.com', password='adminpassword')
        self.assertEqual(admin.role, 'ADMIN')

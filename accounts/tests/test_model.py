"""Module to define test cases for accounts models"""
from django.test import TestCase
from accounts.models import User


class TestUserModel(TestCase):
    """Test cases for User model"""

    def test_create_user(self):
        """User should be created on valid data"""
        user = User.objects.create_user(username='username', email='username@gmail.com')
        user.set_password('username')
        user.save()
        self.assertEqual(str(user), user.username)

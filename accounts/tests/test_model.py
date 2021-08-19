from accounts.models import User
from django.test import TestCase


class TestUserModel(TestCase):

	def test_create_user(self):
		user = User.objects.create_user(username='username', email='username@gmail.com')
		user.set_password('username')
		user.save()
		self.assertEqual(str(user), user.username)
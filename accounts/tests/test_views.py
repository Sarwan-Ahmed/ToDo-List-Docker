from utils.setup_test import TestSetUp
from accounts.models import User
from rest_framework.authtoken.models import Token
import pdb

class TestRegisterView(TestSetUp):

	def test_register_without_data(self):
		res = self.client.post(self.register_url)
		self.assertEqual(res.status_code, 400)


	def test_register_with_without_email(self):
		del self.user_register_data['email']
		res = self.client.post(self.register_url, self.user_register_data, format="json")	
		self.assertEqual(res.status_code, 400)


	def test_register_with_without_username(self):
		del self.user_register_data['username']
		res = self.client.post(self.register_url, self.user_register_data, format="json")	
		self.assertEqual(res.status_code, 400)


	def test_register_with_without_password(self):
		del self.user_register_data['password']
		res = self.client.post(self.register_url, self.user_register_data, format="json")
		self.assertEqual(res.status_code, 400)


	def test_register_with_invalid_username(self):
		self.user_register_data['username'] = 'new user'
		res = self.client.post(self.register_url, self.user_register_data, format="json")	
		self.assertEqual(res.status_code, 400)


	def test_register_with_invalid_email(self):
		self.user_register_data['email'] = 'abc@gmail'
		res = self.client.post(self.register_url, self.user_register_data, format="json")
		self.assertEqual(res.status_code, 400)


	def test_register_with_valid_data(self):
		res = self.client.post(self.register_url, self.user_register_data, format="json")	
		self.assertEqual(res.status_code, 201)


	def test_register_with_existing_email(self):
		self.client.post(self.register_url, self.user_register_data, format="json")
		self.user_register_data['username'] = 'user'
		res = self.client.post(self.register_url, self.user_register_data, format="json")
		self.assertEqual(res.status_code, 400)


	def test_register_with_existing_username(self):
		self.client.post(self.register_url, self.user_register_data, format="json")
		self.user_register_data['email'] = 'new@gmail.com'
		res = self.client.post(self.register_url, self.user_register_data, format="json")
		self.assertEqual(res.status_code, 400)	



class TestLoginView(TestSetUp):

	def test_login_without_data(self):
		res = self.client.post(self.login_url)
		self.assertEqual(res.status_code, 400)


	def test_login_without_email(self):
		user = self.create_test_user()
		del self.user_login_data['username']
		res = self.client.post(self.login_url, self.user_login_data, format="json")
		self.assertEqual(res.status_code, 400)


	def test_login_without_password(self):
		user = self.create_test_user()
		del self.user_login_data['password']
		res = self.client.post(self.login_url, self.user_login_data, format="json")
		self.assertEqual(res.status_code, 400)


	def test_login_with_invalid_email(self):
		user = self.create_test_user()
		self.user_login_data['username'] = 'email'
		res = self.client.post(self.login_url, self.user_login_data, format="json")
		self.assertEqual(res.status_code, 400)


	def test_login_with_invalid_password(self):
		user = self.create_test_user()
		self.user_login_data['password'] = 'password'
		res = self.client.post(self.login_url, self.user_login_data, format="json")
		self.assertEqual(res.status_code, 400)


	def test_login_with_unverified_email(self):
		self.client.post(self.register_url, self.user_register_data, format="json")
		res = self.client.post(self.login_url, self.user_login_data, format="json")
		self.assertEqual(res.status_code, 401)


	def test_login_with_verified_email(self):
		user = self.create_test_user()
		res = self.client.post(self.login_url, self.user_login_data, format="json")
		self.assertEqual(res.status_code, 200)


	def test_login_without_email_authprovider(self):
		user = self.create_test_user()
		user.auth_provider = 'google'
		user.save()
		res = self.client.post(self.login_url, self.user_login_data, format="json")
		self.assertEqual(res.status_code, 401)



class TestLogoutView(TestSetUp):

	def test_logout_without_token(self):
		res = self.client.post(self.logout_url)
		self.assertEqual(res.status_code, 401)


	def test_logout_with_invalid_token(self):
		res = self.client.post(self.logout_url, **{'HTTP_AUTHORIZATION':'token abcds'})
		self.assertEqual(res.status_code, 401)


	def test_logout_with_valid_token(self):
		user = self.create_test_user()
		token = self.client.post(self.login_url, self.user_login_data, format="json").data['token']
		res = self.client.post(self.logout_url, **{'HTTP_AUTHORIZATION':'token '+token})
		self.assertEqual(res.status_code, 200)

	def test_logout_with_already_logged_out(self):
		user = self.create_test_user()
		token = self.client.post(self.login_url, self.user_login_data, format="json").data['token']
		self.client.post(self.logout_url, **{'HTTP_AUTHORIZATION':'token '+token})
		res = self.client.post(self.logout_url, **{'HTTP_AUTHORIZATION':'token '+token})		
		self.assertEqual(res.status_code, 401)



class TestResendLinkView(TestSetUp):

	def test_resendLink_without_data(self):
		res = self.client.post(self.resendLink_url)
		self.assertEqual(res.status_code, 400)


	def test_resendLink_with_invalid_email(self):
		res = self.client.post(self.resendLink_url, self.user_email, format='json')
		self.assertEqual(res.status_code, 404)


	def test_resendLink_with_other_auth_provider(self):
		user = self.create_test_user()
		user.auth_provider = 'google'
		user.save()
		res = self.client.post(self.resendLink_url, self.user_email, format='json')
		self.assertEqual(res.status_code, 403)


	def test_resendLink_with_valid_email(self):
		self.client.post(self.register_url, self.user_register_data, format="json")
		res = self.client.post(self.resendLink_url, self.user_email, format='json')
		self.assertEqual(res.status_code, 200)



class TestVerifyEmail(TestSetUp):

	def test_verifyEmail_with_invalid_token(self):
		res = self.client.get('/accounts/verify-email/token/')
		self.assertEqual(res.status_code, 404)


	def test_verifyEmail_with_valid_token(self):
		self.client.post(self.register_url, self.user_register_data, format="json")
		user = User.objects.get(email=self.user_register_data['email'])
		token, created = Token.objects.get_or_create(user=user)
		res = self.client.get('/accounts/verify-email/'+token.key+'/')
		verified_user = User.objects.get(email=self.user_register_data['email'])
		self.assertEqual(res.status_code, 201)
		self.assertTrue(verified_user.email_verified)


	def test_verifyEmail_with_valid_token_verified_email(self):
		user = self.create_test_user()
		token, created = Token.objects.get_or_create(user=user)
		res = self.client.get('/accounts/verify-email/'+token.key+'/')
		self.assertEqual(res.status_code, 200)
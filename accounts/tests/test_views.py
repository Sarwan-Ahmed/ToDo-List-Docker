"""Module to define test cases for Accounts views"""
from rest_framework.authtoken.models import Token
from utils.setup_test import TestSetUp
from accounts.models import User



class TestRegisterView(TestSetUp):
    """Test cases for account register view"""

    def test_register_without_data(self):
        """Account cannot be created without data"""
        res = self.client.post(self.register_url)
        self.assertEqual(res.status_code, 400)


    def test_register_with_without_email(self):
        """Account cannot be created without email"""
        del self.user_register_data['email']
        res = self.client.post(self.register_url, self.user_register_data, format="json")
        self.assertEqual(res.status_code, 400)


    def test_register_with_without_username(self):
        """Account cannot be created without username"""
        del self.user_register_data['username']
        res = self.client.post(self.register_url, self.user_register_data, format="json")
        self.assertEqual(res.status_code, 400)


    def test_register_with_without_password(self):
        """Account cannot be created without password"""
        del self.user_register_data['password']
        res = self.client.post(self.register_url, self.user_register_data, format="json")
        self.assertEqual(res.status_code, 400)


    def test_register_with_invalid_username(self):
        """Account cannot be created with non alphanumeric username"""
        self.user_register_data['username'] = 'new user'
        res = self.client.post(self.register_url, self.user_register_data, format="json")
        self.assertEqual(res.status_code, 400)


    def test_register_with_invalid_email(self):
        """Account cannot be created with invalid email"""
        self.user_register_data['email'] = 'abc@gmail'
        res = self.client.post(self.register_url, self.user_register_data, format="json")
        self.assertEqual(res.status_code, 400)


    def test_register_with_valid_data(self):
        """Account can only be created by providing valid data"""
        res = self.client.post(self.register_url, self.user_register_data, format="json")
        self.assertEqual(res.status_code, 201)


    def test_register_with_existing_email(self):
        """Account cannot be created with existing email"""
        self.client.post(self.register_url, self.user_register_data, format="json")
        self.user_register_data['username'] = 'user'
        res = self.client.post(self.register_url, self.user_register_data, format="json")
        self.assertEqual(res.status_code, 400)


    def test_register_with_existing_username(self):
        """Account cannot be created with existing username"""
        self.client.post(self.register_url, self.user_register_data, format="json")
        self.user_register_data['email'] = 'new@gmail.com'
        res = self.client.post(self.register_url, self.user_register_data, format="json")
        self.assertEqual(res.status_code, 400)



class TestLoginView(TestSetUp):
    """Test cases for account login view"""

    def test_login_without_data(self):
        """Account cannot be logged in without data"""
        res = self.client.post(self.login_url)
        self.assertEqual(res.status_code, 400)


    def test_login_without_email(self):
        """Account cannot be logged in without email"""
        self.create_test_user()
        del self.user_login_data['username']
        res = self.client.post(self.login_url, self.user_login_data, format="json")
        self.assertEqual(res.status_code, 400)


    def test_login_without_password(self):
        """Account cannot be logged in without password"""
        self.create_test_user()
        del self.user_login_data['password']
        res = self.client.post(self.login_url, self.user_login_data, format="json")
        self.assertEqual(res.status_code, 400)


    def test_login_with_invalid_email(self):
        """Account cannot be logged in with invalid email"""
        self.create_test_user()
        self.user_login_data['username'] = 'email'
        res = self.client.post(self.login_url, self.user_login_data, format="json")
        self.assertEqual(res.status_code, 400)


    def test_login_with_invalid_password(self):
        """Account cannot be logged in with invalid password"""
        self.create_test_user()
        self.user_login_data['password'] = 'password'
        res = self.client.post(self.login_url, self.user_login_data, format="json")
        self.assertEqual(res.status_code, 400)


    def test_login_with_unverified_email(self):
        """Account cannot be logged in with unverified email"""
        self.client.post(self.register_url, self.user_register_data, format="json")
        res = self.client.post(self.login_url, self.user_login_data, format="json")
        self.assertEqual(res.status_code, 401)


    def test_login_with_verified_email(self):
        """Account will be logged in with verified email"""
        self.create_test_user()
        res = self.client.post(self.login_url, self.user_login_data, format="json")
        self.assertEqual(res.status_code, 200)


    def test_login_without_email_authprovider(self):
        """Account cannot be logged in with auth provider other than email"""
        user = self.create_test_user()
        user.auth_provider = 'google'
        user.save()
        res = self.client.post(self.login_url, self.user_login_data, format="json")
        self.assertEqual(res.status_code, 401)


class TestLogoutView(TestSetUp):
    """Test cases for account logout view"""

    def test_logout_without_token(self):
        """User must provide it's unique token to logout itself"""
        res = self.client.post(self.logout_url)
        self.assertEqual(res.status_code, 401)


    def test_logout_with_invalid_token(self):
        """User must provide a valid token to logout itself"""
        res = self.client.post(self.logout_url, **{'HTTP_AUTHORIZATION':'token abcds'})
        self.assertEqual(res.status_code, 401)


    def test_logout_with_valid_token(self):
        """User will be logged out with valid token"""
        self.create_test_user()

        token = self.client.post(self.login_url, self.user_login_data,
                                format="json").data['token']

        res = self.client.post(self.logout_url, **{'HTTP_AUTHORIZATION':'token '+token})
        self.assertEqual(res.status_code, 200)


    def test_logout_with_already_logged_out(self):
        """User cannot logout more than once with same token"""
        self.create_test_user()

        token = self.client.post(self.login_url, self.user_login_data,
                                format="json").data['token']

        self.client.post(self.logout_url, **{'HTTP_AUTHORIZATION':'token '+token})
        res = self.client.post(self.logout_url, **{'HTTP_AUTHORIZATION':'token '+token})
        self.assertEqual(res.status_code, 401)



class TestResendLinkView(TestSetUp):
    """Test cases for resend verification link view"""

    def test_resend_link_without_data(self):
        """Verification link cannot be sent without providing email"""
        res = self.client.post(self.resendLink_url)
        self.assertEqual(res.status_code, 400)


    def test_resend_link_with_invalid_email(self):
        """Verification link cannot be sent with invalid email"""
        res = self.client.post(self.resendLink_url, self.user_email, format='json')
        self.assertEqual(res.status_code, 404)


    def test_resend_link_with_other_auth_provider(self):
        """Verification link can only be sent to account registered through email"""
        user = self.create_test_user()
        user.auth_provider = 'google'
        user.save()
        res = self.client.post(self.resendLink_url, self.user_email, format='json')
        self.assertEqual(res.status_code, 403)


    def test_resend_link_with_valid_email(self):
        """Verification link will only be sent to valid and registered email"""
        self.client.post(self.register_url, self.user_register_data, format="json")
        res = self.client.post(self.resendLink_url, self.user_email, format='json')
        self.assertEqual(res.status_code, 200)



class TestVerifyEmail(TestSetUp):
    """Test cases for account verify email view"""

    def test_verify_email_with_invalid_token(self):
        """Email cannot be verified with invalid token"""
        res = self.client.get('/accounts/verify-email/token/')
        self.assertEqual(res.status_code, 404)


    def test_verify_email_with_valid_token(self):
        """Email can only be verified with valid token"""
        self.client.post(self.register_url, self.user_register_data, format="json")
        user = User.objects.get(email=self.user_register_data['email'])
        token, created = Token.objects.get_or_create(user=user)
        res = self.client.get('/accounts/verify-email/'+token.key+'/')
        verified_user = User.objects.get(email=self.user_register_data['email'])
        self.assertEqual(res.status_code, 201)
        self.assertTrue(verified_user.email_verified)


    def test_verify_email_with_valid_token_verified_email(self):
        """Return already verified if email is verified"""
        user = self.create_test_user()
        token, created = Token.objects.get_or_create(user=user)
        res = self.client.get('/accounts/verify-email/'+token.key+'/')
        self.assertEqual(res.status_code, 200)

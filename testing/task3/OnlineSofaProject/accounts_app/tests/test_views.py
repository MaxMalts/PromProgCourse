from django.test import TestCase, Client
from django.urls import reverse
from django.core import mail
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.models import User
from accounts_app.models import RegistrationConfirmationByEmail


class SignUpViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.signup_url = reverse('signup')

    def test_get_signup_page(self):
        response = self.client.get(self.signup_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'signup.html')
    
    def test_get_signup_page_logged_in(self):
        User.objects.create_user(username='testuser', password='password123')
        self.client.login(username='testuser', password='password123')
        
        response = self.client.get(self.signup_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('home'))

    def test_signup_new_user(self):
        data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password': 'password123',
            'repeat_password': 'password123',
            'first_name': 'Test',
            'last_name': 'User'
        }
        response = self.client.post(self.signup_url, data=data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('activate_account'))

        self.assertTrue(User.objects.filter(username='testuser').exists())
        user = User.objects.get(username='testuser')
        self.assertEqual(user.email, 'testuser@example.com')
        self.assertEqual(user.first_name, 'Test')
        self.assertEqual(user.last_name, 'User')

        registration_attempt = RegistrationConfirmationByEmail.objects.get(user=user)
        self.assertFalse(registration_attempt.is_confirmed) 
        self.assertEqual(len(registration_attempt.activation_code), 30)

    def test_signup_password_mismatch(self):
        data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password': 'password123',
            'repeat_password': 'password1234',
            'first_name': 'Test',
            'last_name': 'User'
        }
        response = self.client.post(self.signup_url, data=data)
        self.assertTemplateUsed(response, 'signup.html')


class ResetPasswordViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.reset_password_url = reverse('password_reset')
        self.password_reset_done_url = reverse('password_reset_done')
        self.user = User.objects.create_user(username='testuser', email='testuser@example.com', password='password123')

    def test_get_signup_page(self):
        response = self.client.get(self.reset_password_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'password_reset.html')
    
    def test_get_signup_page_logged_in(self):
        self.client.login(username='testuser', password='password123')
        
        response = self.client.get(self.reset_password_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('home'))
    
    def test_reset_password_existing_user(self):
        response = self.client.post(self.reset_password_url, {'email': 'testuser@example.com'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(len(mail.outbox), 1)
        self.assertTemplateUsed(response, 'password_reset_email.html')
        self.assertEqual(mail.outbox[0].to, ['testuser@example.com'])
        self.assertRedirects(response, self.password_reset_done_url)

    def test_reset_password_nonexisting_user(self):
        response = self.client.post(self.reset_password_url, {'email': 'someemail@example.com'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'password_reset.html')
        self.assertContains(response, 'No user found with that email address.')

    def test_reset_password_email_contains_correct_uid_and_token(self):
        self.client.post(self.reset_password_url, {'email': 'testuser@example.com'})
        self.assertEqual(len(mail.outbox), 1)
        uid = urlsafe_base64_encode(force_bytes(self.user.pk))
        token = default_token_generator.make_token(self.user)
        self.assertIn(uid, mail.outbox[0].body)
        self.assertIn(token, mail.outbox[0].body)
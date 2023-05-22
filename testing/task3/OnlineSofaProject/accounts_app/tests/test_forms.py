from django.test import TestCase
from accounts_app.forms import ChangePasswordForm, RegisterForm

class RegisterFormTest(TestCase):
    def test_valid_form(self):
        form_data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password': 'testpassword',
            'repeat_password': 'testpassword',
            'first_name': 'Test',
            'last_name': 'User',
        }
        form = RegisterForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_blank_data(self):
        form = RegisterForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 6)
    
    def test_long_username(self):
        form_data = {
            'username': '1234567890123456789012345678901',
            'email': 'testuser@example.com',
            'password': 'testpassword',
            'repeat_password': 'testpassword',
            'first_name': 'Test',
            'last_name': 'User',
        }
        form = RegisterForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('username', form.errors)
    
    def test_no_username(self):
        form_data = {
            'username': '',
            'email': 'testuser@example.com',
            'password': 'testpassword',
            'repeat_password': 'testpassword',
            'first_name': 'Test',
            'last_name': 'User',
        }
        form = RegisterForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('username', form.errors)
        
    def test_short_email(self):
        form_data = {
            'username': 'testuser',
            'email': '1234567890123456789012345678901245678901',
            'password': 'testpassword',
            'repeat_password': 'testpassword',
            'first_name': 'Test',
            'last_name': 'User',
        }
        form = RegisterForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)
        
    def test_wrong_email(self):
        form_data = {
            'username': 'testuser',
            'email': 'sdkjfhasdf@',
            'password': 'testpassword',
            'repeat_password': 'testpassword',
            'first_name': 'Test',
            'last_name': 'User',
        }
        form = RegisterForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)
        
    def test_long_email(self):
        form_data = {
            'username': 'testuser',
            'email': 'tst',
            'password': 'testpassword',
            'repeat_password': 'testpassword',
            'first_name': 'Test',
            'last_name': 'User',
        }
        form = RegisterForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)
        
    def test_no_email(self):
        form_data = {
            'username': 'testuser',
            'email': '',
            'password': 'testpassword',
            'repeat_password': 'testpassword',
            'first_name': 'Test',
            'last_name': 'User',
        }
        form = RegisterForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)

    def test_short_password(self):
        form_data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password': 'pswd',
            'repeat_password': 'pswd',
            'first_name': 'Test',
            'last_name': 'User',
        }
        form = RegisterForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 2)
        self.assertIn('password', form.errors)
        self.assertIn('repeat_password', form.errors)

    def test_long_password(self):
        form_data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password': '123456789012345678901',
            'repeat_password': '123456789012345678901',
            'first_name': 'Test',
            'last_name': 'User',
        }
        form = RegisterForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 2)
        self.assertIn('password', form.errors)
        self.assertIn('repeat_password', form.errors)
    
    def test_no_password(self):
        form_data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password': '',
            'repeat_password': '',
            'first_name': 'Test',
            'last_name': 'User',
        }
        form = RegisterForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 2)
        self.assertIn('password', form.errors)
        self.assertIn('repeat_password', form.errors)

    def test_short_first_name(self):
        form_data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password': 'testpassword',
            'repeat_password': 'testpassword',
            'first_name': 'N',
            'last_name': 'User',
        }
        form = RegisterForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 1)
        self.assertIn('first_name', form.errors)
        
    def test_long_first_name(self):
        form_data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password': 'testpassword',
            'repeat_password': 'testpassword',
            'first_name': '123456789012345678901',
            'last_name': 'User',
        }
        form = RegisterForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 1)
        self.assertIn('first_name', form.errors)
    
    def test_no_first_name(self):
        form_data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password': 'testpassword',
            'repeat_password': 'testpassword',
            'first_name': '',
            'last_name': 'User',
        }
        form = RegisterForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 1)
        self.assertIn('first_name', form.errors)
    
    def test_long_last_name(self):
        form_data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password': 'testpassword',
            'repeat_password': 'testpassword',
            'first_name': 'Test',
            'last_name': '1234567890123456789012345678901',
        }
        form = RegisterForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 1)
        self.assertIn('last_name', form.errors)
    
    def test_no_last_name(self):
        form_data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password': 'testpassword',
            'repeat_password': 'testpassword',
            'first_name': 'Test',
            'last_name': '',
        }
        form = RegisterForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 1)
        self.assertIn('last_name', form.errors)


class ChangePasswordFormTest(TestCase):
    def test_valid_form(self):
        form_data = {
            'old_password': 'oldpassword',
            'new_password': 'newpassword'
        }
        form = ChangePasswordForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_blank_data(self):
        form = ChangePasswordForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 2)
    
    def test_long_old_password(self):
        form_data = {
            'old_password': '123456789012345678901',
            'new_password': 'newpassword'
        }
        form = ChangePasswordForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('old_password', form.errors)
    
    def test_short_old_password(self):
        form_data = {
            'old_password': 'p',
            'new_password': 'newpassword'
        }
        form = ChangePasswordForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('old_password', form.errors)
    
    def test_no_old_password(self):
        form_data = {
            'old_password': '',
            'new_password': 'newpassword'
        }
        form = ChangePasswordForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('old_password', form.errors)
    
    def test_long_new_password(self):
        form_data = {
            'old_password': 'oldpassword',
            'new_password': '123456789012345678901'
        }
        form = ChangePasswordForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('new_password', form.errors)
    
    def test_short_new_password(self):
        form_data = {
            'old_password': 'oldpassword',
            'new_password': 'p'
        }
        form = ChangePasswordForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('new_password', form.errors)
    
    def test_no_new_password(self):
        form_data = {
            'old_password': 'oldpassword',
            'new_password': ''
        }
        form = ChangePasswordForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('new_password', form.errors)
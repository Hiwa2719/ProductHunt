from django.test import TestCase
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.urls import reverse
from django.contrib.auth.models import User
from . import views

User = get_user_model()


class SignUpTestCase(TestCase):
    def test_getting_signup_page(self):
        """getting sign up page here"""
        response = self.client.get(reverse('signup'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.resolver_match.func.__name__, views.SignupView.as_view().__name__)
        self.assertTemplateUsed(response, 'account/signup.html')
        self.assertEqual(response.context['form'].__class__, UserCreationForm)
        self.assertContains(response, 'username')

    def test_posting_data_to_signup_page(self):
        """posting data to signup view"""
        response = self.client.post(reverse('signup'),
                                    {'username': 'hiwa@gmail.com', 'password1': 'HiWa_asdf', 'password2': 'HiWa_asdf'})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login'))
        self.assertEqual(response.resolver_match.func.__name__, views.SignupView.as_view().__name__)
        self.assertEqual(User.objects.get(pk=1).username, 'hiwa@gmail.com')


class LoginViewTestCase(TestCase):
    def test_getting_login_page(self):
        """test getting login page"""
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.resolver_match.func.__name__, views.LoginView.as_view().__name__)
        self.assertTemplateUsed(response, 'registration/login.html')
        self.assertEqual(response.context['form'].__class__, AuthenticationForm)
        self.assertContains(response, 'username')

    def test_posting_to_login_view(self):
        """posting to login view"""
        user = User.objects.create_user(username='hiwa@gmail.com', password='tests')
        response = self.client.post(reverse('login'), {'username': user.username, 'password': 'tests'})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('index'))
        self.assertIn('_auth_user_id', self.client.session)
        self.assertEqual(int(self.client.session.get('_auth_user_id')), user.id)

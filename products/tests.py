from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from . import views
from .models import Product

#  Unit tests

class ProductModelTestCase(TestCase):
    fixtures = ['fixtures/database.json']

    def setUp(self):
        self.user = User.objects.get(
            username='hiwa@gmail.com',
        )
        self.product = Product.objects.get(
            title='CPU'
        )

    # def test_creating_product(self):
    #     """test attaching hunter to a user work and also it adds the same user to vote field"""
    #     self.client.force_login(self.user)
    #     response = self.client.get('')
    #     print(response.request.user)
    #     instance = Product.objects.create(response.request, title='hello world', content='hey you')
    #     self.assertEqual(self.user, instance.hunter)
    #     self.assertIn(self.user, instance.vote.all())

    def test_vote_check(self):
        """testing if vote_check method works properly"""
        self.product.vote_check(user=self.user)
        self.assertNotIn(self.user, self.product.vote.all())
        self.product.vote_check(user=self.user)
        self.assertIn(self.user, self.product.vote.all())


class IndexViewTestCase(TestCase):
    fixtures = ['fixtures/database.json']

    def test_getting_index_view(self):
        """getting products list"""
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.resolver_match.func.__name__, views.IndexView.as_view().__name__)
        self.assertTemplateUsed(response, 'products/index.html')
        self.assertIn('product_list', response.context)
        # content_str = str(response.content, encoding='utf-8')
        # self.assertIn('CPU', content_str)
        self.assertContains(response, 'CPU')



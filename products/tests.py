from django.contrib.auth.models import User
from django.test import TestCase

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

    def test_vote_check(self):
        """testing if vote_check method works properly"""
        self.product.vote_check(user=self.user)
        self.assertIn(self.user, self.product.vote.all())
        self.product.vote_check(user=self.user)
        self.assertNotIn(self.user, self.product.vote.all())


class IndexViewTestCase(TestCase):
    def setUp(self) -> None:
        pass

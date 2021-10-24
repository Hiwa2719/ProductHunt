from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from . import views
from .forms import ProductCreateForm
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


class ProductDetailViewTestCase(TestCase):
    fixtures = ['fixtures/database.json']

    def test_getting_a_product_detail(self):
        """getting detail of a product"""
        product = Product.objects.get(pk=2)
        response = self.client.get(reverse('products:product-detail', kwargs={'pk': 2}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.resolver_match.func.__name__, views.ProductDetailView.as_view().__name__)
        self.assertTemplateUsed(response, 'products/product_detail.html')
        self.assertIn('product', response.context)
        self.assertContains(response, product.title)


class ProductCreateViewTestCase(TestCase):
    fixtures = ['fixtures/database.json']

    def force_login(self):
        self.client.login(username='hiwa@gmail.com', password='asdf')

    def test_getting_product_create_page_by_anonymous_user(self):
        response = self.client.get(reverse('products:create-product'), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, reverse('login') + '?next=' + reverse('products:create-product'))

    def test_getting_to_product_create_page(self):
        """test getting create form"""
        self.force_login()
        response = self.client.get(reverse('products:create-product'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.resolver_match.func.__name__, views.ProductCreateView.as_view().__name__)
        self.assertTemplateUsed(response, 'products/product_form.html')
        self.assertIn('form', response.context)
        self.assertEqual(response.context['form'].__class__, ProductCreateForm)
        self.assertIn('input_val', response.context)
        self.assertContains(response, 'title')

    def test_posting_product_data_to_Product_create_view(self):
        """examining creating new product"""
        self.force_login()
        response = self.client.post(reverse('products:create-product'),
                                    {'title': 'your cv', 'content': 'this place is hell'})
        self.assertEqual(response.status_code, 302)
        product = Product.objects.get(title='your cv')
        self.assertEqual(product.content, 'this place is hell')

    def test_redirecting_after_creating_product(self):
        """test redirecting after creation"""
        self.force_login()
        response = self.client.post(reverse('products:create-product'),
                                    {'title': 'your cv', 'content': 'this place is hell'}, follow=True)
        self.assertEqual(response.status_code, 200)
        product = Product.objects.get(title__iexact='your cv')
        self.assertRedirects(response, reverse('products:product-detail', kwargs={'pk': product.pk}))


class ProductUpdateViewTestCase(TestCase):
    fixtures = ['fixtures/database.json']

    def force_login(self):
        self.client.login(username='hiwa@gmail.com', password='asdf')

    def test_redirecting_for_anonymous_user(self):
        """testing if anonymous user being redirected"""
        response = self.client.get(reverse('products:product-update', kwargs={'pk': 2}), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response,
                             reverse('login') + '?next=' + reverse('products:product-update', kwargs={'pk': 2}))

    def test_getting_update_page(self):
        """test getting update page of product with pk 2"""
        product = Product.objects.get(pk=2)
        self.force_login()
        response = self.client.get(reverse('products:product-update', kwargs={'pk': 2}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.resolver_match.func.__name__, views.ProductUpdateView.as_view().__name__)
        self.assertTemplateUsed(response, 'products/product_form.html')
        self.assertIn('form', response.context)
        self.assertEqual(response.context['form'].__class__, ProductCreateForm)
        self.assertContains(response, product.title)

    def test_updating_title(self):
        """test updating product title"""
        self.force_login()
        product = Product.objects.get(pk=2)
        response = self.client.post(reverse('products:product-update', kwargs={'pk': 2}),
                                    {'title': 'intel CPU', 'content': product.content})
        self.assertEqual(response.status_code, 302)
        product.refresh_from_db()
        self.assertEqual(product.title, 'intel CPU')

    def test_redirecting(self):
        """test redirecting url"""
        self.force_login()
        product = Product.objects.get(pk=2)
        response = self.client.post(reverse('products:product-update', kwargs={'pk': 2}),
                                    {'title': 'intel CPU', 'content': product.content}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, reverse('products:product-detail', kwargs={'pk': 2}))
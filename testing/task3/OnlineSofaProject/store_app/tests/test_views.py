from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from store_app.models import Product, WarehouseProducts, CartUser
import json


class AddProductToCartViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.product = Product.objects.create(title='Test Product', price=10.0)
        self.warehouse_product = WarehouseProducts.objects.create(product=self.product, count_products=10)
        self.cart_user = CartUser.objects.create(user=self.user)
        self.url = reverse('add_product_to_basket')

    def test_add_product_to_cart(self):
        self.client.login(username='testuser', password='password123')
        data = {'product_id': self.product.id, 'count_product': 2}
        response = self.client.post(self.url, data=data)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content)['status'], 'OK')
        self.assertEqual(self.cart_user.products.count(), 1)
        self.assertEqual(self.cart_user.products.first(), self.product)
        self.assertEqual(self.cart_user.productincart_set.first().count_product_in_cart, 2)
        
        self.warehouse_product.refresh_from_db()
        self.assertEqual(self.warehouse_product.count_products, 8)

    def test_add_product_to_cart_more_than_available(self):
        self.client.login(username='testuser', password='password123')
        data = {'product_id': self.product.id, 'count_product': 11}
        response = self.client.post(self.url, data=data)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content)['status'], 'MORE')
        self.assertEqual(self.cart_user.products.count(), 0)
        
        self.warehouse_product.refresh_from_db()
        self.assertEqual(self.warehouse_product.count_products, 10)

    def test_add_product_to_cart_anonymous_user(self):
        data = {'product_id': self.product.id, 'count_product': 2}
        response = self.client.post(self.url, data=data)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content)['status'], 'BAD')
        self.assertEqual(self.cart_user.products.count(), 0)
        
        self.warehouse_product.refresh_from_db()
        self.assertEqual(self.warehouse_product.count_products, 10)

    def test_add_product_to_cart_existing_cart(self):
        self.client.login(username='testuser', password='password123')
        self.cart_user.products.add(self.product)
        
        data = {'product_id': self.product.id, 'count_product': 3}
        response = self.client.post(self.url, data=data)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content)['status'], 'OK')
        self.assertEqual(self.cart_user.products.count(), 1)
        self.assertEqual(self.cart_user.products.first(), self.product)
        self.assertEqual(self.cart_user.productincart_set.first().count_product_in_cart, 3)
        
        self.warehouse_product.refresh_from_db()
        self.assertEqual(self.warehouse_product.count_products, 7)

    def test_add_product_to_cart_new_cart(self):
        self.client.login(username='testuser', password='password123')
        self.cart_user.delete()
        
        data = {'product_id': self.product.id, 'count_product': 2}
        response = self.client.post(self.url, data=data)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content)['status'], 'OK')
        
        cart_user = CartUser.objects.filter(user=self.user)
        self.assertEqual(len(cart_user), 1)
        cart_user = cart_user[0]
        
        self.assertEqual(cart_user.products.count(), 1)
        self.assertEqual(cart_user.productincart_set.count(), 1)
        self.assertEqual(cart_user.products.first(), self.product)
        self.assertEqual(cart_user.productincart_set.first().count_product_in_cart, 2)
        
        self.warehouse_product.refresh_from_db()
        self.assertEqual(self.warehouse_product.count_products, 8)
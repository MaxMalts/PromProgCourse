# from django.test import TestCase, Client
# from django.urls import reverse
# from store_app.models import Order
# import json

# class GetSalesAnalyticsViewTestCase(TestCase):
#     def setUp(self):
#         self.client = Client()
#         self.url = reverse('get_sales_analytics')
#         self.order1 = Order.objects.create(customer_name='Name1', total_price=10)
#         self.order2 = Order.objects.create(customer_name='Name2', total_price=20)

#     def test_get_sales_analytics_view_with_permission(self):
#         response = self.client.get(self.url)
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'get_sales_analytics.html')

#     def test_get_sales_analytics_view_without_permission(self):
#         self.client.login(username='user', password='password')
#         response = self.client.get(self.url)
#         self.assertEqual(response.status_code, 403)

#     def test_get_sales_analytics_view_with_data(self):
#         response = self.client.get(self.url)
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'get_sales_analytics.html')
#         self.assertContains(response, 'sold_products_for_period')
#         self.assertContains(response, 'json_data')
#         json_data = json.loads(response.context['json_data'])
#         self.assertEqual(len(json_data), 2)
#         self.assertEqual(len(json_data[0]), 2)
#         self.assertEqual(len(json_data[1]), 2)

#     def test_get_sales_analytics_view_with_no_data(self):
#         Order.objects.all().delete()
#         response = self.client.get(self.url)
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'get_sales_analytics.html')
#         self.assertContains(response, 'sold_products_for_period')
#         self.assertContains(response, 'json_data')
#         json_data = json.loads(response.context['json_data'])
#         self.assertEqual(len(json_data), 2)
#         self.assertEqual(len(json_data[0]), 0)
#         self.assertEqual(len(json_data[1]), 0)

#     def test_get_sales_analytics_view_with_exception(self):
#         Order.objects.all().delete()
#         response = self.client.get(self.url)
#         self.assertEqual(response.status_code, 302)
#         self.assertRedirects(response, reverse('home'))







from django.test import TestCase, Client
from django.urls import reverse
from store_app.models import Order, Recipient
import json
import datetime

class GetSalesAnalyticsViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('get_sales_analytics')

    def test_get_sales_analytics_view_one_order(self):
        self.order = Order.objects.create(num_order='123', recipient=Recipient.objects.create(name_recipient="Name"), total_sum=100)
        
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'get_sales_analytics.html')
        
        sold_products_for_period = response.context['sold_products_for_period']
        self.assertEqual(len(sold_products_for_period), 1)
        self.assertEqual(sold_products_for_period[str(datetime.date.today().strftime('%d.%m.%Y'))], 1)
        
        json_data = json.loads(response.context['json_data'])
        self.assertEqual(len(json_data), 2)
        self.assertEqual(json_data[0][0], str(datetime.date.today().strftime('%d.%m.%Y')))
        self.assertEqual(json_data[1][0], 1)
        
        self.assertContains(response, '<th>Дата</th>')
        self.assertContains(response, '<th>Количество проданных товаров</th>')
        self.assertContains(response, '<td>' + datetime.date.today().strftime('%d.%m.%Y') + '</td>')
        self.assertContains(response, '<td>1</td>')


    def test_get_sales_analytics_view_multiple_orders(self):
        self.order = Order.objects.create(num_order='123', recipient=Recipient.objects.create(name_recipient="Name1"), total_sum=100)
        self.order = Order.objects.create(num_order='456', recipient=Recipient.objects.create(name_recipient="Name2"), total_sum=200)
        self.order = Order.objects.create(num_order='789', recipient=Recipient.objects.create(name_recipient="Name1"), total_sum=200)
        
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'get_sales_analytics.html')
        
        sold_products_for_period = response.context['sold_products_for_period']
        self.assertEqual(len(sold_products_for_period), 1)
        self.assertEqual(sold_products_for_period[str(datetime.date.today().strftime('%d.%m.%Y'))], 3)
        
        json_data = json.loads(response.context['json_data'])
        self.assertEqual(len(json_data), 2)
        self.assertEqual(json_data[0][0], str(datetime.date.today().strftime('%d.%m.%Y')))
        self.assertEqual(json_data[1][0], 3)
        
        self.assertContains(response, '<th>Дата</th>')
        self.assertContains(response, '<th>Количество проданных товаров</th>')
        self.assertContains(response, '<td>' + datetime.date.today().strftime('%d.%m.%Y') + '</td>')
        self.assertContains(response, '<td>3</td>')
    
    def test_get_sales_analytics_view_no_orders(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'get_sales_analytics.html')
        self.assertEqual(response.context['sold_products_for_period'], {})
        self.assertEqual(response.context['json_data'], '[]')
        self.assertContains(response, '<th>Дата</th>')
        self.assertContains(response, '<th>Количество проданных товаров</th>')
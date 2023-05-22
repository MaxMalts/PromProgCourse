from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from rolepermissions.roles import assign_role
from store_app.models import Product, WarehouseProducts, FeedBackWithClient
from online_store_on_sofa_project.roles import OperatorCallCenter, ContentManager, TopManager


class CommonGetTests:
    def setUp(self):
        self.client = Client()
        User.objects.create_user(username='testuser', password='password123')
        assign_role(User.objects.create_user(username='operator_call_center', password='password123'), OperatorCallCenter)
        assign_role(User.objects.create_user(username='content_manager', password='password123'), ContentManager)
        assign_role(User.objects.create_user(username='top_manager', password='password123'), TopManager)
        self.product = Product.objects.create(title='Test Product', price=10.0, description='Test Description')
    
    def test_client_access_to_view_get(self):
        self.client.login(username='testuser', password='password123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200 if self.client_has_get_permission else 403)

    def test_operator_call_center_access_to_view_get(self):
        self.client.login(username='operator_call_center', password='password123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200 if self.operator_call_center_has_get_permission else 403)

    def test_content_manager_access_to_view_get(self):
        self.client.login(username='content_manager', password='password123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200 if self.content_manager_has_get_permission else 403)

    def test_top_manager_access_to_view_get(self):
        self.client.login(username='top_manager', password='password123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200 if self.top_manager_has_get_permission else 403)


class CommonPostTests:
    def setUp(self):
        self.client = Client()
        User.objects.create_user(username='testuser', password='password123')
        assign_role(User.objects.create_user(username='operator_call_center', password='password123'), OperatorCallCenter)
        assign_role(User.objects.create_user(username='content_manager', password='password123'), ContentManager)
        assign_role(User.objects.create_user(username='top_manager', password='password123'), TopManager)
        self.product = Product.objects.create(title='Test Product', price=10.0, description='Test Description')
    
    def test_client_access_to_view_post(self):
        self.client.login(username='testuser', password='password123')
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 200 if self.client_has_post_permission else 403)

    def test_operator_call_center_access_to_view_post(self):
        self.client.login(username='operator_call_center', password='password123')
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 200 if self.operator_call_center_has_post_permission else 403)

    def test_content_manager_access_to_view_post(self):
        self.client.login(username='content_manager', password='password123')
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 200 if self.content_manager_has_post_permission else 403)

    def test_top_manager_access_to_view_post(self):
        self.client.login(username='top_manager', password='password123')
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 200 if self.top_manager_has_post_permission else 403)


class ChangeInfoProductViewAccessTestCase(CommonGetTests, TestCase):
    def setUp(self):
        super().setUp()
        self.client_has_get_permission = False
        self.operator_call_center_has_get_permission = False
        self.content_manager_has_get_permission = True
        self.top_manager_has_get_permission = True
        
        self.url = reverse('change_info_product')


class AddCountReceivedProductToWarehouseViewAccessTestCase(CommonGetTests, CommonPostTests, TestCase):
    def setUp(self):
        super().setUp()
        self.client_has_get_permission = False
        self.operator_call_center_has_get_permission = False
        self.content_manager_has_get_permission = True
        self.top_manager_has_get_permission = True
        
        self.client_has_post_permission = False
        self.operator_call_center_has_post_permission = False
        self.content_manager_has_post_permission = True
        self.top_manager_has_post_permission = True
        
        WarehouseProducts.objects.create(product=self.product, count_products=2)
        self.url = reverse('add_count_received_product_to_warehouse', args=[self.product.pk])
    
    def test_content_manager_access_to_view_post(self):
        self.client.login(username='content_manager', password='password123')
        response = self.client.post(self.url, data={'count_prod': '2'})
        self.assertEqual(response.status_code, 302)

    def test_top_manager_access_to_view_post(self):
        self.client.login(username='top_manager', password='password123')
        response = self.client.post(self.url, data={'count_prod': '2'})
        self.assertEqual(response.status_code, 302)


class AddImagesForProductViewAccessTestCase(CommonGetTests, CommonPostTests, TestCase):
    def setUp(self):
        super().setUp()
        self.client_has_get_permission = False
        self.operator_call_center_has_get_permission = False
        self.content_manager_has_get_permission = True
        self.top_manager_has_get_permission = True
        
        self.client_has_post_permission = False
        self.operator_call_center_has_post_permission = False
        self.content_manager_has_post_permission = True
        self.top_manager_has_post_permission = True
        
        self.url = reverse('add_images_for_product')
        
    def test_content_manager_access_to_view_post(self):
        self.client.login(username='content_manager', password='password123')
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 302)

    def test_top_manager_access_to_view_post(self):
        self.client.login(username='top_manager', password='password123')
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 302)


class AddNewProductsViewAccessTestCase(CommonGetTests, CommonPostTests, TestCase):
    def setUp(self):
        super().setUp()
        self.client_has_get_permission = False
        self.operator_call_center_has_get_permission = False
        self.content_manager_has_get_permission = True
        self.top_manager_has_get_permission = True
        
        self.client_has_post_permission = False
        self.operator_call_center_has_post_permission = False
        self.content_manager_has_post_permission = True
        self.top_manager_has_post_permission = True
        
        self.url = reverse('add_new_products')
    
    def test_content_manager_access_to_view_post(self):
        self.client.login(username='content_manager', password='password123')
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 302)

    def test_top_manager_access_to_view_post(self):
        self.client.login(username='top_manager', password='password123')
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 302)
    

class ChangeCharacteristicsProductViewAccessTestCase(CommonGetTests, CommonPostTests, TestCase):
    def setUp(self):
        super().setUp()
        self.client_has_get_permission = False
        self.operator_call_center_has_get_permission = False
        self.content_manager_has_get_permission = True
        self.top_manager_has_get_permission = True
        
        self.client_has_post_permission = False
        self.operator_call_center_has_post_permission = False
        self.content_manager_has_post_permission = True
        self.top_manager_has_post_permission = True
        
        self.url = reverse('change_characteristics_product', args=[self.product.pk])
        
    def test_content_manager_access_to_view_post(self):
        self.client.login(username='content_manager', password='password123')
        response = self.client.post(self.url, data={'title': 'sometitle', 'brand': 'somebrand'})
        self.assertEqual(response.status_code, 302)

    def test_top_manager_access_to_view_post(self):
        self.client.login(username='top_manager', password='password123')
        response = self.client.post(self.url, data={'title': 'sometitle', 'brand': 'somebrand'})
        self.assertEqual(response.status_code, 302)


class CheckRequestsFeedbackViewAccessTestCase(CommonGetTests, TestCase):
    def setUp(self):
        super().setUp()
        self.client_has_get_permission = False
        self.operator_call_center_has_get_permission = True
        self.content_manager_has_get_permission = False
        self.top_manager_has_get_permission = True
        
        self.url = reverse('feedback_with_clients')


class GetSalesAnalyticsViewAccessTestCase(CommonGetTests, TestCase):
    def setUp(self):
        super().setUp()
        self.client_has_get_permission = False
        self.operator_call_center_has_get_permission = False
        self.content_manager_has_get_permission = False
        self.top_manager_has_get_permission = True
        
        self.url = reverse('get_sales_analytics')


class SendAnswerToClientFeedbackRequestViewAccessTestCase(CommonPostTests, TestCase):
    def setUp(self):
        super().setUp()
        self.client_has_post_permission = False
        self.operator_call_center_has_post_permission = True
        self.content_manager_has_post_permission = False
        self.top_manager_has_post_permission = True
        
        self.feedback_with_client = FeedBackWithClient.objects.create(
            name_client='clientname',
            email_client='client@example.com',
            question_client='some question from the client'
        )
        self.url = reverse('response_to_request_feedback')
    
    def test_operator_call_center_access_to_view_post(self):
        self.client.login(username='operator_call_center', password='password123')
        response = self.client.post(self.url, data={'request_feedback_id': self.feedback_with_client.id, 'text_answer': 'sometextanswer'})
        self.assertEqual(response.status_code, 200 if self.operator_call_center_has_post_permission else 403)
    
    def test_top_manager_access_to_view_post(self):
        self.client.login(username='top_manager', password='password123')
        response = self.client.post(self.url, data={'request_feedback_id': self.feedback_with_client.id, 'text_answer': 'sometextanswer'})
        self.assertEqual(response.status_code, 200 if self.top_manager_has_post_permission else 403)
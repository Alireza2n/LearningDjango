from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


class MyOrdersViewTestCase(TestCase):
    """
    Tests My orders view
    """

    def setUp(self) -> None:
        pass

    def test_auth_required(self):
        """
        Tests if view redirects anonymous user to login page
        """
        response = self.client.get(reverse('store:list-orders'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login/', response.url)

        response = self.client.get(reverse('store:list-orders'), follow=True)
        self.assertContains(response, 'Please login')

    def test_empty_order_history_for_user(self):
        """
        A new user should see an empty history
        """
        user = get_user_model().objects.create(username='user1')
        self.client.force_login(user=user)
        response = self.client.get(reverse('store:list-orders'))
        self.assertContains(response, 'تاریخ سفارش')
        self.assertEqual(response.context_data['paginator'].count, 0)
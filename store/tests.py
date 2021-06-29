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

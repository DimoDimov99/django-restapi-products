from django.urls import reverse
from django.test import TestCase
from api.models import Order, User
from rest_framework import status

# Object.objects.create(**payload)


# Create your tests here.
class UserOrderTestCase(TestCase):
    def setUp(self):
        user_01 = User.objects.create_user(username="user_01", password="test_01")
        user_02 = User.objects.create_user(username="user_02", password="test_02")
        Order.objects.create(user=user_01)
        Order.objects.create(user=user_01)
        Order.objects.create(user=user_02)
        Order.objects.create(user=user_02)

    def test_user_order_api_retrieves_only_auth_user_orders(self):
        dummy_user_01 = User.objects.get(username="user_01")
        self.client.force_login(dummy_user_01)
        response = self.client.get(reverse("user-orders"))

        assert response.status_code == status.HTTP_200_OK
        orders = response.json()
        self.assertTrue(all(order["user"] == dummy_user_01.id for order in orders))

    def test_user_order_list_unath(self):
        response = self.client.get(reverse("user-orders"))
        """
        The request was successfully authenticated, but permission was denied. — An HTTP 403 Forbidden response will be returned.
        The request was not successfully authenticated, and the highest priority authentication class does not use WWW-Authenticate headers. — An HTTP 403 Forbidden response will be returned.
        The request was not successfully authenticated, and the highest priority authentication class does use WWW-Authenticate headers. — An HTTP 401 Unauthorized response, with an appropriate WWW-Authenticate header will be returned.
        """
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        response_text = response.json().get("detail")
        self.assertEqual(
            response_text,
            "Authentication credentials were not provided.",
        )

    def test_get_auth_token_of_admin(self):
        admin_user = User.objects.create_superuser(username="admin", password="test")
        payload = {"username": "admin", "password": "test"}
        response = self.client.post(reverse("token_obtain_pair"), data=payload)
        auth_token = response.json()["access"]
        print(auth_token)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

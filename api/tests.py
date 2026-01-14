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
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response_text = response.json().get("detail")
        self.assertEqual(
            response_text,
            "Authentication credentials were not provided.",
        )

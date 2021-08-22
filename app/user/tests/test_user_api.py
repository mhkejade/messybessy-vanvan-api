from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status


CREATE_USER_URL = reverse('user:create')


def create_user(**params):
    return get_user_model().objects.create_user(**params)


class PublicUserApiTests(TestCase):
    """test public user api"""

    def setUp(self):
        self.client = APIClient()

    def test_create_valid_user_success(self):
        """test creating user with valid params/payload is successful"""
        payload = {
            'email': 'mike@test.com',
            'password': 'testpassword',
            'name': 'mike test'
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**res.data)
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)

    def test_user_exists(self):
        """test creating a user that already exists should fail"""
        payload = {
            'email': 'mike@test.com',
            'password': 'testpassword',
            'name': 'mike test'
        }
        create_user(**payload)

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        """test that password is more than 5 characters"""
        payload = {
            'email': 'mike@test.com',
            'password': 'test',
            'name': 'mike test'
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()
        self.assertFalse(user_exists)
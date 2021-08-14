from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTests(TestCase):

    def test_create_user_with_email_successful(self):
        """test creating user with email is successful"""
        email = 'test@vanvan.com'
        password = '1234567890'
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """email of new user should be normalized"""
        email = 'mike.bengil@GMail.com'
        user = get_user_model().objects.create_user(email, 'testpassword')

        self.assertEqual(user.email, email.lower())

    def test_new_user_email_isprovided(self):
        """email should be provided"""
        with self.assertRaises(ValueError):
            email = None
            get_user_model().objects.create_user(email, 'testpassword')

    def test_create_new_superuser(self):
        """test creating new superuser"""
        user = get_user_model().objects.create_superuser(
            'mike@superuser.com',
            'superuserpassword'
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

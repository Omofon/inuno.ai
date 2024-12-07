from django.test import TestCase
from .models import CustomUser

# Create your tests here.


class TestCustomUserModel(TestCase):
    def setUp(self):

        self.user01 = CustomUser.objects.create_user(
            username="user01",
            email="user01@example.com",
            first_name="User",
            last_name="One",
        )
        self.user01.set_password
        ("password123")
        self.user01.save()

        self.user02 = CustomUser.objects.create_user(
            username="user02",
            email="user02@example.com",
            first_name="User",
            last_name="Two",
        )
        self.user01.set_password
        ("sample123")
        self.user01.save()

    def test_user_saved_successfully(self):
        """Testing fi the user was succeffully created."""
        user1 = CustomUser.objects.get(username="user01")
        user2 = CustomUser.objects.get(last_name="Two")

        self.assertEqual(user1.first_name, self.user01.first_name)
        self.assertFalse(user2.is_superuser)

    def test_str_method(self):
        """Testing the __str__ method of the CustomUser model."""
        self.assertEqual(str(self.user01), "user01")
        self.assertEqual(str(self.user02), "user02")

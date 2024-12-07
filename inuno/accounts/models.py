from django.db import models
from django.urls import reverse
from django.contrib.auth.models import AbstractUser


# Create your models here.
class CustomUser(AbstractUser):
    """Model for users."""

    email = models.EmailField(unique=True)

    def __str__(self):
        return self.username

    def promote_to_staff(self):
        """
        Promote a user to staff (admin) status.
        """
        self.is_staff = True
        self.save()

    def get_absolute_url(self):
        return reverse("user_profile", kwargs={"pk": self.pk})

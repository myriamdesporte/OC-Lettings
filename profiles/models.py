"""Models of the profiles application."""

from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    """User profile storing the user's favorite city."""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    favorite_city = models.CharField(max_length=64, blank=True)

    def __str__(self):
        """Return the username of the related user."""
        return self.user.username

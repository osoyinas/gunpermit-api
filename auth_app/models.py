from django.contrib.auth.models import AbstractUser
from django.db import models

AUTH_PROVIDERS = {
    "google": "google",
    "email": "email",
    "github": "github",
}


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    auth_provider = models.CharField(
        max_length=255, blank=False, null=False, default=AUTH_PROVIDERS.get("email")
    )
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]  # removes username from REQUIRED_FIELDS

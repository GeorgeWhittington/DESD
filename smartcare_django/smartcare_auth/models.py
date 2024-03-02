from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    USER_TYPE_CHOICES = (
        (0, "superuser"),
        (1, "admin"),
        (2, "doctor"),
        (3, "nurse"),
        (4, "patient"),
        (5, "external")
    )

    user_type = models.PositiveSmallIntegerField(choices=USER_TYPE_CHOICES, null=True)


# class Patient(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
#     # additional fields specifically for patient data
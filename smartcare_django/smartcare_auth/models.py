from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

from .validators import UnicodeNoEmailUsernameValidator

class User(AbstractUser):
    USER_TYPE_CHOICES = (
        (0, "superuser"),
        (1, "admin"),
        (2, "doctor"),
        (3, "nurse"),
        (4, "patient"),
        (5, "external")
    )

    username_validator = UnicodeNoEmailUsernameValidator()

    username = models.CharField(
        _("username"),
        max_length=150,
        unique=True,
        help_text=_(
            "Required. 150 characters or fewer. Letters, digits and ./+/-/_ only."
        ),
        validators=[username_validator],
        error_messages={
            "unique": _("A user with that username already exists."),
        },
    )
    email = models.EmailField(_("email address"), blank=True, unique=True)
    user_type = models.PositiveSmallIntegerField(choices=USER_TYPE_CHOICES, null=True)


# class Patient(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
#     # additional fields specifically for patient data
from enum import IntEnum
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

from .validators import UnicodeNoEmailUsernameValidator


class UserType(IntEnum):
    SUPERUSER = 0
    ADMIN = 1
    DOCTOR = 2
    NURSE = 3
    EXTERNAL = 4
    PATIENT = 5

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]

class EmploymentType(models.TextChoices):
    FULL_TIME = 'FT', _('Full Time')
    PART_TIME = 'PT', _('Part Time')


class User(AbstractUser):
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
    user_type = models.PositiveSmallIntegerField(choices=UserType.choices(), null=False, default=0)
    employment_type = models.CharField(max_length=2, choices=EmploymentType.choices, null=True, blank=True)

    def is_clinic_staff(self):
        return self.is_staff or (self.user_type is not None and self.user_type <= 3)
    
    def is_full_time(self):
        return self.employment_type == EmploymentType.FULL_TIME
    
    def is_part_time(self):
        return self.employment_type == EmploymentType.PART_TIME

    def full_name(self):
        return f"{self.first_name} {self.last_name}"


'''class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='patient_info')
    first_name = models.TextField(blank=True, null=True)
    last_name = models.TextField(blank=True, null=True)
'''
    
    # additional fields specifically for patient data
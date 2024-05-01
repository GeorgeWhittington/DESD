from enum import IntEnum
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, RegexValidator, MinLengthValidator

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
    phone_number = models.CharField(max_length=14, null=True, blank=True, validators=[RegexValidator("^[\d -]*$", "Phone numbers cannot contain values other than digits and hyphens"), MinLengthValidator(3, "Phone numbers must be atleast 3 digits long")])
    user_type = models.PositiveSmallIntegerField(choices=UserType.choices(), null=False, default=0)
    date_of_birth = models.DateField(null=True, blank=True)

    address_line_1 = models.CharField(max_length=50, blank=True, null=True, validators=[MinLengthValidator(1, "City/Town field cannot be empty")])
    address_line_2 = models.CharField(max_length=50, blank=True, null=True)
    city = models.CharField(max_length=30, blank=True, null=True, validators=[RegexValidator("^\D+$", "City/Town names cannot include digits"), MinLengthValidator(1, "City/Town field cannot be empty")])
    postcode = models.CharField(max_length=7, blank=True, null=True, validators=[RegexValidator("^[0-9a-zA-Z]{5,7}$", "Please enter a valid postcode which is 5 to 7 characters long")])

    def is_clinic_admin(self):
        return self.is_staff or (self.user_type is not None and self.user_type == UserType.ADMIN)

    def is_clinic_staff(self):
        return self.is_staff or (self.user_type is not None and self.user_type <= UserType.NURSE)

    def is_clinic_or_external_staff(self):
        allowed = [UserType.ADMIN, UserType.DOCTOR, UserType.NURSE, UserType.EXTERNAL]
        return self.is_staff or (self.user_type is not None and self.user_type in allowed)

    def is_full_time(self):
        return self.employment_type == EmploymentType.FULL_TIME

    def is_part_time(self):
        return self.employment_type == EmploymentType.PART_TIME

    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return self.full_name() if self.first_name and self.last_name else self.username


class EmploymentType(models.TextChoices):
    FULL_TIME = 'FT', _('Full Time')
    PART_TIME = 'PT', _('Part Time')


class PayRate(models.Model):
    title = models.CharField(max_length=150, unique=True, null=False)
    rate = models.FloatField(null=False, validators=[MinValueValidator(0.01)])

    def __str__(self):
        return f"{self.title}: £{self.rate:.2f}/h"


class StaffInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='staff_info')
    employment_type = models.CharField(max_length=2, choices=EmploymentType.choices, blank=True, null=True)
    payrate = models.ForeignKey(PayRate, null=True, on_delete=models.CASCADE, related_name="staff_payrate")

    def __str__(self):
        return f"{self.user.full_name()}"

    def is_full_time(self):
        return self.employment_type == EmploymentType.FULL_TIME.value

    def is_part_time(self):
        return self.employment_type == EmploymentType.PART_TIME.value


class PatientPayType(IntEnum):
    PRIVATE = 0
    NHS = 1

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]


class PatientInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name="patient_info")
    pay_type = models.PositiveSmallIntegerField(choices=PatientPayType.choices(), null=False, default=0)


class PasswordReset(models.Model):
    email = models.EmailField()
    token = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
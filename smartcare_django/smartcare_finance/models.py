from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.core.validators import MinValueValidator

from smartcare_auth.models import UserType
from smartcare_appointments.models import Appointment, AppointmentStage

# Hourly rate (move this to an actual table)
NURSE_RATE = 30.0
DOCTOR_RATE = 40.0


class Invoice(models.Model):
    appointment = models.OneToOneField(Appointment, null=False, on_delete=models.CASCADE, related_name="invoice_appointment")

    duration = models.DurationField(null=False)
    amount = models.FloatField(null=False, validators=[MinValueValidator(0.01)])
    is_paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    paid_at = models.DateTimeField(null=True)

    def fill_extra_fields(self):
        if not hasattr(self, "appointment") or self.appointment.stage != AppointmentStage.COMPLETED:
            raise ValidationError("An completed appointment must be provided")

        duration = self.appointment.actual_end_time - self.appointment.actual_start_time

        # TODO: fetch this from the database, properly
        if self.appointment.staff.user_type == UserType.NURSE:
            rate = NURSE_RATE
        elif self.appointment.staff.user_type == UserType.DOCTOR:
            rate = DOCTOR_RATE
        else:
            raise ValidationError("An invoice cannot be created for an appointment not carried out by a doctor or nurse")

        self.duration = duration
        self.amount = float(f"{duration.seconds / 3600 * rate:.2f}")

    def save(self, *args, **kwargs):
        if self.pk is None:
            self.fill_extra_fields()

        super(Invoice, self).save(*args, **kwargs)

from django.conf import settings
from django.db import models
from smartcare_appointments.models import Appointment

class Prescription(models.Model):
    appointment = models.ForeignKey(Appointment, null=True, on_delete=models.CASCADE)
    medicine = models.CharField(max_length=255, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    is_repeating = models.BooleanField(default=False)
    patient = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.CASCADE, related_name='prescription_patient')
    staff = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.CASCADE, related_name='prescription_staff')


class PrescriptionRequest(models.Model):
    prescription = models.ForeignKey(Prescription, null=True, on_delete=models.CASCADE)
    requested_time = models.DateTimeField(null=True)
    approved_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.CASCADE)
    approved_time = models.DateTimeField(null=True)
    collected = models.BooleanField(default=False) # will be changed by the API (external pharmacy site)
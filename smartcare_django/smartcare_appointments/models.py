from django.conf import settings
from django.db import models
from enum import IntEnum

class TimeSlot(IntEnum):
    # 8:00 - 9:59
    EARLY_MORNING = 0
    # 10:00 - 11:59
    LATE_MORNING = 1
    # 12:00 - 14:59
    EARLY_AFTERNOON = 2
    # 15:00 - 18:00
    LATE_AFTERNOON = 3

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]

class AppointmentStage(IntEnum):
    REQUESTED = 0
    OPEN = 1
    COMPLETED = 2
    CANCELLED = 3

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]
    
class Appointment(models.Model):
    patient = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.CASCADE, related_name='appointment_patient')
    staff = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.CASCADE, related_name='appointment_staff')
    reason = models.TextField(blank=True, null=True)

    # time slot that the patient has selected
    stage = models.IntegerField(choices=AppointmentStage.choices(), null=False, default=AppointmentStage.REQUESTED)

    slot_number = models.IntegerField(default=-1)

    # time slot that the patient has selected
    time_slot = models.IntegerField(choices=TimeSlot.choices(), null=False)

    # symptom duration (measured in days)
    symptom_duration = models.IntegerField(null=False, default=1)

    # time that the staff has assigned based on time slot
    assigned_start_time = models.DateTimeField(null=True)

    # time that the appointment actually took place
    actual_start_time = models.DateTimeField(null=True)
    actual_end_time = models.DateTimeField(null=True)

class Prescription(models.Model):
    appointment = models.ForeignKey(Appointment, null=True, on_delete=models.CASCADE)

    medicine = models.CharField(max_length=255, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)

    is_repeating = models.BooleanField(default=False)

class PrescriptionRequest(models.Model):
    prescription = models.ForeignKey(Prescription, null=True, on_delete=models.CASCADE)
    requested_time = models.DateTimeField(null=True)
    approved_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.CASCADE)
    approved_time = models.DateTimeField(null=True)
    collected = models.BooleanField(default=False) # will be changed by the API (external pharmacy site)


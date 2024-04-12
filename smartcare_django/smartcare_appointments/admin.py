from django.contrib import admin

from .models import Appointment, Prescription, PrescriptionRequest
from .schedule_models import WorkingDay, TimeOff
from smartcare_auth.models import Staff
from smartcare_appointments.schedule_models import TimeOff

admin.site.register(Appointment)
admin.site.register(Prescription)
admin.site.register(PrescriptionRequest)
admin.site.register(TimeOff)



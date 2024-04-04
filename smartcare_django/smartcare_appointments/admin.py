from django.contrib import admin

from .models import Appointment, Prescription, PrescriptionRequest
from .schedule_models import WorkingDay, TimeOff
from smartcare_auth.models import Staff

admin.site.register(Appointment)
admin.site.register(Prescription)
admin.site.register(PrescriptionRequest)



from django.contrib import admin

from smartcare_appointments.models import Appointment
from smartcare_appointments.prescriptions_models import Prescription, PrescriptionRequest

admin.site.register(Appointment)
admin.site.register(Prescription)
admin.site.register(PrescriptionRequest)

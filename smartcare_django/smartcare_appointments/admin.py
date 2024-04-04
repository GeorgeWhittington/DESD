from django.contrib import admin

from smartcare_appointments.models import Appointment, Prescription, PrescriptionRequest, WorkingDay, TimeOff

admin.site.register(Appointment)
admin.site.register(Prescription)
admin.site.register(PrescriptionRequest)
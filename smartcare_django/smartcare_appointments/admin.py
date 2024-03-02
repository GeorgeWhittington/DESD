from django.contrib import admin

from .models import Appointment, Prescription, PrescriptionRequest

admin.site.register(Appointment)
admin.site.register(Prescription)
admin.site.register(PrescriptionRequest)

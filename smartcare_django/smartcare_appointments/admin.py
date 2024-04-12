from django.contrib import admin

from smartcare_appointments.models import Appointment, Prescription, PrescriptionRequest, WorkingDay, TimeOff, AppointmentComment

admin.site.register(Appointment)
admin.site.register(Prescription)
admin.site.register(PrescriptionRequest)
admin.site.register(AppointmentComment)
admin.site.register(WorkingDay)
admin.site.register(TimeOff)

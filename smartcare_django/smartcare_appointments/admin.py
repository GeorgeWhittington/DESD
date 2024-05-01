from django.contrib import admin

from smartcare_appointments.models import Appointment, Prescription, PrescriptionRequest, WorkingDay, TimeOff, AppointmentComment

admin.site.register(TimeOff)

@admin.register(WorkingDay)
class WorkingDayAdmin(admin.ModelAdmin):
    list_display = ["format_staff_user", "day"]

    def format_staff_user(self, obj):
        return obj.staff.user
    format_staff_user.short_description = "staff member"


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ["id", "patient", "staff", "date_created", "stage"]


@admin.register(AppointmentComment)
class AppointmentCommentAdmin(admin.ModelAdmin):
    list_display = ["appointment", "created_by", "created_time"]


@admin.register(Prescription)
class PrescriptionAdmin(admin.ModelAdmin):
    list_display = ["medicine", "patient", "staff", "is_repeating"]


@admin.register(PrescriptionRequest)
class PrescriptionRequestAdmin(admin.ModelAdmin):
    list_display = ["prescription", "approved_by", "requested_time", "approved_time", "collected"]
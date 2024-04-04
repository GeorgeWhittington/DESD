from django.contrib import admin, messages
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ngettext
from django.db import transaction
from smartcare_appointments.schedule_models import TimeOff, WorkingDay
from smartcare_appointments.schedule_logic import update_working_days

from .models import User, EmploymentType, Staff, PayRate


class WorkingDayInline(admin.TabularInline):
    model = WorkingDay
    extra = 0
    can_delete = True
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # If there is an object being edited (i.e., we're not creating a new one)
        if hasattr(self, 'instance') and self.instance is not None:
            assigned_days = qs.values_list('day', flat=True)
            self.form.base_fields['day'].queryset = self.form.base_fields['day'].queryset.exclude(name__in=assigned_days)
        return qs


class TimeOffInline(admin.TabularInline):
    model = TimeOff
    extra = 1


@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    inlines = (WorkingDayInline, TimeOffInline,)


class StaffInline(admin.StackedInline):
    model = Staff 
    verbose_name_plural = 'staff'
    fk_name = 'user'
    extra = 0


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    inlines = (StaffInline, )
    list_display = ["username", "email", "full_name", "user_type", "is_active", "is_staff","employment_type_display"]
    fieldsets = UserAdmin.fieldsets + (
        ("Custom Fields", {
            "fields": ("user_type","employment_type",)
        }),
    )

    def employment_type_display(self, obj):
        if hasattr(obj, 'staff_info'):
            return obj.staff_info.get_employment_type_display()
        return None
    employment_type_display.short_description = 'Employment Type'

    actions = ["make_active", "make_inactive", "set_full_time", "set_part_time", "clear_employment_type"]

    @admin.action(description="Activate selected users")
    def make_active(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(
            request,
            ngettext(
                "%d user account was successfully activated.",
                "%d user accounts were successfully activated.",
                updated,
            ) % updated,
            messages.SUCCESS
        )

    @admin.action(description="Deactivate selected users")
    def make_inactive(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(
            request,
            ngettext(
                "%d user account was successfully deactivated.",
                "%d user accounts were successfully deactivated.",
                updated,
            ) % updated,
            messages.SUCCESS
        )

    @admin.action(description="Set selected users as Full Time")
    def set_full_time(self, request, queryset):
        for user in queryset:
            if hasattr(user, 'staff_info'):
                user.staff_info.employment_type = EmploymentType.FULL_TIME.value
                user.staff_info.save()
                update_working_days(user.staff_info)
        self.message_user(request, "Selected users were successfully set to Full Time.", messages.SUCCESS)

    @admin.action(description="Set selected users as Part Time")
    def set_part_time(self, request, queryset):
        for user in queryset:
            if hasattr(user, 'staff_info'):
                user.staff_info.employment_type = EmploymentType.PART_TIME.value
                user.staff_info.save()
                update_working_days(user.staff_info)
        self.message_user(request, "Selected users were successfully set to Part Time.", messages.SUCCESS)

    @admin.action(description="Clear Employment Type for selected users")
    def clear_employment_type(self, request, queryset):
        for user in queryset:
            if hasattr(user, 'staff_info'):
                user.staff_info.employment_type = None
                user.staff_info.save()
        self.message_user(request, "Employment Type for selected users was successfully cleared.", messages.SUCCESS)


@admin.register(PayRate)
class PayRateAdmin(admin.ModelAdmin):
    list_display = ["title", "rate"]
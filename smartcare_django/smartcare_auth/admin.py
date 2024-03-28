from django.contrib import admin, messages
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ngettext
from django.db import transaction
from smartcare_appointments.schedule_models import update_working_days
from .models import User, EmploymentType


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ["username", "email", "full_name", "user_type", "is_active", "is_staff","employment_type"]
    fieldsets = UserAdmin.fieldsets + (
        ("Custom Fields", {
            "fields": ("user_type","employment_type",)
        }),
    )
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
        updated = queryset.update(employment_type=EmploymentType.FULL_TIME.value)

        for user in queryset:
            update_working_days(user)
            
        self.message_user(
            request,
            ngettext(
                "%d user was successfully set to Full Time.",
                "%d users were successfully set to Full Time.",
                updated,
            ) % updated,
            messages.SUCCESS
        )

    @admin.action(description="Set selected users as Part Time")
    def set_part_time(self, request, queryset):
        updated = queryset.update(employment_type=EmploymentType.PART_TIME.value)

        for user in queryset:
            update_working_days(user)

        self.message_user(
            request,
            ngettext(
                "%d user was successfully set to Part Time.",
                "%d users were successfully set to Part Time.",
                updated,
            ) % updated,
            messages.SUCCESS
        )

    @admin.action(description="Clear Employment Type for selected users")
    def clear_employment_type(self, request, queryset):
        updated = queryset.update(employment_type=None)
        self.message_user(
            request,
            ngettext(
                "%d user's employment type was successfully cleared.",
                "%d users' employment types were successfully cleared.",
                updated,
            ) % updated,
            messages.SUCCESS
        )
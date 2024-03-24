from django.contrib import admin, messages
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ngettext

from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ["username", "email", "full_name", "user_type", "is_active", "is_staff"]
    fieldsets = UserAdmin.fieldsets + (
        ("Custom Fields", {
            "fields": ("user_type",)
        }),
    )
    actions = ["make_active", "make_inactive"]

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
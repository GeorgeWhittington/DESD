from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ["username", "email", "first_name", "last_name", "user_type", "is_staff"]
    fieldsets = UserAdmin.fieldsets + (
        ("Custom Fields", {
            "fields": ("user_type",)
        }),
    )
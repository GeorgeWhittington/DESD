from django.contrib import admin

from .models import Invoice

@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ["appointment", "pay_type", "formatted_duration", "formatted_amount", "created_at", "paid_at"]

    def formatted_duration(self, obj):
        return obj.formatted_duration()
    formatted_duration.short_description = "duration"

    def formatted_amount(self, obj):
        return f"£{obj.amount:.2f}"
    formatted_amount.short_description = "amount"
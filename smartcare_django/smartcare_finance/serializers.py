from rest_framework import serializers

from smartcare_auth.models import UserType
from .models import Invoice


class InvoiceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Invoice
        fields = ["appointment", "duration", "amount", "is_paid", "created_at", "paid_at"]
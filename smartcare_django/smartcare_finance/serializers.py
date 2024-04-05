from rest_framework import serializers

from smartcare_auth.serializers import UserSerializer
from smartcare_finance.models import Invoice


class InvoiceSerializer(serializers.HyperlinkedModelSerializer):
    staff = UserSerializer(read_only=True)
    patient = UserSerializer(read_only=True)

    class Meta:
        model = Invoice
        fields = ["staff", "patient", "duration", "amount", "is_paid", "paid_at"]
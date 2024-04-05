from datetime import datetime, date, time

from rest_framework import permissions, viewsets, mixins
from django_filters import rest_framework as filters

from .models import Invoice
from .serializers import InvoiceSerializer
from smartcare_auth.rest_permissions import IsAdmin


class InvoiceFilter(filters.FilterSet):
    date = filters.DateFilter(field_name="created_at", method="filter_date")

    def filter_date(self, queryset, name, value):
        return queryset.filter(created_at__date=value)

    class Meta:
        model = Invoice
        fields = ["date"]


class InvoiceView(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    serializer_class = InvoiceSerializer
    model = Invoice
    queryset = Invoice.objects.all()
    permission_classes = [IsAdmin]
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = InvoiceFilter
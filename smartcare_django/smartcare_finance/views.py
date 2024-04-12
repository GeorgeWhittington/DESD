from rest_framework import permissions, viewsets, mixins

from .models import Invoice
from .serializers import InvoiceSerializer
from smartcare_auth.rest_permissions import IsAdmin


class InvoiceView(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    serializer_class = InvoiceSerializer
    model = Invoice
    queryset = Invoice.objects.all()
    permission_classes = [IsAdmin]
from rest_framework import permissions, viewsets, mixins

from .models import Invoice
from .serializers import InvoiceSerializer


class InvoiceView(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    serializer_class = InvoiceSerializer
    model = Invoice
    queryset = Invoice.objects.all()

    def get_permissions(self):
        return super().get_permissions()
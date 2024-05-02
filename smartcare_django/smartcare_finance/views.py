from datetime import date, timedelta, datetime, UTC
import uuid

from rest_framework import viewsets, mixins, status, permissions
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.response import Response
from django_filters import rest_framework as filters
from weasyprint import HTML
from django_weasyprint.utils import django_url_fetcher
from django.core.files.storage import default_storage
from django.template import loader
from django.db.models import Sum, Case, When, F, functions

from smartcare_finance.models import Invoice
from smartcare_finance.serializers import InvoiceSerializer
from smartcare_auth.rest_permissions import IsAdmin, InvoiceIsOwnerOrExternal
from smartcare_auth.models import PatientPayType


def load_pdf_html(template, context):
    return HTML(
        string=loader.render_to_string(template, context),
        url_fetcher=django_url_fetcher,
        base_url="file://"
    )


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
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = InvoiceFilter

    def get_permissions(self):
        if self.action in ["pay_invoice", "is_invoice_paid"]:
            return [InvoiceIsOwnerOrExternal()]
        else:
            return [IsAdmin()]

    @action(detail=True)
    def pay_invoice(self, request, pk=None):
        invoice = self.get_object()
        invoice.paid_at = datetime.now(UTC)
        invoice.save()
        return Response({"detail": "success"}, status=status.HTTP_200_OK)

    @action(detail=True)
    def is_invoice_paid(self, request, pk=None):
        invoice = self.get_object()
        return Response({"is_paid": invoice.is_paid()}, status=status.HTTP_200_OK)

@api_view(["POST"])
@permission_classes((IsAdmin,))
def generate_turnover_report(request):
    try:
        from_date = date.fromisoformat(request.data.pop("from"))
        to_date = date.fromisoformat(request.data.pop("to"))
        payment_type = request.data.pop("type")
    except KeyError:
        return Response({"detail": "Parameters missing"}, status=status.HTTP_400_BAD_REQUEST)
    except (TypeError, ValueError) as err:
        print(err)
        return Response({"detail": "Please select two valid dates"}, status=status.HTTP_400_BAD_REQUEST)

    if payment_type not in ["private", "nhs", "all"]:
        return Response(
            {"detail": "Invalid report type selected, must be either 'private', 'nhs' or 'all'"},
            status=status.HTTP_400_BAD_REQUEST
        )

    context = {
        "requested_by": request.user,
        "from_date": from_date,
        "to_date": to_date,
        "payment_type": payment_type
    }

    all_invoices = Invoice.objects.filter(created_at__gte=from_date, created_at__lt=to_date + timedelta(days=1))

    if all_invoices.count() < 1:
        return Response({"detail": "No invoices found for the provided timespan"}, status=status.HTTP_404_NOT_FOUND)

    if to_date - from_date > timedelta(weeks=4):
        all_data = None
        nhs_data = None
        private_data = None

        if payment_type == "all":
            all_data = all_invoices.annotate(month=functions.TruncMonth("created_at"))\
                .values("month")\
                .annotate(full_total=Sum("amount", default=0.0))\
                .annotate(settled_total=Sum(Case(When(paid_at__isnull=False, then=F("amount")), default=0.0)))

        if payment_type in ["all", "nhs"]:
            nhs_data = all_invoices.filter(pay_type=PatientPayType.NHS)\
                .annotate(month=functions.TruncMonth("created_at"))\
                .values("month")\
                .annotate(full_total=Sum("amount", default=0.0))\
                .annotate(settled_total=Sum(Case(When(paid_at__isnull=False, then=F("amount")), default=0.0)))

        if payment_type in ["all", "private"]:
            private_data = all_invoices.filter(pay_type=PatientPayType.PRIVATE)\
                .annotate(month=functions.TruncMonth("created_at"))\
                .values("month")\
                .annotate(full_total=Sum("amount", default=0.0))\
                .annotate(settled_total=Sum(Case(When(paid_at__isnull=False, then=F("amount")), default=0.0)))

        # if any of the queries performed fetched more than one month, produce a breakdown
        if any([data is not None and len(data) != 1 for data in [all_data, nhs_data, private_data]]):
            if all_data is not None:
                context["breakdown"] = list(all_data)
            else:
                context["breakdown"] = []

            if nhs_data is not None:
                for entry in nhs_data:

                    found = False
                    for aggregate_entry in context["breakdown"]:
                        if aggregate_entry["month"] == entry["month"]:
                            aggregate_entry["nhs_full_total"] = entry["full_total"]
                            aggregate_entry["nhs_settled_total"] = entry["settled_total"]
                            found = True
                            break

                    if not found:
                        context["breakdown"].append({
                            "month": entry["month"],
                            "nhs_full_total": entry["full_total"],
                            "nhs_settled_total": entry["settled_total"]
                        })

            if private_data is not None:
                for entry in private_data:

                    found = False
                    for aggregate_entry in context["breakdown"]:
                        if aggregate_entry["month"] == entry["month"]:
                            aggregate_entry["private_full_total"] = entry["full_total"]
                            aggregate_entry["private_settled_total"] = entry["settled_total"]
                            found = True
                            break

                    if not found:
                        context["breakdown"].append({
                            "month": entry["month"],
                            "private_full_total": entry["full_total"],
                            "private_settled_total": entry["settled_total"]
                        })

            context["breakdown"] = sorted(context["breakdown"], key=lambda entry: entry["month"])

    context["grand_total"] = {}

    def find_total_and_settled(invoices):
        total = invoices.aggregate(Sum("amount", default=0.0))["amount__sum"]
        settled = invoices.aggregate(
            settled_invoices=Sum(Case(When(paid_at__isnull=False, then=F("amount")), default=0.0)))["settled_invoices"]

        return total, settled

    if payment_type == "all":
        all_total, all_settled = find_total_and_settled(all_invoices)
        context["grand_total"]["All Patients"] = {"total": all_total, "settled": all_settled}

    if payment_type in ["nhs", "all"]:
        nhs_total, nhs_settled = find_total_and_settled(all_invoices.filter(pay_type=PatientPayType.NHS))
        context["grand_total"]["NHS Patients"] = {"total": nhs_total, "settled": nhs_settled}

    if payment_type in ["private", "all"]:
        private_total, private_settled = find_total_and_settled(all_invoices.filter(pay_type=PatientPayType.PRIVATE))
        context["grand_total"]["Private Patients"] = {"total": private_total, "settled": private_settled}

    html = load_pdf_html("smartcare_finance/turnover.html", context)

    filename = f"/reports/turnover-{uuid.uuid4()}.pdf"

    with default_storage.open(default_storage.location + filename, "wb") as file:
        html.write_pdf(file)

    return Response({"pdf": default_storage.url(filename)})
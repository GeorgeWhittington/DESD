from datetime import date, timedelta
import uuid

from rest_framework import viewsets, mixins, status
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
from smartcare_auth.rest_permissions import IsAdmin


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
    permission_classes = [IsAdmin]
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = InvoiceFilter


@api_view(["POST"])
@permission_classes((IsAdmin,))
def generate_turnover_report(request):
    try:
        from_date = date.fromisoformat(request.data.pop("from"))
        to_date = date.fromisoformat(request.data.pop("to"))
        type = request.data.pop("type")
    except KeyError:
        return Response({"detail": "Parameters missing"}, status=status.HTTP_400_BAD_REQUEST)
    except (TypeError, ValueError) as err:
        print(err)
        return Response({"detail": "Please select two valid dates"}, status=status.HTTP_400_BAD_REQUEST)

    if type not in ["private", "nhs", "all"]:
        return Response(
            {"detail": "Invalid report type selected, must be either 'private', 'nhs' or 'all'"},
            status=status.HTTP_400_BAD_REQUEST
        )

    context = {
        "requested_by": request.user,
        "from_date": from_date,
        "to_date": to_date,
        "type": "all"  # TODO: when payment source is stored, make this not hardcoded
    }

    all_invoices = Invoice.objects.filter(created_at__gte=from_date, created_at__lte=to_date)

    if all_invoices.count() < 1:
        return Response({"detail": "No invoices found for the provided timespan"}, status=status.HTTP_404_NOT_FOUND)

    if to_date - from_date > timedelta(weeks=4):
        # TODO: aggregation will need to be modified once private/nhs distinctions are possible
        # (will need to decide if it's better to duplicate this query for each of the three possible groups
        # or if it's better to always fetch all the data, namespace it - private_full_total, nhs_settled_total etc -
        # and then only render what's relevant inside the template, by using the type variable we pass in)
        data = all_invoices.annotate(month=functions.TruncMonth("created_at"))\
            .values("month")\
            .annotate(full_total=Sum("amount", default=0.0))\
            .annotate(settled_total=Sum(Case(When(paid_at__isnull=False, then=F("amount")), default=0.0)))

        if len(data) != 1:
            # Continue, more than one months worth of data was collected
            context["breakdown"] = data

            print(data)

    all_total = all_invoices.aggregate(Sum("amount", default=0.0))["amount__sum"]
    all_settled = all_invoices.aggregate(
        settled_invoices=Sum(Case(When(paid_at__isnull=False, then=F("amount")), default=0.0)))["settled_invoices"]

    context["grand_total"] = {"All Patients": {"total": all_total, "settled": all_settled}}

    html = load_pdf_html("smartcare_finance/turnover.html", context)

    filename = f"/reports/turnover-{uuid.uuid4()}.pdf"

    with default_storage.open(default_storage.location + filename, "wb") as file:
        html.write_pdf(file)

    return Response({"pdf": default_storage.url(filename)})
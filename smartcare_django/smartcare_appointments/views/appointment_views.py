import datetime

from django.core.mail import EmailMessage
from django.conf import settings
from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from rest_framework.response import Response

from smartcare_appointments.slot_logic import scheduler
from smartcare_appointments.models import Appointment, AppointmentComment, AppointmentStage
from smartcare_appointments.serializers import AppointmentSerializer, AppointmentCommentSerializer
from smartcare_finance.models import Invoice
from smartcare_finance.views import load_pdf_html
from smartcare_auth.models import PatientPayType


class AppointmentView(mixins.CreateModelMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer

    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        appointment = self.get_object()
        scheduler(appointment)
        return Response({"result" : f"request to approve {appointment.id}"})

    @action(detail=True, methods=['post'])
    def reject(self, request, pk=None):
        appointment = self.get_object()
        return Response({"result" : "success"})

    @action(detail=True, methods=['post'])
    def begin(self, request, pk=None):
        appointment = self.get_object()
        requested_user = request.user

        # TODO: reimplement this
        # if appointment.staff != requested_user:
        #    return Response({"result" : "error", "message" : "the logged in user does not own this appointment"})

        appointment.actual_start_time = datetime.datetime.now()
        appointment.save()

        comment = AppointmentComment.objects.create(
            created_by=appointment.staff,
            appointment=appointment,
            text="Appointment Started"
        )
        comment.save()

        print('Begin ', 'Appointment', appointment, ' user', requested_user)
        return Response({"result" : "success"})

    @action(detail=True, methods=['post'])
    def end(self, request, pk=None):
        appointment = self.get_object()
        requested_user = request.user

        # TODO: reimplement this
        # if appointment.staff != requested_user:
        #    return Response({"result" : "error", "message" : "the logged in user does not own this appointment"})

        appointment.actual_end_time = datetime.datetime.now()
        appointment.stage = AppointmentStage.COMPLETED
        appointment.save()

        comment = AppointmentComment.objects.create(
            created_by=appointment.staff,
            appointment=appointment,
            text="Appointment Completed"
        )
        comment.save()

        invoice = Invoice(appointment=appointment)

        if hasattr(appointment.patient, "patient_info") and appointment.patient.patient_info.pay_type == PatientPayType.PRIVATE:
            html = load_pdf_html("smartcare_finance/invoice.html", {"invoice": invoice})
            filename = f"/invoice-{invoice.id}.pdf"

            with open(settings.INVOICE_FOLDER + filename, "wb") as file:
                html.write_pdf(file)

            email = EmailMessage(
                subject="Appointment Invoice",
                body=f"""
                Dear {appointment.patient.first_name} {appointment.patient.last_name},

                Thank you for your recent appointment at smartcare. Your invoice is attached to this email.

                Regards, Smartcare.
                """,
                from_email="from@example.com",
                to=["to@example.com", appointment.patient.email]
            )
            email.attach_file(settings.INVOICE_FOLDER + filename, mimetype="application/pdf")
            email.send()

        return Response({"result" : "success"})

    @action(detail=True, methods=['post'])
    def assign_to_current_user(self, request, pk=None):
        appointment = self.get_object()
        requested_user = request.user

        if appointment.staff is None:
            appointment.staff = requested_user
            appointment.save()

        return Response({"result" : "success"})


class AppointmentCommentView(mixins.CreateModelMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = AppointmentComment.objects.all()
    serializer_class = AppointmentCommentSerializer
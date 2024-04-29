import datetime

from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from rest_framework.response import Response

from smartcare_appointments.slot_logic import scheduler
from smartcare_appointments.models import Appointment, AppointmentComment, AppointmentStage
from smartcare_appointments.serializers import AppointmentSerializer, AppointmentCommentSerializer


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
import json
from datetime import datetime, date
from django.db import models
from smartcare_auth.models import User
from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from rest_framework.response import Response

from smartcare_appointments.slot_logic import scheduler
from smartcare_appointments.models import Appointment, AppointmentComment, AppointmentStage
from smartcare_appointments.serializers import AppointmentSerializer, AppointmentCommentSerializer
      
class AppointmentView(mixins.CreateModelMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer

    def get_queryset(self):
        """
        Optionally restricts the returned purchases to a given user,
        by filtering against a `username` query parameter in the URL.
        """
        queryset = Appointment.objects.all()
        
        # filter based on staff / patient user
        if not self.request.user.is_clinic_staff():
            queryset = queryset.filter(patient=self.request.user)
        else:
            if 'staff_id' in self.request.query_params:
                queryset = queryset.filter(staff=User.objects.get(id=int(self.request.query_params.get('staff_id')) ))

            if 'patient_id' in self.request.query_params:
                queryset = queryset.filter(patient=User.objects.get(id=int(self.request.query_params.get('patient_id')) ))

        # filter based on stage
        if 'stage_id' in self.request.query_params:
            stage_id_str = str(self.request.query_params.get('stage_id'))
            stage_ids = []

            if stage_id_str:
                for character in str(self.request.query_params.get('stage_id')):
                    stage_ids.append(int(character))
                
                print(stage_ids)
                queryset = queryset.filter(stage__in=stage_ids)

        return queryset

    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        appointment = self.get_object()

        # update appointment stage
        appointment.stage = AppointmentStage.APPROVED
        appointment.save()

        comment = AppointmentComment.objects.create(
            created_by=request.user,
            appointment=appointment,
            text="Appointment Approved"
        )
        comment.save()

        # try to schedule

        schedule_result = scheduler(appointment)

        if schedule_result:

            comment = AppointmentComment.objects.create(
                created_by=request.user,
                appointment=appointment,
                text=f"Appointment automatically scheduled at {datetime.strftime(appointment.assigned_start_time, '%d/%m/%y %H:%M')} with {appointment.staff.first_name} {appointment.staff.last_name}"
            )
            comment.save()

            return Response({"result" : True, "message": "appointment scheduled"})

        return Response({"result" : False, "message": "failed to automatically schedule appointment"})

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

        appointment.actual_start_time = datetime.now()
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

        appointment.actual_end_time = datetime.now()
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

    @action(detail=True, methods=['post'])
    def add_comment(self, request, pk=None):
        appointment = self.get_object()
        comment = json.loads(request.body)['comment']
        
        if not comment:
            return Response({"result" : "error", "message" : "cannot add empty comment"})

        if self.request.user != appointment.patient and not self.request.user.is_clinic_staff():
            return Response({"result" : "error", "message" : "cannot add comment to another appointment"})

        comment = AppointmentComment.objects.create(
            created_by=request.user,
            appointment=appointment,
            text=comment
        )
        comment.save()

        return Response({"result" : "success"})

class AppointmentCommentView(mixins.CreateModelMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = AppointmentComment.objects.all()
    serializer_class = AppointmentCommentSerializer
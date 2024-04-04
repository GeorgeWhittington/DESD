from django.shortcuts import render
from rest_framework import routers, serializers, viewsets

from smartcare_appointments.models import Appointment
from smartcare_appointments.schedule_models import TimeOff
from smartcare_appointments.schedule_serializers import TimeOffSerializer
from smartcare_appointments.serializers import AppointmentSerializer


class TimeOffView(viewsets.ModelViewSet):
    queryset = TimeOff.objects.all()
    serializer_class = TimeOffSerializer

    # def get_queryset(self):

    #     user = self.request.user
    #     if user.is_authenticated:
    #         return TimeOff.objects.filter(staff__user=user)
    #     else:
    #         return TimeOff.objects.none()
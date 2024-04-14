from django.shortcuts import render
from rest_framework import routers, serializers, viewsets

from smartcare_appointments.models import Appointment, TimeOff
from smartcare_appointments.schedule_serializers import TimeOffSerializer
from smartcare_appointments.serializers import AppointmentSerializer


class TimeOffView(viewsets.ModelViewSet):
    queryset = TimeOff.objects.all()
    serializer_class = TimeOffSerializer

    
from django.shortcuts import render
from rest_framework import routers, serializers, viewsets

from smartcare_appointments.models import Appointment
from smartcare_appointments.serializers import AppointmentSerializer

class AppointmentView(viewsets.ModelViewSet):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer